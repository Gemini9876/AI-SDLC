require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const rateLimit = require('express-rate-limit');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// --- Middleware ---
app.use(cors()); // Allow cross-origin requests for development
app.use(express.json()); // Body parser for JSON requests

// --- In-memory 'Database' (for demonstration purposes) ---
const users = {
  'testuser': { passwordHash: bcrypt.hashSync('password123', 10) }
};

// Track failed login attempts for brute-force protection
const loginAttempts = new Map(); // Stores { username: { count: N, lastAttempt: Date, lockedUntil: Date } }
const MAX_ATTEMPTS = 5;
const LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutes
const RESET_ATTEMPTS_TIME_MS = 5 * 60 * 1000; // 5 minutes

// Helper to manage login attempts
const recordFailedAttempt = (username) => {
  const now = Date.now();
  if (!loginAttempts.has(username)) {
    loginAttempts.set(username, { count: 0, lastAttempt: now, lockedUntil: null });
  }

  const attemptData = loginAttempts.get(username);
  
  // Reset count if last attempt was too long ago
  if (now - attemptData.lastAttempt > RESET_ATTEMPTS_TIME_MS) {
    attemptData.count = 0;
  }

  attemptData.count++;
  attemptData.lastAttempt = now;

  if (attemptData.count >= MAX_ATTEMPTS) {
    attemptData.lockedUntil = new Date(now + LOCKOUT_DURATION_MS);
    // In a real app, send an email notification here:
    console.log(`[SECURITY ALERT] Account '${username}' locked due to ${MAX_ATTEMPTS} failed attempts.`);
    // sendEmailNotification(username, 'Account Locked');
  }
  loginAttempts.set(username, attemptData);
};

const checkAccountLockout = (username) => {
  const attemptData = loginAttempts.get(username);
  if (attemptData && attemptData.lockedUntil && attemptData.lockedUntil > new Date()) {
    return true; // Account is locked
  }
  return false; // Account is not locked
};

const resetLoginAttempts = (username) => {
  if (loginAttempts.has(username)) {
    loginAttempts.set(username, { count: 0, lastAttempt: Date.now(), lockedUntil: null });
  }
};

// --- API Routes ---

// Login endpoint
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  // Simulate API response delay for performance testing scenario
  setTimeout(() => {
    if (!username || !password) {
      return res.status(400).json({ success: false, message: 'Username and password are required.' });
    }

    if (checkAccountLockout(username)) {
      const lockedUntil = loginAttempts.get(username).lockedUntil;
      return res.status(403).json({
        success: false,
        message: `Account is temporarily locked. Please try again after ${lockedUntil.toLocaleTimeString()}.`
      });
    }

    const user = users[username];

    if (user && bcrypt.compareSync(password, user.passwordHash)) {
      // Successful login
      resetLoginAttempts(username); // Reset attempts on success
      return res.json({ success: true, message: 'Login successful!', token: 'mock-jwt-token' });
    } else {
      // Invalid credentials
      recordFailedAttempt(username);
      let errorMessage = 'Invalid username or password. Please try again.';
      if (checkAccountLockout(username)) {
         errorMessage = 'Invalid username or password. Account is now locked due to multiple failed attempts. Please try again later.';
      }
      // Clearer message for invalid credentials as per Gherkin scenario
      if (!checkAccountLockout(username)) {
        errorMessage = "Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it.";
      }
      return res.status(401).json({ success: false, message: errorMessage });
    }
  }, 500); // Simulate 500ms API response time
});

// Serve static files from the React app (frontend build)
// In production, the React app will be built into the 'build' folder.
app.use(express.static(path.join(__dirname, '..', 'build')));

// All other GET requests not handled by the API should return the React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'build', 'index.html'));
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Access backend API at http://localhost:${PORT}/api/login`);
  console.log(`Access frontend at http://localhost:${PORT}`);
  // Note: For production, ensure HTTPS (TLS 1.2+) is configured at the server/proxy level (e.g., Nginx, AWS ELB).
});
