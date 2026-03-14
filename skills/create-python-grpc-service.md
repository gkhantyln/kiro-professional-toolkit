---
name: create-python-grpc-service
description: Production gRPC service with protobuf, async servicer, interceptors (auth/tracing/metrics), health checking, reflection, and load balancing
---

# Create Python gRPC Service

İleri seviye gRPC servisi oluşturur:
- Async gRPC servicer (grpcio-aio)
- Protobuf schema + code generation
- Interceptor chain (auth + tracing + metrics)
- Server reflection (grpcurl desteği)
- Health checking (grpc_health)
- Graceful shutdown
- Client-side load balancing

## Usage
```
#create-python-grpc-service <service-name>
```

## proto/user_service.proto
```protobuf
syntax = "proto3";
package user.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

option py_generic_services = false;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc StreamUserEvents(StreamUserEventsRequest) returns (stream UserEvent);
  rpc BatchGetUsers(BatchGetUsersRequest) returns (BatchGetUsersResponse);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  UserRole role = 4;
  google.protobuf.Timestamp created_at = 5;
  map<string, string> metadata = 6;
}

message GetUserRequest    { string id = 1; }
message CreateUserRequest { string email = 1; string name = 2; UserRole role = 3; }
message ListUsersRequest  { int32 page = 1; int32 page_size = 2; string filter = 3; }
message ListUsersResponse { repeated User users = 1; int32 total = 2; string next_page_token = 3; }
message StreamUserEventsRequest { string user_id = 1; repeated string event_types = 2; }
message UserEvent         { string id = 1; string type = 2; string user_id = 3; bytes payload = 4; google.protobuf.Timestamp occurred_at = 5; }
message BatchGetUsersRequest  { repeated string ids = 1; }
message BatchGetUsersResponse { map<string, User> users = 1; repeated string not_found_ids = 2; }

enum UserRole { USER_ROLE_UNSPECIFIED = 0; USER_ROLE_USER = 1; USER_ROLE_ADMIN = 2; USER_ROLE_VIEWER = 3; }
```

## service/user_servicer.py
```python
import grpc
import grpc.aio
from grpc_health.v1 import health_pb2, health_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone
import asyncio
import structlog

from proto.generated import user_service_pb2 as pb2
from proto.generated import user_service_pb2_grpc as pb2_grpc
from service.repository import UserRepository

logger = structlog.get_logger()

class UserServicer(pb2_grpc.UserServiceServicer):
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def GetUser(self, request: pb2.GetUserRequest, context: grpc.aio.ServicerContext) -> pb2.User:
        user = await self.repo.get_by_id(request.id)
        if not user:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"User {request.id} not found")
        return self._to_proto(user)

    async def CreateUser(self, request: pb2.CreateUserRequest, context: grpc.aio.ServicerContext) -> pb2.User:
        try:
            user = await self.repo.create(
                email=request.email,
                name=request.name,
                role=request.role,
            )
            return self._to_proto(user)
        except ValueError as e:
            await context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))

    async def ListUsers(self, request: pb2.ListUsersRequest, context: grpc.aio.ServicerContext) -> pb2.ListUsersResponse:
        users, total = await self.repo.list(
            page=request.page or 1,
            page_size=min(request.page_size or 20, 100),
            filter_expr=request.filter,
        )
        return pb2.ListUsersResponse(
            users=[self._to_proto(u) for u in users],
            total=total,
        )

    async def StreamUserEvents(self, request: pb2.StreamUserEventsRequest, context: grpc.aio.ServicerContext):
        """Server-side streaming RPC."""
        async for event in self.repo.stream_events(request.user_id, request.event_types):
            if context.cancelled():
                break
            ts = Timestamp()
            ts.FromDatetime(event.occurred_at)
            yield pb2.UserEvent(
                id=event.id,
                type=event.type,
                user_id=event.user_id,
                payload=event.payload,
                occurred_at=ts,
            )

    async def BatchGetUsers(self, request: pb2.BatchGetUsersRequest, context: grpc.aio.ServicerContext) -> pb2.BatchGetUsersResponse:
        users = await self.repo.batch_get(request.ids)
        found = {u.id: self._to_proto(u) for u in users}
        not_found = [id_ for id_ in request.ids if id_ not in found]
        return pb2.BatchGetUsersResponse(users=found, not_found_ids=not_found)

    def _to_proto(self, user) -> pb2.User:
        ts = Timestamp()
        ts.FromDatetime(user.created_at.replace(tzinfo=timezone.utc))
        return pb2.User(id=user.id, email=user.email, name=user.name, role=user.role, created_at=ts)
```

## interceptors/auth_interceptor.py
```python
import grpc
import grpc.aio
import jwt
import os
from typing import Callable, Any

PUBLIC_METHODS = frozenset([
    "/grpc.health.v1.Health/Check",
    "/grpc.reflection.v1alpha.ServerReflection/ServerReflectionInfo",
])

class AuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails):
        if handler_call_details.method in PUBLIC_METHODS:
            return await continuation(handler_call_details)

        metadata = dict(handler_call_details.invocation_metadata or [])
        token = metadata.get("authorization", "").removeprefix("Bearer ")

        if not token:
            async def deny(request, context):
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing token")
            return grpc.unary_unary_rpc_method_handler(deny)

        try:
            payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
            # Attach user to context via trailing metadata
        except jwt.ExpiredSignatureError:
            async def deny(request, context):
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token expired")
            return grpc.unary_unary_rpc_method_handler(deny)
        except jwt.InvalidTokenError:
            async def deny(request, context):
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
            return grpc.unary_unary_rpc_method_handler(deny)

        return await continuation(handler_call_details)
```

## interceptors/tracing_interceptor.py
```python
import grpc
import grpc.aio
from opentelemetry import trace, propagate
from opentelemetry.trace import SpanKind
from opentelemetry.semconv.trace import SpanAttributes
from typing import Callable

tracer = trace.get_tracer(__name__)

class TracingInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails):
        metadata = dict(handler_call_details.invocation_metadata or [])
        ctx = propagate.extract(metadata)

        with tracer.start_as_current_span(
            handler_call_details.method,
            context=ctx,
            kind=SpanKind.SERVER,
            attributes={
                SpanAttributes.RPC_SYSTEM: "grpc",
                SpanAttributes.RPC_METHOD: handler_call_details.method.split("/")[-1],
                SpanAttributes.RPC_SERVICE: handler_call_details.method.split("/")[-2],
            },
        ) as span:
            handler = await continuation(handler_call_details)
            return handler
```

## server/main.py
```python
import asyncio
import grpc
import grpc.aio
from grpc_health.v1 import health_pb2_grpc, health
from grpc_reflection.v1alpha import reflection
import structlog
import os

from proto.generated import user_service_pb2, user_service_pb2_grpc
from service.user_servicer import UserServicer
from service.repository import UserRepository
from interceptors.auth_interceptor import AuthInterceptor
from interceptors.tracing_interceptor import TracingInterceptor

logger = structlog.get_logger()

async def serve():
    server = grpc.aio.server(
        interceptors=[TracingInterceptor(), AuthInterceptor()],
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
            ("grpc.keepalive_time_ms", 10_000),
            ("grpc.keepalive_timeout_ms", 5_000),
            ("grpc.keepalive_permit_without_calls", True),
        ],
    )

    repo = UserRepository()
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(repo), server)

    # Health checking
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set("user.v1.UserService", health.SERVICE_UNKNOWN)

    # Server reflection (enables grpcurl)
    SERVICE_NAMES = (
        user_service_pb2.DESCRIPTOR.services_by_name["UserService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    port = os.environ.get("GRPC_PORT", "50051")
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info("gRPC server started", port=port)

    health_servicer.set("user.v1.UserService", health.SERVING)

    async def shutdown():
        logger.info("Shutting down gRPC server")
        await server.stop(grace=30)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(shutdown()))
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
```
