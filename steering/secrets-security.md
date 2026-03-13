---
inclusion: auto
---

# Secrets Security Rules

## CRITICAL: Never Commit Secrets

### ❌ NEVER Do This
```javascript
// ❌ Hardcoded API key
const apiKey = 'sk_live_abc123xyz';

// ❌ Hardcoded database password
const dbPassword = 'mypassword123';

// ❌ Hardcoded JWT secret
const jwtSecret = 'secret';

// ❌ Credentials in code
const config = {
  aws: {
    accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
    secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
  }
};
```

### ✅ ALWAYS Do This
```javascript
// ✅ Use environment variables
const apiKey = process.env.STRIPE_API_KEY;

// ✅ Use secret manager
const dbPassword = await getSecret('database-password');

// ✅ Strong random JWT secret from env
const jwtSecret = process.env.JWT_SECRET;

// ✅ AWS credentials from IAM roles or env
const config = {
  aws: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
  }
};
```

## .gitignore Requirements

```gitignore
# Environment variables
.env
.env.local
.env.*.local
.env.production

# Secrets
secrets/
*.key
*.pem
*.p12
*.pfx

# AWS
.aws/
credentials

# SSH keys
id_rsa
id_rsa.pub
*.ppk

# Certificates
*.crt
*.cer
*.der

# Database
*.db
*.sqlite
*.sqlite3

# Logs (may contain sensitive data)
*.log
logs/
```

## Secret Validation

### Minimum Requirements
- JWT secrets: Minimum 32 characters, random
- API keys: Use provider-generated keys
- Passwords: Minimum 12 characters, complex
- Database passwords: Minimum 16 characters, random
- Encryption keys: 256-bit minimum

### Secret Generation
```javascript
// Generate strong secret
const crypto = require('crypto');

// JWT secret (32 bytes = 256 bits)
const jwtSecret = crypto.randomBytes(32).toString('hex');

// API key (24 bytes = 192 bits)
const apiKey = crypto.randomBytes(24).toString('base64');

// Password (16 bytes with special chars)
const password = crypto.randomBytes(16).toString('base64');
```

## Secret Rotation

### Rotation Schedule
- Database passwords: Every 90 days
- API keys: Every 180 days
- JWT secrets: Every 365 days
- Service account keys: Every 90 days
- SSL/TLS certificates: Before expiry

### Rotation Process
1. Generate new secret
2. Update secret in secret manager
3. Deploy new secret to applications
4. Verify applications using new secret
5. Revoke old secret after grace period
6. Monitor for errors

## Logging Rules

### ❌ NEVER Log Secrets
```javascript
// ❌ Bad
console.log('API Key:', apiKey);
logger.info({ password: userPassword });
console.log('JWT Token:', token);
```

### ✅ ALWAYS Redact Secrets
```javascript
// ✅ Good
console.log('API Key: [REDACTED]');
logger.info({ password: '[REDACTED]' });
console.log('JWT Token: [REDACTED]');

// Redaction helper
function redactSecrets(obj) {
  const sensitiveKeys = ['password', 'token', 'secret', 'apiKey', 'key'];
  const redacted = { ...obj };
  
  for (const key of Object.keys(redacted)) {
    if (sensitiveKeys.some(k => key.toLowerCase().includes(k))) {
      redacted[key] = '[REDACTED]';
    }
  }
  
  return redacted;
}
```

## Access Control

### Principle of Least Privilege
- Only grant access to secrets that are needed
- Use separate secrets for different environments
- Rotate secrets when team members leave
- Audit secret access regularly

### Secret Scoping
```
Development:  dev/database, dev/api-keys
Staging:      staging/database, staging/api-keys
Production:   prod/database, prod/api-keys
```

## Encryption

### Encrypt Secrets at Rest
```javascript
const crypto = require('crypto');

// Encryption
function encrypt(text, masterKey) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', masterKey, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}

// Decryption
function decrypt(encrypted, iv, authTag, masterKey) {
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    masterKey,
    Buffer.from(iv, 'hex')
  );
  
  decipher.setAuthTag(Buffer.from(authTag, 'hex'));
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}
```

## Emergency Procedures

### If Secret is Compromised
1. Immediately rotate the secret
2. Revoke compromised secret
3. Audit access logs
4. Notify security team
5. Investigate breach
6. Update incident response plan

### Incident Response Checklist
- [ ] Identify compromised secret
- [ ] Assess impact and scope
- [ ] Rotate secret immediately
- [ ] Review access logs
- [ ] Notify affected parties
- [ ] Document incident
- [ ] Implement preventive measures
