import React, { useState, useEffect } from 'react';
import { loginPageData } from '../utils/uiData';

// Simulate Contentful translations
const translations = {
  'en': {
    'welcomeBack': loginPageData.loginPage.sectionOne.fieldTwo,
    'username': loginPageData.loginPage.sectionOne.fieldThree,
    'password': loginPageData.loginPage.sectionOne.fieldFour,
    'login': loginPageData.loginPage.sectionTwo.fieldTwo,
    'forgotPassword': loginPageData.loginPage.sectionTwo.fieldThree,
    'invalidCredentials': "Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it.",
    'usernameRequired': "Username is required.",
    'passwordRequired': "Password is required."
  },
  'es': {
    'welcomeBack': "¡Bienvenido de Nuevo!",
    'username': "Nombre de Usuario",
    'password': "Contraseña",
    'login': "Iniciar Sesión",
    'forgotPassword': "¿Olvidaste tu Contraseña?",
    'invalidCredentials': "Nombre de usuario o contraseña inválidos. Por favor, inténtelo de nuevo o haga clic en '¿Olvidaste tu Contraseña?' si necesita restablecerla.",
    'usernameRequired': "El nombre de usuario es requerido.",
    'passwordRequired': "La contraseña es requerida."
  },
  'fr': {
    'welcomeBack': "Bienvenue de Nouveau !",
    'username': "Nom d'utilisateur",
    'password': "Mot de passe",
    'login': "Connexion",
    'forgotPassword': "Mot de passe oublié ?",
    'invalidCredentials': "Nom d'utilisateur ou mot de passe invalide. Veuillez réessayer ou cliquer sur 'Mot de passe oublié ?' si vous devez le réinitialiser.",
    'usernameRequired': "Le nom d'utilisateur est requis.",
    'passwordRequired': "Le mot de passe est requis."
  }
};

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState({});
  const [language, setLanguage] = useState('en');

  const currentTranslations = translations[language];

  useEffect(() => {
    // This effect is for the 'Login Page Load Performance' scenario.
    // In a real app, you'd monitor actual load times. Here, we simulate initial rendering.
    console.log(`Login page loaded and UI elements rendered at ${new Date().toLocaleTimeString()}`);
    const interactiveTimeout = setTimeout(() => {
      console.log(`Login page interactive at ${new Date().toLocaleTimeString()}`);
    }, 3000); // Simulate interactive within 3 seconds
    return () => clearTimeout(interactiveTimeout);
  }, []);

  const validateForm = () => {
    const errors = {};
    if (!username) {
      errors.username = currentTranslations.usernameRequired;
    }
    if (!password) {
      errors.password = currentTranslations.passwordRequired;
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous API errors
    setValidationErrors({}); // Clear previous validation errors

    if (!validateForm()) {
      // Client-side validation failed (empty fields scenario)
      return;
    }

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (data.success) {
        console.log('Login successful:', data.message);
        onLoginSuccess(); // Trigger success action in App.js
      } else {
        setError(data.message);
        console.error('Login failed:', data.message);
      }
    } catch (err) {
      console.error('Network or server error:', err);
      setError('Could not connect to the server. Please try again later.');
    }
  };

  return (
    <div className="login-page">
      <header className="login-header">
        <img src={loginPageData.loginPage.sectionOne.fieldOne} alt="Application logo" className="app-logo" />
        <h1>{currentTranslations.welcomeBack}</h1>
      </header>

      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">{currentTranslations.username}</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            aria-label={currentTranslations.username}
            autoComplete="username"
            tabIndex="1"
          />
          {validationErrors.username && <span className="error-message">{validationErrors.username}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="password">{currentTranslations.password}</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            aria-label={currentTranslations.password}
            autoComplete="current-password"
            tabIndex="2"
          />
          {validationErrors.password && <span className="error-message">{validationErrors.password}</span>}
          {error && <p className="error-message api-error">{error}</p>} {/* API error message */}
        </div>

        <button type="submit" className="login-button" tabIndex="3">
          <img src={loginPageData.loginPage.sectionTwo.fieldOne} alt="Login arrow icon" className="login-arrow-icon" />
          {currentTranslations.login}
        </button>
      </form>

      <div className="login-footer">
        <a href="#forgot-password" className="forgot-password-link" tabIndex="4">
          {currentTranslations.forgotPassword}
        </a>

        <div className="language-selector" tabIndex="5">
          <label htmlFor="language-dropdown" className="sr-only">Select Language</label>
          <select
            id="language-dropdown"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            aria-label="Language selection dropdown"
          >
            <option value="en">{loginPageData.loginPage.sectionTwo.fieldFour.dropDownOption1}</option>
            <option value="es">{loginPageData.loginPage.sectionTwo.fieldFour.dropDownOption2}</option>
            <option value="fr">{loginPageData.loginPage.sectionTwo.fieldFour.dropDownOption3}</option>
          </select>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
