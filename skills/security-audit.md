---
name: security-audit
description: Perform comprehensive security audit with automated scanning and manual checks
---

# Security Audit

Performs a complete security audit including:
- Dependency vulnerability scanning
- Static code analysis
- Secret detection
- Security best practices check
- OWASP Top 10 verification

## Usage
```
#security-audit <scope>
```

## Example
```
#security-audit full
```

## Audit Steps

### 1. Dependency Scanning

#### Node.js
```bash
# NPM Audit
npm audit --audit-level=moderate

# Snyk scan
npx snyk test

# Check for outdated packages
npm outdated
```

#### Python
```bash
# Safety check
pip install safety
safety check

# Bandit for security issues
pip install bandit
bandit -r . -f json -o security-report.json

# pip-audit
pip install pip-audit
pip-audit
```

#### Go
```bash
# Go vulnerability check
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# Nancy for dependencies
go list -json -m all | nancy sleuth
```

### 2. Secret Detection

#### GitLeaks
```bash
# Install gitleaks
# Windows: choco install gitleaks
# Mac: brew install gitleaks
# Linux: wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz

# Scan repository
gitleaks detect --source . --verbose

# Scan specific files
gitleaks detect --source . --log-opts="--all"
```

#### TruffleHog
```bash
# Install
pip install trufflehog

# Scan repository
trufflehog filesystem . --json > secrets-report.json

# Scan git history
trufflehog git file://. --since-commit HEAD~10
```

### 3. Static Code Analysis

#### SonarQube
```bash
# Run SonarQube scanner
sonar-scanner \
  -Dsonar.projectKey=myproject \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

#### ESLint Security Plugin (JavaScript)
```bash
npm install --save-dev eslint-plugin-security

# .eslintrc.json
{
  "plugins": ["security"],
  "extends": ["plugin:security/recommended"]
}

# Run
npx eslint . --ext .js,.ts
```

#### Semgrep (Multi-language)
```bash
# Install
pip install semgrep

# Run security rules
semgrep --config=auto .

# Specific rulesets
semgrep --config=p/owasp-top-ten .
semgrep --config=p/security-audit .
```

### 4. Container Security

#### Docker Image Scanning
```bash
# Trivy
docker run aquasec/trivy image myimage:latest

# Snyk Container
snyk container test myimage:latest

# Docker Scout
docker scout cves myimage:latest
```

#### Dockerfile Best Practices
```bash
# Hadolint
docker run --rm -i hadolint/hadolint < Dockerfile
```

### 5. Infrastructure Security

#### Terraform Security
```bash
# tfsec
tfsec .

# Checkov
pip install checkov
checkov -d .
```

#### Kubernetes Security
```bash
# kubesec
docker run -i kubesec/kubesec:512c5e0 scan /dev/stdin < deployment.yaml

# kube-bench
kube-bench run --targets master,node
```

### 6. API Security Testing

#### OWASP ZAP
```bash
# Docker
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://api.example.com

# Full scan
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t https://api.example.com
```

#### Burp Suite
```bash
# Use Burp Suite Professional for:
# - Active scanning
# - Passive scanning
# - Intruder attacks
# - Repeater for manual testing
```

### 7. Authentication & Authorization

#### JWT Security Check
```javascript
// Check JWT configuration
const jwt = require('jsonwebtoken');

// ❌ Bad - weak secret
jwt.sign(payload, 'secret');

// ✅ Good - strong secret
jwt.sign(payload, process.env.JWT_SECRET, {
  algorithm: 'HS256',
  expiresIn: '15m',
  issuer: 'myapp',
  audience: 'myapp-users'
});
```

#### OAuth 2.0 Security
```
Checklist:
- [ ] Use PKCE for public clients
- [ ] Validate redirect URIs
- [ ] Use state parameter for CSRF protection
- [ ] Short-lived access tokens (15-30 min)
- [ ] Secure refresh token storage
- [ ] Token rotation on refresh
```

### 8. Database Security

#### SQL Injection Check
```bash
# SQLMap
sqlmap -u "http://example.com/page?id=1" --batch

# Manual check
# Look for:
# - Raw SQL queries
# - String concatenation in queries
# - Unparameterized queries
```

#### Database Configuration
```sql
-- Check user privileges
SELECT user, host, authentication_string FROM mysql.user;

-- Check for weak passwords
SELECT user FROM mysql.user WHERE authentication_string = '';

-- Verify SSL/TLS
SHOW VARIABLES LIKE '%ssl%';
```

### 9. XSS Prevention

#### Content Security Policy
```javascript
// Express.js
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],
  },
}));
```

#### Input Sanitization
```javascript
const DOMPurify = require('isomorphic-dompurify');

// Sanitize HTML
const clean = DOMPurify.sanitize(dirty);

// Escape output
const escape = require('escape-html');
const safe = escape(userInput);
```

### 10. CSRF Protection

```javascript
// Express.js with csurf
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.post('/api/users', csrfProtection, (req, res) => {
  // Protected endpoint
});

// Frontend
<input type="hidden" name="_csrf" value="<%= csrfToken %>" />
```

## Security Report Template

```markdown
# Security Audit Report

**Date**: 2024-01-01
**Auditor**: Security Team
**Scope**: Full Application

## Executive Summary
Brief overview of findings and risk level.

## Critical Vulnerabilities 🔴
1. **SQL Injection in /api/users**
   - Severity: Critical
   - Impact: Database compromise
   - Remediation: Use parameterized queries
   - Status: Open

## High Vulnerabilities 🟠
1. **Weak JWT Secret**
   - Severity: High
   - Impact: Token forgery
   - Remediation: Use strong random secret
   - Status: Fixed

## Medium Vulnerabilities 🟡
1. **Missing Rate Limiting**
   - Severity: Medium
   - Impact: DoS attacks
   - Remediation: Implement rate limiting
   - Status: In Progress

## Low Vulnerabilities 🔵
1. **Outdated Dependencies**
   - Severity: Low
   - Impact: Potential vulnerabilities
   - Remediation: Update packages
   - Status: Open

## Compliance Status
- [ ] OWASP Top 10
- [ ] GDPR
- [ ] PCI-DSS
- [ ] SOC 2

## Recommendations
1. Implement automated security scanning in CI/CD
2. Regular penetration testing (quarterly)
3. Security training for developers
4. Bug bounty program

## Next Steps
1. Fix critical vulnerabilities (Week 1)
2. Address high vulnerabilities (Week 2)
3. Plan for medium/low issues (Month 1)
```

## Automated Security Pipeline

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      
      - name: Run GitLeaks
        uses: gitleaks/gitleaks-action@v2
      
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
      
      - name: Upload results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```
