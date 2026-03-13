---
inclusion: manual
---

# Security Checklist

## Pre-Deployment Security Audit

### Authentication & Authorization
- [ ] JWT tokens have short expiry (15-30 minutes)
- [ ] Refresh tokens implemented and rotated
- [ ] Password hashing uses bcrypt/argon2 (min 12 rounds)
- [ ] Multi-factor authentication available for sensitive operations
- [ ] Session management is secure (httpOnly, secure, sameSite cookies)
- [ ] Account lockout after failed login attempts
- [ ] Password reset tokens expire within 1 hour
- [ ] OAuth/OIDC flows properly implemented

### Input Validation & Sanitization
- [ ] All user inputs validated on server-side
- [ ] SQL injection prevention (parameterized queries/ORM)
- [ ] XSS prevention (output encoding, CSP headers)
- [ ] CSRF tokens implemented for state-changing operations
- [ ] File upload validation (type, size, content)
- [ ] Path traversal prevention
- [ ] Command injection prevention
- [ ] XML/JSON parsing limits set

### API Security
- [ ] Rate limiting implemented (per IP, per user)
- [ ] API authentication required for all endpoints
- [ ] CORS properly configured (no wildcard in production)
- [ ] Request size limits enforced
- [ ] Timeout values set for all operations
- [ ] API versioning implemented
- [ ] Sensitive data not exposed in URLs
- [ ] Error messages don't leak system information

### Data Protection
- [ ] Sensitive data encrypted at rest (AES-256)
- [ ] TLS 1.3 enforced for data in transit
- [ ] Database credentials stored in secrets manager
- [ ] PII data identified and protected
- [ ] Data retention policies implemented
- [ ] Secure data deletion procedures
- [ ] Backup encryption enabled
- [ ] Database access restricted by IP/VPN

### Infrastructure Security
- [ ] Firewall rules configured (principle of least privilege)
- [ ] SSH key-based authentication only
- [ ] Root/admin access disabled or restricted
- [ ] Security groups properly configured
- [ ] VPC/network segmentation implemented
- [ ] Bastion host for database access
- [ ] DDoS protection enabled
- [ ] WAF (Web Application Firewall) configured

### Secrets Management
- [ ] No secrets in source code
- [ ] Environment variables used for configuration
- [ ] Secrets rotation policy in place
- [ ] AWS Secrets Manager / HashiCorp Vault used
- [ ] API keys have appropriate scopes
- [ ] Service accounts use minimal permissions
- [ ] Secrets not logged or exposed in errors

### Logging & Monitoring
- [ ] Security events logged (login, logout, permission changes)
- [ ] Failed authentication attempts logged
- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Log aggregation and analysis configured
- [ ] Alerting for suspicious activities
- [ ] Audit trail for data access
- [ ] Log retention policy defined
- [ ] SIEM integration (if applicable)

### Dependency Security
- [ ] All dependencies up to date
- [ ] Vulnerability scanning enabled (Snyk, Dependabot)
- [ ] No known critical vulnerabilities
- [ ] License compliance checked
- [ ] Dependency pinning in package.json/requirements.txt
- [ ] Private package registry for internal packages
- [ ] Supply chain security measures

### Code Security
- [ ] Static code analysis performed (SonarQube, ESLint security rules)
- [ ] No hardcoded credentials or secrets
- [ ] Secure random number generation
- [ ] Proper error handling (no stack traces in production)
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Deserialization vulnerabilities checked
- [ ] Race condition vulnerabilities addressed

### Container Security (if applicable)
- [ ] Base images from trusted sources
- [ ] Images scanned for vulnerabilities
- [ ] Non-root user in containers
- [ ] Minimal image size (distroless/alpine)
- [ ] Secrets not baked into images
- [ ] Container runtime security configured
- [ ] Network policies defined

### Cloud Security (AWS/Azure/GCP)
- [ ] IAM roles follow least privilege
- [ ] MFA enabled for all accounts
- [ ] CloudTrail/Activity logs enabled
- [ ] S3 buckets not publicly accessible
- [ ] Encryption enabled for all services
- [ ] Security groups reviewed
- [ ] Compliance standards met (SOC2, HIPAA, etc.)

### Mobile Security (if applicable)
- [ ] Certificate pinning implemented
- [ ] Secure storage for sensitive data (Keychain/Keystore)
- [ ] Jailbreak/root detection
- [ ] Code obfuscation applied
- [ ] API keys not hardcoded in app
- [ ] Biometric authentication supported
- [ ] App transport security configured

### Compliance & Privacy
- [ ] GDPR compliance (if applicable)
- [ ] CCPA compliance (if applicable)
- [ ] Privacy policy updated
- [ ] Terms of service reviewed
- [ ] Data processing agreements signed
- [ ] Right to deletion implemented
- [ ] Data export functionality available
- [ ] Cookie consent implemented

### Incident Response
- [ ] Incident response plan documented
- [ ] Security contact information available
- [ ] Breach notification procedures defined
- [ ] Backup and recovery tested
- [ ] Rollback procedures documented
- [ ] Security team contacts listed

## OWASP Top 10 Checklist

1. **Broken Access Control**
   - [ ] Authorization checks on every request
   - [ ] No direct object references without validation

2. **Cryptographic Failures**
   - [ ] Strong encryption algorithms used
   - [ ] Proper key management

3. **Injection**
   - [ ] Parameterized queries used
   - [ ] Input validation and sanitization

4. **Insecure Design**
   - [ ] Threat modeling performed
   - [ ] Security requirements defined

5. **Security Misconfiguration**
   - [ ] Default credentials changed
   - [ ] Unnecessary features disabled

6. **Vulnerable Components**
   - [ ] Dependencies updated
   - [ ] Vulnerability scanning enabled

7. **Authentication Failures**
   - [ ] Strong password policy
   - [ ] MFA available

8. **Software and Data Integrity**
   - [ ] Code signing implemented
   - [ ] CI/CD pipeline secured

9. **Logging and Monitoring Failures**
   - [ ] Security events logged
   - [ ] Alerting configured

10. **Server-Side Request Forgery (SSRF)**
    - [ ] URL validation implemented
    - [ ] Network segmentation in place

## Security Testing

- [ ] Penetration testing performed
- [ ] Vulnerability assessment completed
- [ ] Security code review done
- [ ] Automated security tests in CI/CD
- [ ] Third-party security audit (if required)

## Sign-off

- [ ] Security team approval
- [ ] DevOps team approval
- [ ] Compliance team approval (if applicable)
- [ ] Final security scan passed

**Date**: _______________
**Approved by**: _______________
