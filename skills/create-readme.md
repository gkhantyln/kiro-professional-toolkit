---
name: create-readme
description: Create comprehensive README.md with all essential sections
---

# Create README

Creates a professional README.md with:
- Project description
- Installation instructions
- Usage examples
- API documentation
- Contributing guidelines

## Usage
```
#create-readme <project-name>
```

## Example
```
#create-readme my-awesome-api
```

## README Template

```markdown
# Project Name

Brief description of what this project does and who it's for.

![Build Status](https://img.shields.io/github/workflow/status/user/repo/CI)
![Coverage](https://img.shields.io/codecov/c/github/user/repo)
![License](https://img.shields.io/github/license/user/repo)

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Node.js 18.x or higher
- PostgreSQL 14.x or higher
- Redis 7.x or higher

## Installation

### Clone the repository
```bash
git clone https://github.com/username/project.git
cd project
```

### Install dependencies
```bash
npm install
```

### Setup environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Run database migrations
```bash
npm run migrate
```

### Start the application
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage

### Basic Example
```javascript
const client = new APIClient({
  apiKey: 'your-api-key',
  baseURL: 'https://api.example.com'
});

const user = await client.users.create({
  email: 'user@example.com',
  name: 'John Doe'
});
```

### Advanced Example
```javascript
// With error handling
try {
  const users = await client.users.list({
    page: 1,
    limit: 20,
    filter: { status: 'active' }
  });
  
  console.log(`Found ${users.length} users`);
} catch (error) {
  console.error('Failed to fetch users:', error.message);
}
```

## API Reference

### Authentication

All API requests require authentication using an API key:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/users
```

### Endpoints

#### Create User
```http
POST /api/v1/users
```

**Request Body**
```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response**
```json
{
  "id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Configuration

Configuration is done through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `JWT_SECRET` | Secret for JWT tokens | Required |
| `LOG_LEVEL` | Logging level | `info` |

## Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- user.test.ts
```

## Deployment

### Docker
```bash
docker build -t myapp .
docker run -p 3000:3000 myapp
```

### Docker Compose
```bash
docker-compose up -d
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to:
- Update tests as appropriate
- Follow the existing code style
- Update documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/username/project](https://github.com/username/project)

## Acknowledgments

- [Library Name](https://example.com) - Description
- [Another Library](https://example.com) - Description
```
