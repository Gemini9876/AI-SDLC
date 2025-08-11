-- FILE: frontend/src/App.js --
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';

/**
 * Main application component responsible for routing.
 */
function App() {
  // In a real application, you would manage authentication state (e.g., using Context API or Redux)
  // For this demo, we'll simulate a redirect to Dashboard upon successful login,
  // but there's no persistent authentication state managed here.
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Default route redirects to Login Page */}
          <Route path="/" element={<Navigate to="/login" />} />
          {/* Login Page Route */}
          <Route path="/login" element={<LoginPage />} />
          {/* Dashboard Page Route - protected in a real app */}
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

-- FILE: frontend/src/api/auth.js --
/**
 * API client for authentication related requests.
 */

const API_BASE_URL = 'http://localhost:5000/api'; // Backend URL

/**
 * Attempts to log in a user with provided credentials.
 * @param {string} username - The user's username.
 * @param {string} password - The user's password.
 * @returns {Promise<Object>} A promise that resolves with the login response or rejects with an error.
 */
export const login = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    // Ensure secure transmission over HTTPS is handled by the server environment (e.g., Nginx, cloud load balancer)
    // The fetch API itself will respect the protocol of the URL.

    const data = await response.json();

    if (!response.ok) {
      // Handle HTTP errors (e.g., 400, 401, 403)
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }

    return data; // Contains success message or token
  } catch (error) {
    console.error('Login API error:', error);
    throw error; // Re-throw to be caught by the component
  }
};

-- FILE: frontend/src/components/Dashboard.js --
import React from 'react';

/**
 * A simple placeholder for the secure dashboard page.
 * In a real application, this would contain user-specific features.
 */
const Dashboard = () => {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Welcome to Your Secure Dashboard!</h1>
      <p>This is a placeholder for your personalized content.</p>
      <p>You have successfully logged in.</p>
      {/* In a real app, you might have a logout button here */}
      <button onClick={() => alert('Logging out is not implemented in this demo.')}>
        Logout
      </button>
    </div>
  );
};

export default Dashboard;

-- FILE: frontend/src/components/LoginPage.js --
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';
import appLogo from '../assets/app_logo.svg'; // Assuming these SVGs exist in src/assets
import loginArrow from '../assets/login_arrow.svg'; // Assuming these SVGs exist in src/assets
import '../styles/LoginPage.css'; // Assuming you create this CSS file

// Mock translations for language selection (simulating Contentful integration)
const translations = {
  en: {
    welcomeBack: 'Welcome Back!',
    username: 'Username',
    password: 'Password',
    login: 'Login',
    forgotPassword: 'Forgot Password?',
    usernameRequired: 'Username is required.',
    passwordRequired: 'Password is required.',
    invalidCredentials: 'Invalid username or password. Please try again or click \'Forgot Password?\' if you need to reset it.',
    selectLanguage: 'Select Language',
    applicationLogoAlt: 'Application logo',
    loginButtonAlt: 'Login, press to access your account',
  },
  es: {
    welcomeBack: '¡Bienvenido de nuevo!',
    username: 'Nombre de usuario',
    password: 'Contraseña',
    login: 'Iniciar sesión',
    forgotPassword: '¿Olvidaste tu contraseña?',
    usernameRequired: 'El nombre de usuario es obligatorio.',
    passwordRequired: 'La contraseña es obligatoria.',
    invalidCredentials: 'Usuario o contraseña inválidos. Por favor, inténtelo de nuevo o haga clic en \'¿Olvidaste tu contraseña?\' si necesita restablecerla.',
    selectLanguage: 'Seleccionar idioma',
    applicationLogoAlt: 'Logotipo de la aplicación',
    loginButtonAlt: 'Iniciar sesión, presione para acceder a su cuenta',
  },
  fr: {
    welcomeBack: 'Bienvenue !',
    username: 'Nom d\'utilisateur',
    password: 'Mot de passe',
    login: 'Connexion',
    forgotPassword: 'Mot de passe oublié ?',
    usernameRequired: 'Le nom d\'utilisateur est requis.',
    passwordRequired: 'Le mot de passe est requis.',
    invalidCredentials: 'Nom d\'utilisateur ou mot de passe invalide. Veuillez réessayer ou cliquer sur \'Mot de passe oublié ?\' si vous avez besoin de le réinitialiser.',
    selectLanguage: 'Sélectionner la langue',
    applicationLogoAlt: 'Logo de l\'application',
    loginButtonAlt: 'Connexion, appuyez pour accéder à votre compte',
  },
};

/**
 * LoginPage component for user authentication.
 */
const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [loginError, setLoginError] = useState('');
  const [language, setLanguage] = useState('en'); // Default language
  const navigate = useNavigate();

  const t = translations[language]; // Current translation object

  // Scenario: Login Page Load Performance
  // The useEffect with a timer here simulates the interactive within X seconds.
  // Actual performance testing would use tools like Lighthouse, Playwright.
  useEffect(() => {
    const pageLoadStartTime = performance.now();
    const checkInteractive = () => {
      const interactiveTime = performance.now();
      const loadTime = interactiveTime - pageLoadStartTime;
      console.log(`Login page fully rendered within ${loadTime.toFixed(2)} ms.`);
      if (loadTime > 2000) {
        console.warn(`Warning: Login page rendered in ${loadTime.toFixed(2)} ms, exceeding 2 seconds.`);
      }

      // Simulate interactivity check
      const focusableElements = document.querySelectorAll('input, button, a, select');
      if (focusableElements.length > 0) {
        // If elements are present and clickable, consider interactive
        const interactiveDuration = performance.now() - pageLoadStartTime;
        console.log(`Login page interactive within ${interactiveDuration.toFixed(2)} ms.`);
        if (interactiveDuration > 3000) {
          console.warn(`Warning: Login page became interactive in ${interactiveDuration.toFixed(2)} ms, exceeding 3 seconds.`);
        }
      } else {
        // Retry check if elements aren't ready
        setTimeout(checkInteractive, 100);
      }
    };

    const timeoutId = setTimeout(checkInteractive, 100); // Give a small delay for render

    return () => clearTimeout(timeoutId); // Cleanup
  }, []);


  /**
   * Handles form submission for login.
   * Includes client-side validation and API call.
   */
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    setUsernameError('');
    setPasswordError('');

    let isValid = true;
    if (!username) {
      setUsernameError(t.usernameRequired);
      isValid = false;
    }
    if (!password) {
      setPasswordError(t.passwordRequired);
      isValid = false;
    }

    if (!isValid) {
      // Scenario: Unsuccessful User Login with Empty Required Fields
      return; // Stop if validation fails
    }

    // Scenario: API Login Response Performance & Secure Password Input/Transmission
    const apiCallStartTime = performance.now();
    try {
      const response = await login(username, password);

      const apiCallEndTime = performance.now();
      const apiResponseTime = apiCallEndTime - apiCallStartTime;
      console.log(`API response received in ${apiResponseTime.toFixed(2)} ms.`);
      if (apiResponseTime > 1500) {
        console.warn(`Warning: API response time was ${apiResponseTime.toFixed(2)} ms, exceeding 1.5 seconds.`);
      }

      // Scenario: Successful User Login with Valid Credentials
      console.log('Login successful:', response.message);
      // Simulate redirection to dashboard after a short delay to account for UI transition
      setTimeout(() => {
        navigate('/dashboard'); // Redirect to dashboard
      }, Math.max(0, 2000 - apiResponseTime)); // Ensure total time from click to redirect is max 2 seconds

    } catch (error) {
      // Scenario: Unsuccessful User Login with Invalid Credentials
      // Scenario: Clear Error Messaging for Login Failures
      const errorMessage = error.message || 'An unexpected error occurred. Please try again.';
      setLoginError(errorMessage);
      console.error('Login failed:', errorMessage);
    }
  };

  /**
   * Handles language selection change.
   * @param {Object} e - The event object from the select element.
   */
  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  return (
    <div className="login-page">
      <section className="login-page__section-one">
        {/* Scenario: Comprehensive ALT Text for Visual Elements */}
        {/* Scenario: Successful User Login with Valid Credentials - app_logo.svg displayed */}
        <img
          src={appLogo}
          alt={t.applicationLogoAlt}
          className="app-logo"
          id="loginPage.sectionOne.fieldOne"
        />
        {/* Scenario: Successful Login - Welcome Back! message */}
        <h2 className="welcome-message" id="loginPage.sectionOne.fieldTwo">{t.welcomeBack}</h2>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">{t.username}</label>
            <input
              type="text"
              id="username"
              className="form-control"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value);
                setUsernameError(''); // Clear error on input
              }}
              aria-describedby={usernameError ? "username-error" : null}
              aria-invalid={!!usernameError}
              // Scenario: Logical Tab Order Navigation - 1st element
              tabIndex="1"
              data-testid="username-input"
              id="loginPage.sectionOne.fieldThree"
            />
            {usernameError && <p id="username-error" className="error-message">{usernameError}</p>}
          </div>

          <div className="form-group">
            <label htmlFor="password">{t.password}</label>
            <input
              type="password" {/* Scenario: Secure Password Input and Transmission (masked) */}
              id="password"
              className="form-control"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setPasswordError(''); // Clear error on input
                setLoginError(''); // Clear login error on password change
              }}
              aria-describedby={passwordError ? "password-error" : null}
              aria-invalid={!!passwordError}
              // Scenario: Logical Tab Order Navigation - 2nd element
              tabIndex="2"
              data-testid="password-input"
              id="loginPage.sectionOne.fieldFour"
            />
            {passwordError && <p id="password-error" className="error-message">{passwordError}</p>}
          </div>

          {loginError && <p className="error-message login-error" role="alert">{loginError}</p>}

          <section className="login-page__section-two">
            <button
              type="submit"
              className="login-button"
              // Scenario: Logical Tab Order Navigation - 3rd element
              tabIndex="3"
              data-testid="login-button"
              id="loginPage.sectionTwo.fieldTwo"
            >
              {/* Scenario: Comprehensive ALT Text for Visual Elements - Login button with icon */}
              <img
                src={loginArrow}
                alt="" // Decorative icon, alt can be empty if button text explains purpose
                className="login-arrow-icon"
                id="loginPage.sectionTwo.fieldOne"
              />
              {t.login}
            </button>

            <a
              href="/forgot-password"
              className="forgot-password-link"
              // Scenario: Logical Tab Order Navigation - 4th element
              tabIndex="4"
              data-testid="forgot-password-link"
              id="loginPage.sectionTwo.fieldThree"
            >
              {t.forgotPassword}
            </a>

            {/* Scenario: Language Selection Functionality */}
            <div className="language-selector">
              <label htmlFor="language-select" className="sr-only">{t.selectLanguage}</label>
              <select
                id="language-select"
                value={language}
                onChange={handleLanguageChange}
                // Scenario: Logical Tab Order Navigation - 5th element
                tabIndex="5"
                data-testid="language-select"
                id="loginPage.sectionTwo.fieldFour"
              >
                <option value="en" id="loginPage.sectionTwo.fieldFour.dropDownOption1">English</option>
                <option value="es" id="loginPage.sectionTwo.fieldFour.dropDownOption2">Español</option>
                <option value="fr" id="loginPage.sectionTwo.fieldFour.dropDownOption3">Français</option>
              </select>
            </div>
          </section>
        </form>
      </section>
    </div>
  );
};

export default LoginPage;

-- FILE: frontend/src/styles/LoginPage.css --
/* General styles for the login page container */
.login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f0f2f5;
    font-family: Arial, sans-serif;
    padding: 20px;
    box-sizing: border-box;
}

/* Styling for the main login section */
.login-page__section-one {
    background: #fff;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* App logo styling */
.app-logo {
    max-width: 120px;
    height: auto;
    margin: 0 auto 10px;
}

/* Welcome message styling */
.welcome-message {
    color: #333;
    font-size: 24px;
    margin-bottom: 20px;
}

/* Form group for inputs */
.form-group {
    margin-bottom: 15px;
    text-align: left;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #555;
    font-weight: bold;
}

.form-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    box-sizing: border-box; /* Ensures padding doesn't increase width */
}

.form-group input:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

/* Error messages */
.error-message {
    color: #dc3545;
    font-size: 14px;
    margin-top: 5px;
    text-align: left;
}

.login-error {
    text-align: center;
    margin-bottom: 15px;
}

/* Login button section */
.login-page__section-two {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin-top: 20px;
}

/* Login button styling */
.login-button {
    width: 100%;
    padding: 12px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    transition: background-color 0.3s ease;
}

.login-button:hover {
    background-color: #0056b3;
}

.login-button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5);
}

.login-arrow-icon {
    width: 20px;
    height: 20px;
    filter: invert(100%); /* Make SVG white if it's black */
}

/* Forgot password link */
.forgot-password-link {
    color: #007bff;
    text-decoration: none;
    font-size: 14px;
    transition: color 0.3s ease;
}

.forgot-password-link:hover {
    color: #0056b3;
    text-decoration: underline;
}

/* Language selector */
.language-selector {
    margin-top: 20px;
}

.language-selector select {
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
    background-color: #f9f9f9;
    cursor: pointer;
}

.language-selector select:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

/* Screen reader only class for accessibility */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}

/* Basic responsiveness */
@media (max-width: 600px) {
    .login-page__section-one {
        padding: 30px;
        margin: 20px;
    }
}

-- FILE: backend/app.py --
import os
import datetime
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config.Config')

# Enable CORS for cross-origin requests from the frontend
CORS(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# In-memory user store (for demo purposes)
# In a real application, this would be a database.
users = {
    "testuser": {
        "password_hash": bcrypt.generate_password_hash("password123").decode('utf-8'),
        "email": "testuser@example.com"
    },
    "anotheruser": {
        "password_hash": bcrypt.generate_password_hash("securepass").decode('utf-8'),
        "email": "anotheruser@example.com"
    }
}

# In-memory store for login attempts (for brute-force protection)
# In a real application, this would be a persistent store like Redis or database.
login_attempts = {} # {username: {'count': int, 'timestamp': datetime, 'locked_until': datetime}}

@app.route('/api/login', methods=['POST'])
def login():
    """
    Handles user login requests.
    Validates credentials, implements brute-force protection, and returns a success/error message.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Basic input validation
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    user_info = users.get(username)
    current_time = datetime.datetime.now()

    # Scenario: Protection Against Brute-Force Attacks
    if username in login_attempts:
        attempt_info = login_attempts[username]
        # Check if account is currently locked
        if attempt_info.get('locked_until') and attempt_info['locked_until'] > current_time:
            # Send email notification about lockout attempt (mocked)
            print(f"EMAIL NOTIFICATION: Brute-force attempt on account {username}. Account locked until {attempt_info['locked_until']}.")
            return jsonify({"message": f"Account locked due to too many failed attempts. Try again after {attempt_info['locked_until'].strftime('%H:%M:%S')}."}), 403

        # Reset count if last attempt was outside the observation window
        if current_time - attempt_info['timestamp'] > datetime.timedelta(minutes=app.config['BRUTE_FORCE_WINDOW_MINUTES']):
            login_attempts[username] = {'count': 0, 'timestamp': current_time}

    # Verify credentials
    if user_info and bcrypt.check_password_hash(user_info['password_hash'], password):
        # Successful login: reset attempts for this user
        if username in login_attempts:
            del login_attempts[username]
        return jsonify({"message": "Login successful!", "user": username}), 200
    else:
        # Invalid credentials: Increment login attempts
        attempt_info = login_attempts.get(username, {'count': 0, 'timestamp': current_time})
        attempt_info['count'] += 1
        attempt_info['timestamp'] = current_time

        if attempt_info['count'] >= app.config['BRUTE_FORCE_MAX_ATTEMPTS']:
            lockout_time = current_time + datetime.timedelta(minutes=app.config['BRUTE_FORCE_LOCKOUT_MINUTES'])
            attempt_info['locked_until'] = lockout_time
            # Scenario: Protection Against Brute-Force Attacks - email notification
            # In a real app, this would trigger an actual email service
            print(f"EMAIL NOTIFICATION: Account {username} locked due to 5 consecutive invalid login attempts. Locked until {lockout_time}.")
            return jsonify({"message": "Invalid username or password. Account temporarily locked due to too many failed attempts."}), 401 # Use 401 for generic invalid credentials, 403 when locked
        else:
            login_attempts[username] = attempt_info
            # Scenario: Clear Error Messaging for Login Failures
            return jsonify({"message": "Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it."}), 401

# The following lines are for development purposes to run the server directly.
# In production, use a WSGI server like Gunicorn/uWSGI.
if __name__ == '__main__':
    # Ensure a SECRET_KEY is set for production (e.g., for sessions or JWTs, though not used here)
    if not app.config.get('SECRET_KEY'):
        print("WARNING: SECRET_KEY is not set. Using a default for development.")
        app.config['SECRET_KEY'] = 'a_super_secret_key_for_dev_only'

    app.run(debug=True) # debug=True is for development, set to False in production

-- FILE: backend/config.py --
import os

class Config:
    """
    Application configuration class.
    """
    # Flask secret key for session management, CSRF protection, etc.
    # IMPORTANT: Change this to a strong, randomly generated key in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_super_secret_key_please_change'

    # Brute-force protection settings
    BRUTE_FORCE_MAX_ATTEMPTS = 5 # Number of failed attempts before lockout
    BRUTE_FORCE_LOCKOUT_MINUTES = 15 # Duration of lockout in minutes
    BRUTE_FORCE_WINDOW_MINUTES = 5 # Window to count attempts in minutes

    # Database configuration (example, not used in this in-memory demo)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other configurations can be added here (e.g., mail server, logging)

-- FILE: tests/test_backend.py --
import pytest
import datetime
from flask import Flask
from flask.testing import FlaskClient
from flask_bcrypt import Bcrypt
import sys
import os

# Add the backend directory to the sys.path to allow importing app and config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app import app as flask_app, bcrypt, users, login_attempts

@pytest.fixture
def client():
    """
    Configures the Flask app for testing and provides a test client.
    """
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test_secret_key' # Override secret key for tests
    flask_app.config['BRUTE_FORCE_MAX_ATTEMPTS'] = 3 # Lower for easier testing
    flask_app.config['BRUTE_FORCE_LOCKOUT_MINUTES'] = 1 # Lower for easier testing
    flask_app.config['BRUTE_FORCE_WINDOW_MINUTES'] = 1 # Lower for easier testing

    with flask_app.test_client() as client:
        # Clear users and login_attempts for each test to ensure isolation
        users.clear()
        users["testuser"] = {
            "password_hash": bcrypt.generate_password_hash("password123").decode('utf-8'),
            "email": "testuser@example.com"
        }
        users["lockeduser"] = {
            "password_hash": bcrypt.generate_password_hash("lockedpass").decode('utf-8'),
            "email": "lockeduser@example.com"
        }
        login_attempts.clear()
        yield client

def test_successful_login(client: FlaskClient):
    """
    Test case for successful login with valid credentials.
    Scenario: Successful User Login with Valid Credentials
    """
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful!'
    assert 'testuser' not in login_attempts # Ensure attempts are cleared on success

def test_unsuccessful_login_invalid_credentials(client: FlaskClient):
    """
    Test case for unsuccessful login with invalid credentials.
    Scenario: Unsuccessful User Login with Invalid Credentials
    """
    response = client.post('/api/login', json={
        'username': 'invaliduser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['message'] == "Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it."
    assert 'invaliduser' in login_attempts
    assert login_attempts['invaliduser']['count'] == 1

def test_unsuccessful_login_empty_fields(client: FlaskClient):
    """
    Test case for unsuccessful login with empty required fields.
    Scenario: Unsuccessful User Login with Empty Required Fields
    """
    # Test with empty username
    response_no_user = client.post('/api/login', json={
        'username': '',
        'password': 'password123'
    })
    assert response_no_user.status_code == 400
    assert response_no_user.json['message'] == 'Username and password are required.'

    # Test with empty password
    response_no_pass = client.post('/api/login', json={
        'username': 'testuser',
        'password': ''
    })
    assert response_no_pass.status_code == 400
    assert response_no_pass.json['message'] == 'Username and password are required.'

    # Test with both empty
    response_both_empty = client.post('/api/login', json={
        'username': '',
        'password': ''
    })
    assert response_both_empty.status_code == 400
    assert response_both_empty.json['message'] == 'Username and password are required.'

def test_brute_force_protection(client: FlaskClient):
    """
    Test case for brute-force attack protection.
    Scenario: Protection Against Brute-Force Attacks
    """
    test_username = 'testuser'
    wrong_password = 'wrongpassword'
    max_attempts = flask_app.config['BRUTE_FORCE_MAX_ATTEMPTS']

    # Make failed login attempts until lockout threshold is met
    for i in range(max_attempts - 1):
        response = client.post('/api/login', json={
            'username': test_username,
            'password': wrong_password
        })
        assert response.status_code == 401
        assert test_username in login_attempts
        assert login_attempts[test_username]['count'] == (i + 1)
        # Ensure account is not yet locked
        assert 'locked_until' not in login_attempts[test_username] or login_attempts[test_username]['locked_until'] <= datetime.datetime.now()

    # The next attempt should trigger the lockout
    response_lockout = client.post('/api/login', json={
        'username': test_username,
        'password': wrong_password
    })
    assert response_lockout.status_code == 401 # The original code returns 401 before lockout and 403 on locked.
                                              # Adjusting to 401 as per the current app.py logic which
                                              # returns 401 with a message indicating lockout for the *triggering* attempt.
    assert test_username in login_attempts
    assert login_attempts[test_username]['count'] == max_attempts
    assert 'locked_until' in login_attempts[test_username]
    assert login_attempts[test_username]['locked_until'] > datetime.datetime.now()

    # Try to login again while account is locked
    response_after_lockout = client.post('/api/login', json={
        'username': test_username,
        'password': wrong_password
    })
    assert response_after_lockout.status_code == 403
    assert "Account locked due to too many failed attempts." in response_after_lockout.json['message']

    # Simulate passing the lockout time
    original_locked_until = login_attempts[test_username]['locked_until']
    # Manually advance the lockout time to be in the past
    login_attempts[test_username]['locked_until'] = datetime.datetime.now() - datetime.timedelta(minutes=1)

    # Now, a correct login attempt should succeed, and attempts should be reset
    response_success_after_lockout = client.post('/api/login', json={
        'username': test_username,
        'password': 'password123'
    })
    assert response_success_after_lockout.status_code == 200
    assert response_success_after_lockout.json['message'] == "Login successful!"
    assert test_username not in login_attempts # Attempts cleared after successful login

def test_login_attempts_window(client: FlaskClient):
    """
    Test that login attempts are reset if enough time passes.
    """
    test_username = 'brutewindowuser'
    users[test_username] = {
        "password_hash": bcrypt.generate_password_hash("windowpass").decode('utf-8'),
        "email": "windowuser@example.com"
    }

    # Make one failed attempt
    client.post('/api/login', json={
        'username': test_username,
        'password': 'wrongpass'
    })
    assert login_attempts[test_username]['count'] == 1

    # Simulate time passing beyond the window
    login_attempts[test_username]['timestamp'] = datetime.datetime.now() - datetime.timedelta(minutes=flask_app.config['BRUTE_FORCE_WINDOW_MINUTES'] + 1)

    # Make another failed attempt - count should reset
    client.post('/api/login', json={
        'username': test_username,
        'password': 'wrongpass'
    })
    assert login_attempts[test_username]['count'] == 1 # Should be reset to 1

    # And then a successful login should still work
    response = client.post('/api/login', json={
        'username': test_username,
        'password': 'windowpass'
    })
    assert response.status_code == 200
    assert test_username not in login_attempts

def test_clear_error_messaging_for_login_failures(client: FlaskClient):
    """
    Test for clear, concise, and actionable error messages when login fails.
    Scenario: Clear Error Messaging for Login Failures
    """
    response = client.post('/api/login', json={
        'username': 'nonexistent',
        'password': 'anypass'
    })
    assert response.status_code == 401
    expected_message = "Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it."
    assert response.json['message'] == expected_message