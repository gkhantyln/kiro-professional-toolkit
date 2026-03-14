---
name: setup-websocket-server
description: Production WebSocket server with Socket.io, rooms, presence tracking, horizontal scaling via Redis adapter, and reconnection handling
---

# Setup WebSocket Server

Production-ready WebSocket sunucusu kurar:
- Socket.io + Redis adapter (horizontal scaling)
- Room/namespace yönetimi
- Presence tracking (online users)
- JWT authentication middleware
- Reconnection & message queuing
- Rate limiting per connection

## Usage
```
#setup-websocket-server <node|go>
```

## server/socket.ts
```typescript
import { Server, Socket } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';
import { verifyToken } from '../lib/auth';
import { logger } from '../lib/logger';

export async function createSocketServer(httpServer: any): Promise<Server> {
  const io = new Server(httpServer, {
    cors: { origin: process.env.ALLOWED_ORIGINS?.split(','), credentials: true },
    pingTimeout: 20000,
    pingInterval: 25000,
    transports: ['websocket', 'polling'],
  });

  // Redis adapter for horizontal scaling
  const pubClient = createClient({ url: process.env.REDIS_URL });
  const subClient = pubClient.duplicate();
  await Promise.all([pubClient.connect(), subClient.connect()]);
  io.adapter(createAdapter(pubClient, subClient));

  // JWT auth middleware
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth.token;
      socket.data.user = await verifyToken(token);
      next();
    } catch {
      next(new Error('Unauthorized'));
    }
  });

  // Rate limiting
  const connectionCount = new Map<string, number>();
  io.use((socket, next) => {
    const ip = socket.handshake.address;
    const count = (connectionCount.get(ip) ?? 0) + 1;
    if (count > 10) return next(new Error('Too many connections'));
    connectionCount.set(ip, count);
    socket.on('disconnect', () => connectionCount.set(ip, count - 1));
    next();
  });

  io.on('connection', (socket: Socket) => {
    const userId = socket.data.user.id;
    logger.info({ userId, socketId: socket.id }, 'Client connected');

    // Presence tracking
    socket.join(`user:${userId}`);
    io.emit('presence:online', { userId });

    socket.on('room:join', async ({ roomId }: { roomId: string }) => {
      await socket.join(roomId);
      socket.to(roomId).emit('room:user_joined', { userId, roomId });
    });

    socket.on('room:leave', async ({ roomId }: { roomId: string }) => {
      await socket.leave(roomId);
      socket.to(roomId).emit('room:user_left', { userId, roomId });
    });

    socket.on('message:send', async ({ roomId, content }: { roomId: string; content: string }) => {
      const message = { id: crypto.randomUUID(), userId, content, timestamp: Date.now() };
      io.to(roomId).emit('message:new', message);
      // Persist to DB here
    });

    socket.on('disconnect', (reason) => {
      logger.info({ userId, reason }, 'Client disconnected');
      io.emit('presence:offline', { userId });
    });
  });

  return io;
}
```

## client/socket-client.ts
```typescript
import { io, Socket } from 'socket.io-client';

class SocketClient {
  private socket: Socket | null = null;
  private messageQueue: Array<{ event: string; data: unknown }> = [];

  connect(token: string): Socket {
    this.socket = io(process.env.NEXT_PUBLIC_WS_URL!, {
      auth: { token },
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      transports: ['websocket'],
    });

    this.socket.on('connect', () => {
      console.log('Connected:', this.socket!.id);
      // Flush queued messages
      this.messageQueue.forEach(({ event, data }) => this.socket!.emit(event, data));
      this.messageQueue = [];
    });

    this.socket.on('connect_error', (err) => {
      console.error('Connection error:', err.message);
    });

    return this.socket;
  }

  emit(event: string, data: unknown) {
    if (this.socket?.connected) {
      this.socket.emit(event, data);
    } else {
      this.messageQueue.push({ event, data }); // Queue for reconnect
    }
  }

  disconnect() {
    this.socket?.disconnect();
    this.socket = null;
  }
}

export const socketClient = new SocketClient();
```
