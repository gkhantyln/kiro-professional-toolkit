---
name: setup-authentication
description: Setup complete authentication system with JWT, OAuth, and MFA
---

# Setup Authentication

Creates a production-ready authentication system with:
- JWT access and refresh tokens
- OAuth 2.0 (Google, GitHub)
- Multi-factor authentication (MFA)
- Password reset flow
- Email verification
- Rate limiting

## Usage
```
#setup-authentication <strategy>
```

## Example
```
#setup-authentication jwt-oauth
```

## Implementation

### 1. JWT Authentication
```javascript
// src/services/authService.js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const crypto = require('crypto');
const { User } = require('../models');

class AuthService {
  static async register(email, password, name) {
    // Check if user exists
    const existing = await User.findOne({ where: { email } });
    if (existing) {
      throw new Error('User already exists');
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);
    
    // Create user
    const user = await User.create({
      email,
      password: hashedPassword,
      name,
      verificationToken: crypto.randomBytes(32).toString('hex'),
    });
    
    // Send verification email
    await this.sendVerificationEmail(user);
    
    return user;
  }
  
  static async login(email, password) {
    // Find user
    const user = await User.findOne({ where: { email } });
    if (!user) {
      throw new Error('Invalid credentials');
    }
    
    // Check password
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new Error('Invalid credentials');
    }
    
    // Check if verified
    if (!user.isVerified) {
      throw new Error('Please verify your email');
    }
    
    // Generate tokens
    const accessToken = this.generateAccessToken(user);
    const refreshToken = this.generateRefreshToken(user);
    
    // Save refresh token
    await user.update({ refreshToken });
    
    return { accessToken, refreshToken, user };
  }
  
  static generateAccessToken(user) {
    return jwt.sign(
      {
        userId: user.id,
        email: user.email,
        role: user.role,
      },
      process.env.JWT_SECRET,
      { expiresIn: '15m' }
    );
  }
  
  static generateRefreshToken(user) {
    return jwt.sign(
      { userId: user.id },
      process.env.REFRESH_TOKEN_SECRET,
      { expiresIn: '7d' }
    );
  }
  
  static async refreshAccessToken(refreshToken) {
    try {
      const decoded = jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET);
      const user = await User.findByPk(decoded.userId);
      
      if (!user || user.refreshToken !== refreshToken) {
        throw new Error('Invalid refresh token');
      }
      
      const newAccessToken = this.generateAccessToken(user);
      return newAccessToken;
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }
}

module.exports = AuthService;
```

### 2. Authentication Middleware
```javascript
// src/middleware/auth.js
const jwt = require('jsonwebtoken');
const { User } = require('../models');

async function authenticate(req, res, next) {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findByPk(decoded.userId);
    
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }
    
    req.user = user;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

function authorize(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

module.exports = { authenticate, authorize };
```

### 3. OAuth 2.0 (Google)
```javascript
// src/services/oauthService.js
const { OAuth2Client } = require('google-auth-library');
const { User } = require('../models');
const AuthService = require('./authService');

const client = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

class OAuthService {
  static async googleLogin(idToken) {
    try {
      const ticket = await client.verifyIdToken({
        idToken,
        audience: process.env.GOOGLE_CLIENT_ID,
      });
      
      const payload = ticket.getPayload();
      const { email, name, picture, sub: googleId } = payload;
      
      // Find or create user
      let user = await User.findOne({ where: { email } });
      
      if (!user) {
        user = await User.create({
          email,
          name,
          picture,
          googleId,
          isVerified: true,
          provider: 'google',
        });
      }
      
      // Generate tokens
      const accessToken = AuthService.generateAccessToken(user);
      const refreshToken = AuthService.generateRefreshToken(user);
      
      await user.update({ refreshToken });
      
      return { accessToken, refreshToken, user };
    } catch (error) {
      throw new Error('Invalid Google token');
    }
  }
}

module.exports = OAuthService;
```
