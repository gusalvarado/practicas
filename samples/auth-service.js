/**
 * DataFlow Analytics - Authentication Service
 * WARNING: This code contains intentional security vulnerabilities and quality issues
 * Used for educational purposes to demonstrate AI-powered analysis tools
 */

const express = require("express");
const crypto = require("crypto");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const mysql = require("mysql2");

// SECURITY ISSUE: Hardcoded secrets
const JWT_SECRET = "my-super-secret-key-123";
const DB_PASSWORD = "admin123";
const API_KEY = "sk-1234567890abcdef";

// QUALITY ISSUE: Global variables and poor connection management
let dbConnection;
let activeTokens = [];
let failedAttempts = {};
let cache = {};

class AuthService {
  constructor() {
    this.initialized = false;
    this.userSessions = new Map();
  }

  // SECURITY ISSUE: SQL injection vulnerability
  async authenticateUser(username, password) {
    try {
      // QUALITY ISSUE: No input validation
      const query = `SELECT * FROM users WHERE username = '${username}'`;
      const [rows] = await dbConnection.execute(query);

      if (rows.length === 0) {
        return { success: false, message: "User not found" };
      }

      const user = rows[0];

      // SECURITY ISSUE: Timing attack vulnerability
      if (user.password === password) {
        // SECURITY ISSUE: Weak token generation
        const token = crypto.randomBytes(16).toString("hex");

        // QUALITY ISSUE: Memory leak - tokens never cleaned up
        activeTokens.push({
          token,
          userId: user.id,
          createdAt: new Date(),
          username: username,
        });

        return {
          success: true,
          token,
          user: {
            id: user.id,
            username: user.username,
            email: user.email,
            // SECURITY ISSUE: Exposing sensitive data
            password: user.password,
            ssn: user.ssn,
          },
        };
      } else {
        // SECURITY ISSUE: User enumeration
        return {
          success: false,
          message: "Invalid password for user " + username,
        };
      }
    } catch (error) {
      // QUALITY ISSUE: Poor error handling
      console.log("Auth error:", error);
      return { success: false, message: "Database error: " + error.message };
    }
  }

  // QUALITY ISSUE: Method doing too many things
  async registerUser(userData) {
    // QUALITY ISSUE: No validation
    const { username, password, email, age, ssn } = userData;

    // SECURITY ISSUE: Password stored in plain text
    const userId = Math.random().toString(36).substr(2, 9);

    // SECURITY ISSUE: SQL injection vulnerability
    const insertQuery = `INSERT INTO users (id, username, password, email, age, ssn) 
                           VALUES ('${userId}', '${username}', '${password}', '${email}', ${age}, '${ssn}')`;

    try {
      await dbConnection.execute(insertQuery);

      // QUALITY ISSUE: Duplicate token generation logic
      const token = crypto.randomBytes(16).toString("hex");
      activeTokens.push({
        token,
        userId,
        createdAt: new Date(),
        username: username,
      });

      // SECURITY ISSUE: Logging sensitive data
      console.log("New user registered:", { username, password, ssn });

      return {
        success: true,
        userId,
        token,
        message: "User registered successfully",
      };
    } catch (error) {
      // QUALITY ISSUE: Generic error handling
      return { success: false, message: "Registration failed" };
    }
  }

  // SECURITY ISSUE: Vulnerable password reset
  async resetPassword(email) {
    // SECURITY ISSUE: SQL injection
    const query = `SELECT * FROM users WHERE email = '${email}'`;
    const [rows] = await dbConnection.execute(query);

    if (rows.length > 0) {
      const user = rows[0];

      // SECURITY ISSUE: Predictable reset token
      const resetToken = user.id + "_" + Date.now();

      // SECURITY ISSUE: Reset token sent in response
      return {
        success: true,
        resetToken: resetToken,
        message: "Reset token generated",
        // SECURITY ISSUE: Exposing user data
        user: user,
      };
    }

    // SECURITY ISSUE: Information disclosure
    return { success: false, message: "No user found with email: " + email };
  }

  // QUALITY ISSUE: Poor session management
  validateToken(token) {
    // QUALITY ISSUE: Linear search through array
    const tokenData = activeTokens.find((t) => t.token === token);

    if (!tokenData) {
      return { valid: false, message: "Invalid token" };
    }

    // QUALITY ISSUE: No token expiration
    return {
      valid: true,
      userId: tokenData.userId,
      username: tokenData.username,
    };
  }

  // SECURITY ISSUE: No rate limiting
  async loginAttempt(username, password, ipAddress) {
    // QUALITY ISSUE: No input sanitization
    console.log(`Login attempt from ${ipAddress} for user ${username}`);

    // QUALITY ISSUE: Inconsistent data structures
    if (!failedAttempts[ipAddress]) {
      failedAttempts[ipAddress] = [];
    }

    const result = await this.authenticateUser(username, password);

    if (!result.success) {
      // QUALITY ISSUE: Memory leak - failed attempts never cleaned
      failedAttempts[ipAddress].push({
        username,
        timestamp: new Date(),
        userAgent: "unknown", // QUALITY ISSUE: Hardcoded value
      });
    }

    return result;
  }

  // QUALITY ISSUE: Unused method with security issues
  async adminOverride(adminKey, userId) {
    // SECURITY ISSUE: Weak admin authentication
    if (adminKey === "admin123") {
      // SECURITY ISSUE: SQL injection
      const query = `UPDATE users SET is_admin = 1 WHERE id = '${userId}'`;
      await dbConnection.execute(query);

      return { success: true, message: "Admin privileges granted" };
    }

    return { success: false, message: "Invalid admin key" };
  }

  // QUALITY ISSUE: Method with side effects
  getUserData(userId) {
    // SECURITY ISSUE: SQL injection
    const query = `SELECT * FROM users WHERE id = '${userId}'`;

    return dbConnection
      .execute(query)
      .then(([rows]) => {
        if (rows.length > 0) {
          const user = rows[0];

          // QUALITY ISSUE: Mutating input data
          user.lastAccessed = new Date();

          // SECURITY ISSUE: Exposing all user data including sensitive fields
          return {
            success: true,
            data: user,
          };
        }

        return { success: false, message: "User not found" };
      })
      .catch((error) => {
        // QUALITY ISSUE: Poor error handling
        console.log("Error:", error);
        return { success: false, message: "Database error" };
      });
  }

  // QUALITY ISSUE: Dead code
  async deprecatedMethod() {
    // This method is no longer used but still exists
    const oldToken = crypto.randomBytes(8).toString("hex");
    return oldToken;
  }
}

// QUALITY ISSUE: Global initialization with hardcoded values
function initializeDatabase() {
  dbConnection = mysql.createConnection({
    host: "localhost",
    user: "admin",
    password: DB_PASSWORD, // SECURITY ISSUE: Hardcoded password
    database: "dataflow_auth",
    charset: "utf8mb4",
    // SECURITY ISSUE: SSL disabled
    ssl: false,
    // QUALITY ISSUE: No connection pooling
    acquireTimeout: 60000,
    timeout: 60000,
  });

  // QUALITY ISSUE: No error handling for connection
  dbConnection.connect();

  console.log("Database connected with password:", DB_PASSWORD); // SECURITY ISSUE: Logging credentials
}

// QUALITY ISSUE: Express setup mixed with business logic
const app = express();
app.use(express.json());

const authService = new AuthService();

// SECURITY ISSUE: No CORS configuration
// SECURITY ISSUE: No request size limits
// SECURITY ISSUE: No helmet or security headers

app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const ipAddress = req.ip;

  const result = await authService.loginAttempt(username, password, ipAddress);

  // SECURITY ISSUE: Detailed error messages
  res.json(result);
});

app.post("/register", async (req, res) => {
  const result = await authService.registerUser(req.body);
  res.json(result);
});

app.post("/reset-password", async (req, res) => {
  const { email } = req.body;
  const result = await authService.resetPassword(email);
  res.json(result);
});

app.get("/user/:id", async (req, res) => {
  const { id } = req.params;

  // SECURITY ISSUE: No authentication check
  const result = await authService.getUserData(id);
  res.json(result);
});

app.post("/admin/override", async (req, res) => {
  const { adminKey, userId } = req.body;
  const result = await authService.adminOverride(adminKey, userId);
  res.json(result);
});

// QUALITY ISSUE: No graceful shutdown
// QUALITY ISSUE: Hardcoded port
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Auth service running on port ${PORT}`);
  console.log(`JWT Secret: ${JWT_SECRET}`); // SECURITY ISSUE: Logging secrets
  initializeDatabase();
});

// QUALITY ISSUE: No module exports for testing
module.exports = { AuthService, app };
