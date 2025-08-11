import React, { useState } from 'react';
import './LoginPage.css'; // For component-specific styles

// UI Data Model (simulated import or direct inclusion)
const uiDataModel = {
  "loginUIDataModel": {
    "loginFormSection": {
      "fieldOne": "Login to Application",
      "fieldTwo": {
        "label": "Username",
        "placeholder": "Enter your username",
        "type": "text",
        "icon": "/assets/icons/user.svg" // Placeholder path
      },
      "fieldThree": {
        "label": "Password",
        "placeholder": "Enter your password",
        "type": "password",
        "icon": "/assets/icons/lock.svg" // Placeholder path
      },
      "fieldFour": {
        "text": "Login",
        "type": "submit",
        "action": "authenticateUser"
      }
    },
    "utilitySection": {
      "fieldOne": "/assets/images/app_logo.png", // Placeholder path
      "fieldTwo": {
        "text": "Forgot Password?",
        "url": "/forgot-password",
        "type": "link"
      },
      "fieldThree": "© 2023 Your Application Name",
      "fieldFour": {
        "label": "Language",
        "type": "dropdown",
        "options": {
          "dropDownOption1": "English",
          "dropDownOption2": "Spanish",
          "dropDownOption3": "French"
        }
      }
    }
  }
};

const LoginPage = ({ setIsLoggedIn }) => {
  // State for form fields
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // State for validation errors (client-side)
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // State for server-side error messages (e.g., 'Invalid credentials')
  const [errorMessage, setErrorMessage] = useState('');

  // Destructure data model for easier access
  const { loginFormSection, utilitySection } = uiDataModel.loginUIDataModel;

  /**
   * Handles the form submission.
   * Performs client-side validation and then sends credentials to the backend.
   * @param {Event} e - The form submission event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Reset previous errors
    setErrorMessage('');
    setUsernameError('');
    setPasswordError('');

    let isValid = true;

    // Client-side validation for missing fields
    if (!username.trim()) {
      setUsernameError('Username is required.');
      isValid = false;
    }
    if (!password.trim()) {
      setPasswordError('Password is required.');
      isValid = false;
    }

    if (!isValid) {
      return; // Stop if client-side validation fails
    }

    // Attempt to log in via API
    try {
      // Note: Use the backend URL (e.g., http://localhost:8000) not just /api/login
      // In a production environment, this would be a relative path or an environment variable.
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Successful login
        console.log('Login successful:', data.message);
        setIsLoggedIn(true); // Update parent state to redirect to dashboard
      } else {
        // Failed login (e.g., invalid credentials, server-side validation error)
        console.error('Login failed:', data.detail);
        setErrorMessage(data.detail || 'An unexpected error occurred. Please try again.');
      }
    } catch (error) {
      console.error('Network error or API call failed:', error);
      setErrorMessage('Could not connect to the server. Please try again later.');
    }
  };

  return (
    <div className="login-page">
      {/* Accessibility: Performance - Page Load Time:
          The use of React and semantic HTML contributes to a fast loading time.
          Further optimizations (code splitting, lazy loading) can be added for large apps.
          Ensure images and icons are optimized for web (compressed, appropriate formats).
      */}
      <div className="login-container">
        {/* Application Logo - Image Alt Text Requirements */}
        {utilitySection.fieldOne && (
          <img 
            src={utilitySection.fieldOne} 
            alt="Your Application Name Logo" 
            className="app-logo"
          />
        )}

        <h1>{loginFormSection.fieldOne}</h1>

        <form onSubmit={handleSubmit} noValidate>
          {/* Username Field - Accessibility: Logical Tab Order, Image Alt Text */}
          <div className="form-group">
            <label htmlFor="username-input">{loginFormSection.fieldTwo.label}</label>
            <div className="input-with-icon">
              {/* Icon marked as decorative as label conveys meaning */}
              {loginFormSection.fieldTwo.icon && (
                <img 
                  src={loginFormSection.fieldTwo.icon} 
                  alt="" 
                  aria-hidden="true" 
                  className="input-icon"
                />
              )}
              <input
                id="username-input"
                type={loginFormSection.fieldTwo.type}
                placeholder={loginFormSection.fieldTwo.placeholder}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                aria-describedby={usernameError ? "username-error" : undefined}
                aria-invalid={!!usernameError}
              />
            </div>
            {usernameError && (
              <p id="username-error" className="error-message">{usernameError}</p>
            )}
          </div>

          {/* Password Field - Accessibility: Logical Tab Order, Image Alt Text, Secure Password Handling */}
          <div className="form-group">
            <label htmlFor="password-input">{loginFormSection.fieldThree.label}</label>
            <div className="input-with-icon">
              {/* Icon marked as decorative as label conveys meaning */}
              {loginFormSection.fieldThree.icon && (
                <img 
                  src={loginFormSection.fieldThree.icon} 
                  alt="" 
                  aria-hidden="true" 
                  className="input-icon"
                />
              )}
              <input
                id="password-input"
                type={loginFormSection.fieldThree.type}
                placeholder={loginFormSection.fieldThree.placeholder}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                aria-describedby={passwordError ? "password-error" : undefined}
                aria-invalid={!!passwordError}
              />
            </div>
            {passwordError && (
              <p id="password-error" className="error-message">{passwordError}</p>
            )}
          </div>

          {/* Server-side Error Message - Usability: Clear Error Messaging */}
          {errorMessage && (
            <p className="global-error-message" role="alert">{errorMessage}</p>
          )}

          {/* Login Button - Accessibility: Logical Tab Order */}
          <button type={loginFormSection.fieldFour.type} className="login-button">
            {loginFormSection.fieldFour.text}
          </button>
        </form>

        <div className="utility-links">
          {/* Forgot Password Link - Accessibility: Logical Tab Order */}
          {utilitySection.fieldTwo && (
            <a href={utilitySection.fieldTwo.url} className="forgot-password-link">
              {utilitySection.fieldTwo.text}
            </a>
          )}

          {/* Language Dropdown - Accessibility: Logical Tab Order */}
          {utilitySection.fieldFour && utilitySection.fieldFour.type === 'dropdown' && (
            <div className="language-selector">
              <label htmlFor="language-select">{utilitySection.fieldFour.label}: </label>
              <select id="language-select">
                {Object.values(utilitySection.fieldFour.options).map((option, index) => (
                  <option key={index} value={option.toLowerCase()}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Copyright Information */}
        {utilitySection.fieldThree && (
          <p className="copyright">{utilitySection.fieldThree}</p>
        )}
      </div>
    </div>
  );
};

export default LoginPage;
