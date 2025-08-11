import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { fetchDataModel, loginUser } from '../api/api';
import './LoginPage.css'; // For basic styling

const LoginPage = () => {
  const [uiData, setUiData] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [loginError, setLoginError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPageLoading, setIsPageLoading] = useState(true);
  const [loginSuccess, setLoginSuccess] = useState(false);
  const { selectedLanguage, setLanguage, translations } = useLanguage();

  const usernameRef = useRef(null);
  const passwordRef = useRef(null);
  const loginButtonRef = useRef(null);
  const forgotPasswordRef = useRef(null);
  const languageDropdownRef = useRef(null);

  // Scenario: Login Page Load Performance
  useEffect(() => {
    const pageLoadStartTime = performance.now();

    const loadData = async () => {
      // Simulate network delay for page content (e.g., fetching from Contentful)
      await new Promise(resolve => setTimeout(resolve, 100)); 
      const data = fetchDataModel(); // Static mock data
      setUiData(data.loginPage);
      setIsPageLoading(false);
      
      const fullRenderTime = performance.now();
      const renderDuration = fullRenderTime - pageLoadStartTime;
      console.log(`[Perf] Login page fully rendered in ${renderDuration.toFixed(2)} ms.`);
      if (renderDuration > 2000) {
        console.warn(`[Perf Warning] Login page rendering took ${renderDuration.toFixed(2)} ms, exceeding 2000 ms.`);
      }

      // Simulate interactivity delay
      setTimeout(() => {
        console.log(`[Perf] Login page interactive in ${performance.now() - pageLoadStartTime.toFixed(2)} ms.`);
        if ((performance.now() - pageLoadStartTime) > 3000) {
          console.warn(`[Perf Warning] Login page interactivity took ${performance.now() - pageLoadStartTime.toFixed(2)} ms, exceeding 3000 ms.`);
        }
        usernameRef.current?.focus(); // Focus username field on load for accessibility
      }, 300);
    };
    loadData();
  }, []);

  if (isPageLoading || !uiData) {
    return <div className="login-page-loading">Loading Login Page...</div>;
  }

  // Function to get translated text
  const t = (key) => {
    const path = key.split('.');
    let text = uiData;
    for (let i = 0; i < path.length; i++) {
      text = text[path[i]];
      if (text === undefined) return key; // Fallback to key if not found
    }
    // Use explicit translations if available
    return translations[selectedLanguage]?.[key] || text;
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setUsernameError('');
    setPasswordError('');
    setLoginError('');
    setLoginSuccess(false);

    let hasError = false;
    if (!username.trim()) {
      setUsernameError(t('loginPage.validation.usernameRequired'));
      hasError = true;
    }
    if (!password.trim()) {
      setPasswordError(t('loginPage.validation.passwordRequired'));
      hasError = true;
    }

    if (hasError) {
      setIsLoading(false);
      return;
    }

    const loginAttemptStartTime = performance.now();
    try {
      const response = await loginUser(username, password);
      const apiResponseTime = performance.now() - loginAttemptStartTime;
      console.log(`[Perf] API response received in ${apiResponseTime.toFixed(2)} ms.`);
      if (apiResponseTime > 1500) {
        console.warn(`[Perf Warning] API response took ${apiResponseTime.toFixed(2)} ms, exceeding 1500 ms.`);
      }

      if (response.message === 'Login successful') {
        setLoginSuccess(true);
        setLoginError('');
        console.log('Login successful! Redirecting to dashboard...');
        
        // Simulate redirection delay
        setTimeout(() => {
          const totalRedirectTime = performance.now() - loginAttemptStartTime;
          console.log(`[Perf] Redirected to dashboard in ${totalRedirectTime.toFixed(2)} ms.`);
          if (totalRedirectTime > 2000) {
            console.warn(`[Perf Warning] Total redirection time took ${totalRedirectTime.toFixed(2)} ms, exceeding 2000 ms.`);
          }
          // In a real app, this would be: window.location.href = '/dashboard'; or history.push('/dashboard');
          alert('Redirecting to dashboard (simulated)...');
        }, 500); // Simulate a brief client-side redirect delay

      } else {
        setLoginError(response.detail || 'An unexpected error occurred.');
      }
    } catch (error) {
      const apiResponseTime = performance.now() - loginAttemptStartTime;
      console.error('Login error:', error);
      setLoginError(error.message || 'Login failed. Please try again.');
      if (apiResponseTime > 1500) {
        console.warn(`[Perf Warning] API response (error) took ${apiResponseTime.toFixed(2)} ms, exceeding 1500 ms.`);
      }
    }
    setIsLoading(false);
  };

  // Scenario: Logical Tab Order Navigation
  // The natural DOM order provides the specified tab sequence:
  // Username -> Password -> Login Button -> Forgot Password -> Language Dropdown

  return (
    <div className="login-page">
      {loginSuccess && (
        <div className="login-success-overlay">
          <p>Login Successful! Redirecting...</p>
        </div>
      )}
      <div className="login-container">
        <img
          src={t('loginPage.sectionOne.fieldOne')}
          alt={t('loginPage.sectionOne.fieldOneAlt')}
          className="app-logo"
        />
        <h2>{t('loginPage.sectionOne.fieldTwo')}</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">{t('loginPage.sectionOne.fieldThree')}</label>
            <input
              type="text"
              id="username"
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
              ref={usernameRef}
              aria-label={t('loginPage.sectionOne.fieldThree')}
            />
            {usernameError && <p className="error-message">{usernameError}</p>}
          </div>
          <div className="form-group">
            <label htmlFor="password">{t('loginPage.sectionOne.fieldFour')}</label>
            <input
              type="password" // Scenario: Secure Password Input and Transmission (masking)
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              ref={passwordRef}
              aria-label={t('loginPage.sectionOne.fieldFour')}
            />
            {passwordError && <p className="error-message">{passwordError}</p>}
          </div>
          {loginError && (
            <p className="error-message login-error-display">
              {loginError}
              <br />
              {loginError.includes('Invalid') && (
                <span>
                  <a href="#forgot-password" onClick={(e) => e.preventDefault()} tabIndex={0}>
                    {t('loginPage.sectionTwo.fieldThree')}
                  </a>
                  {' '}{t('loginPage.sectionTwo.fieldThreeSuffix')}
                </span>
              )}
            </p>
          )}
          <button type="submit" disabled={isLoading} className="login-button" ref={loginButtonRef}>
            <img
              src={t('loginPage.sectionTwo.fieldOne')}
              alt={t('loginPage.sectionTwo.fieldOneAlt')}
              className="login-arrow-icon"
            />
            {t('loginPage.sectionTwo.fieldTwo')}
          </button>
        </form>
        <a href="#forgot-password" onClick={(e) => e.preventDefault()} className="forgot-password-link" ref={forgotPasswordRef}>
          {t('loginPage.sectionTwo.fieldThree')}
        </a>
        
        {/* Scenario: Language Selection Functionality */}
        <div className="language-selector">
          <label htmlFor="language-select">{t('loginPage.languageLabel')}:</label>
          <select
            id="language-select"
            value={selectedLanguage}
            onChange={(e) => setLanguage(e.target.value)}
            ref={languageDropdownRef}
            aria-label={t('loginPage.languageLabel')}
          >
            <option value="en">{t('loginPage.sectionTwo.fieldFour.dropDownOption1')}</option>
            <option value="es">{t('loginPage.sectionTwo.fieldFour.dropDownOption2')}</option>
            <option value="fr">{t('loginPage.sectionTwo.fieldFour.dropDownOption3')}</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
