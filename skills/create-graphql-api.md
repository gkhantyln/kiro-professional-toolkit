---
name: create-graphql-api
description: Create GraphQL API with Apollo Server, schema, resolvers, and subscriptions
---

# Create GraphQL API

Creates a production-ready GraphQL API with:
- Apollo Server
- Type-safe schema
- Resolvers
- DataLoader (N+1 prevention)
- Subscriptions (WebSocket)
- Authentication
- Error handling

## Usage
```
#create-graphql-api <resource>
```

## Example
```
#create-graphql-api users
```

## Implementation

### 1. Apollo Server Setup
```javascript
// src/graphql/server.js
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const { makeExecutableSchema } = require('@graphql-tools/schema');
const { WebSocketServer } = require('ws');
const { useServer } = require('graphql-ws/lib/use/ws');
const typeDefs = require('./schema');
const resolvers = require('./resolvers');
const { createContext } = require('./context');

async function createApolloServer(app, httpServer) {
  const schema = makeExecutableSchema({ typeDefs, resolvers });
  
  const server = new ApolloServer({
    schema,
    formatError: (error) => {
      console.error(error);
      return {
        message: error.message,
        code: error.extensions?.code,
        path: error.path,
      };
    },
  });
  
  await server.start();
  
  // HTTP endpoint
  app.use(
    '/graphql',
    express.json(),
    expressMiddleware(server, {
      context: createContext,
    })
  );
  
  // WebSocket endpoint for subscriptions
  const wsServer = new WebSocketServer({
    server: httpServer,
    path: '/graphql',
  });
  
  useServer({ schema, context: createContext }, wsServer);
  
  return server;
}

module.exports = { createApolloServer };
```

### 2. Schema Definition
```graphql
# src/graphql/schema.graphql
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!
  author: User!
  createdAt: DateTime!
}

input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input CreatePostInput {
  title: String!
  content: String!
  published: Boolean
}

type Query {
  me: User
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
  posts(published: Boolean): [Post!]!
}

type Mutation {
  register(input: CreateUserInput!): AuthPayload!
  login(email: String!, password: String!): AuthPayload!
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: CreatePostInput!): Post!
  deletePost(id: ID!): Boolean!
}

type Subscription {
  postCreated: Post!
  postUpdated(id: ID!): Post!
}

type AuthPayload {
  token: String!
  user: User!
}

scalar DateTime
```

### 3. Resolvers
```javascript
// src/graphql/resolvers/index.js
const { GraphQLError } = require('graphql');
const { PubSub } = require('graphql-subscriptions');
const userResolvers = require('./userResolvers');
const postResolvers = require('./postResolvers');

const pubsub = new PubSub();

const resolvers = {
  Query: {
    ...userResolvers.Query,
    ...postResolvers.Query,
  },
  Mutation: {
    ...userResolvers.Mutation,
    ...postResolvers.Mutation,
  },
  Subscription: {
    ...postResolvers.Subscription,
  },
  User: {
    posts: async (parent, args, context) => {
      return context.loaders.postsByUserId.load(parent.id);
    },
  },
  Post: {
    author: async (parent, args, context) => {
      return context.loaders.userById.load(parent.authorId);
    },
  },
};

module.exports = resolvers;
```
