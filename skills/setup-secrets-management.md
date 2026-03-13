---
name: setup-secrets-management
description: Setup secure secrets management with environment variables and secret managers
---

# Setup Secrets Management

Implements secure secrets management with:
- Environment variables
- Secret managers (AWS, Azure, HashiCorp Vault)
- Encryption at rest
- Secret rotation
- Audit logging

## Usage
```
#setup-secrets-management <provider>
```

## Example
```
#setup-secrets-management aws
```

## Implementation

### 1. Environment Variables (.env)

#### .env.example
```bash
# Application
NODE_ENV=production
PORT=3000
APP_URL=https://example.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DB_POOL_MIN=2
DB_POOL_MAX=10

# Redis
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=

# Authentication
JWT_SECRET=your-super-secret-jwt-key-min-32-chars
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_SECRET=your-refresh-token-secret
REFRESH_TOKEN_EXPIRES_IN=7d

# OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET=

# Monitoring
SENTRY_DSN=
```

#### .env Loading (Node.js)
```javascript
// config/env.js
require('dotenv').config();

const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'REDIS_URL'
];

// Validate required variables
requiredEnvVars.forEach(varName => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});

module.exports = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT, 10) || 3000,
  database: {
    url: process.env.DATABASE_URL,
    poolMin: parseInt(process.env.DB_POOL_MIN, 10) || 2,
    poolMax: parseInt(process.env.DB_POOL_MAX, 10) || 10,
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '15m',
  },
  redis: {
    url: process.env.REDIS_URL,
  },
};
```

### 2. AWS Secrets Manager

#### Setup
```javascript
// config/secrets.js
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({
  region: process.env.AWS_REGION || 'us-east-1',
});

async function getSecret(secretName) {
  try {
    const response = await client.send(
      new GetSecretValueCommand({
        SecretId: secretName,
      })
    );
    
    return JSON.parse(response.SecretString);
  } catch (error) {
    console.error('Error retrieving secret:', error);
    throw error;
  }
}

// Usage
async function loadSecrets() {
  const dbSecrets = await getSecret('prod/database');
  const apiSecrets = await getSecret('prod/api-keys');
  
  return {
    database: {
      host: dbSecrets.host,
      password: dbSecrets.password,
    },
    apiKeys: {
      stripe: apiSecrets.stripe,
      sendgrid: apiSecrets.sendgrid,
    },
  };
}

module.exports = { getSecret, loadSecrets };
```

#### Terraform Setup
```hcl
# secrets.tf
resource "aws_secretsmanager_secret" "database" {
  name = "prod/database"
  description = "Database credentials"
  
  rotation_rules {
    automatically_after_days = 30
  }
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    host     = "db.example.com"
    username = "admin"
    password = random_password.db_password.result
  })
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}
```

### 3. HashiCorp Vault

#### Setup
```javascript
// config/vault.js
const vault = require('node-vault')({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR || 'http://localhost:8200',
  token: process.env.VAULT_TOKEN,
});

async function getVaultSecret(path) {
  try {
    const result = await vault.read(path);
    return result.data;
  } catch (error) {
    console.error('Error reading from Vault:', error);
    throw error;
  }
}

// Usage
async function loadVaultSecrets() {
  const dbCreds = await getVaultSecret('secret/data/database');
  const apiKeys = await getVaultSecret('secret/data/api-keys');
  
  return {
    database: dbCreds.data,
    apiKeys: apiKeys.data,
  };
}

module.exports = { getVaultSecret, loadVaultSecrets };
```
