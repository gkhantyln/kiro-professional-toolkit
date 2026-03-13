---
name: create-microservice
description: Create a complete microservice with API, database, messaging, and deployment
---

# Create Microservice

Creates a production-ready microservice with:
- REST/gRPC API
- Database integration
- Message queue (RabbitMQ/Kafka)
- Docker containerization
- Health checks and monitoring
- CI/CD pipeline

## Usage
```
#create-microservice <service-name> <type>
```

## Example
```
#create-microservice user-service rest
```

## Project Structure

```
user-service/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   ├── controllers/
│   │   └── middleware/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── events/
│   │   ├── publishers/
│   │   └── subscribers/
│   ├── config/
│   └── utils/
├── tests/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── package.json
└── README.md
```

## Implementation

### 1. Main Application (Node.js/Express)
```javascript
// src/app.js
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const { errorHandler } = require('./middleware/errorHandler');
const { requestLogger } = require('./middleware/requestLogger');
const routes = require('./api/routes');
const { connectDB } = require('./config/database');
const { connectMessageQueue } = require('./config/messageQueue');

class Application {
  constructor() {
    this.app = express();
    this.setupMiddleware();
    this.setupRoutes();
    this.setupErrorHandling();
  }

  setupMiddleware() {
    this.app.use(helmet());
    this.app.use(cors());
    this.app.use(express.json());
    this.app.use(requestLogger);
  }

  setupRoutes() {
    this.app.use('/api/v1', routes);
    
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        service: 'user-service',
        timestamp: new Date().toISOString(),
      });
    });
  }

  setupErrorHandling() {
    this.app.use(errorHandler);
  }

  async start() {
    try {
      await connectDB();
      await connectMessageQueue();
      
      const PORT = process.env.PORT || 3000;
      this.app.listen(PORT, () => {
        console.log(`User service listening on port ${PORT}`);
      });
    } catch (error) {
      console.error('Failed to start application:', error);
      process.exit(1);
    }
  }
}

module.exports = Application;
```

### 2. Message Queue Integration
```javascript
// src/config/messageQueue.js
const amqp = require('amqplib');

let channel = null;

async function connectMessageQueue() {
  try {
    const connection = await amqp.connect(process.env.RABBITMQ_URL);
    channel = await connection.createChannel();
    
    // Declare exchanges
    await channel.assertExchange('user.events', 'topic', { durable: true });
    
    console.log('Connected to message queue');
    return channel;
  } catch (error) {
    console.error('Failed to connect to message queue:', error);
    throw error;
  }
}

async function publishEvent(eventType, data) {
  if (!channel) {
    throw new Error('Message queue not connected');
  }
  
  const message = {
    eventType,
    data,
    timestamp: new Date().toISOString(),
    service: 'user-service',
  };
  
  channel.publish(
    'user.events',
    eventType,
    Buffer.from(JSON.stringify(message)),
    { persistent: true }
  );
}

module.exports = { connectMessageQueue, publishEvent };
```

### 3. Event Publisher
```javascript
// src/events/publishers/userCreatedPublisher.js
const { publishEvent } = require('../../config/messageQueue');

class UserCreatedPublisher {
  static async publish(user) {
    await publishEvent('user.created', {
      userId: user.id,
      email: user.email,
      name: user.name,
      createdAt: user.createdAt,
    });
  }
}

module.exports = UserCreatedPublisher;
```

### 4. Event Subscriber
```javascript
// src/events/subscribers/orderCreatedSubscriber.js
const { channel } = require('../../config/messageQueue');

class OrderCreatedSubscriber {
  static async subscribe() {
    const queue = 'user-service.order-created';
    
    await channel.assertQueue(queue, { durable: true });
    await channel.bindQueue(queue, 'order.events', 'order.created');
    
    channel.consume(queue, async (msg) => {
      if (msg) {
        const event = JSON.parse(msg.content.toString());
        await this.handleOrderCreated(event.data);
        channel.ack(msg);
      }
    });
  }
  
  static async handleOrderCreated(data) {
    console.log('Order created:', data);
    // Handle the event
  }
}

module.exports = OrderCreatedSubscriber;
```
