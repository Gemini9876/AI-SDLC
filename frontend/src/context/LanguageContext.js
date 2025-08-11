import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

// Mock translations (in a real app, fetched from Contentful/i18n solution)
const MOCK_TRANSLATIONS = {
  en: {
    'loginPage.sectionOne.fieldTwo': 'Welcome Back!',
    'loginPage.sectionOne.fieldThree': 'Username',
    'loginPage.sectionOne.fieldFour': 'Password',
    'loginPage.sectionTwo.fieldTwo': 'Login',
    'loginPage.sectionTwo.fieldThree': 'Forgot Password?',
    'loginPage.sectionTwo.fieldThreeSuffix': 'if you need to reset it.',
    'loginPage.sectionTwo.fieldFour.dropDownOption1': 'English',
    'loginPage.sectionTwo.fieldFour.dropDownOption2': 'Español',
    'loginPage.sectionTwo.fieldFour.dropDownOption3': 'Français',
    'loginPage.sectionOne.fieldOneAlt': 'Application logo',
    'loginPage.sectionTwo.fieldOneAlt': 'Login arrow icon',
    'loginPage.languageLabel': 'Language',
    'loginPage.validation.usernameRequired': 'Username is required.',
    'loginPage.validation.passwordRequired': 'Password is required.',
    'loginPage.error.invalidCredentials': 'Invalid username or password. Please try again or click \'Forgot Password?\' if you need to reset it.'
  },
  es: {
    'loginPage.sectionOne.fieldTwo': '¡Bienvenido de Nuevo!',
    'loginPage.sectionOne.fieldThree': 'Nombre de Usuario',
    'loginPage.sectionOne.fieldFour': 'Contraseña',
    'loginPage.sectionTwo.fieldTwo': 'Iniciar Sesión',
    'loginPage.sectionTwo.fieldThree': '¿Olvidaste tu Contraseña?',
    'loginPage.sectionTwo.fieldThreeSuffix': 'si necesitas restablecerla.',
    'loginPage.sectionTwo.fieldFour.dropDownOption1': 'Inglés',
    'loginPage.sectionTwo.fieldFour.dropDownOption2': 'Español',
    'loginPage.sectionTwo.fieldFour.dropDownOption3': 'Francés',
    'loginPage.sectionOne.fieldOneAlt': 'Logotipo de la aplicación',
    'loginPage.sectionTwo.fieldOneAlt': 'Icono de flecha de inicio de sesión',
    'loginPage.languageLabel': 'Idioma',
    'loginPage.validation.usernameRequired': 'El nombre de usuario es obligatorio.',
    'loginPage.validation.passwordRequired': 'La contraseña es obligatoria.',
    'loginPage.error.invalidCredentials': 'Nombre de usuario o contraseña inválidos. Inténtalo de nuevo o haz clic en \'¿Olvidaste tu Contraseña?\' si necesitas restablecerla.'
  },
  fr: {
    'loginPage.sectionOne.fieldTwo': 'Bienvenue !',
    'loginPage.sectionOne.fieldThree': 'Nom d\'utilisateur',
    'loginPage.sectionOne.fieldFour': 'Mot de passe',
    'loginPage.sectionTwo.fieldTwo': 'Se connecter',
    'loginPage.sectionTwo.fieldThree': 'Mot de passe oublié ?',
    'loginPage.sectionTwo.fieldThreeSuffix': 'si vous devez le réinitialiser.',
    'loginPage.sectionTwo.fieldFour.dropDownOption1': 'Anglais',
    'loginPage.sectionTwo.fieldFour.dropDownOption2': 'Espagnol',
    'loginPage.sectionTwo.fieldFour.dropDownOption3': 'Français',
    'loginPage.sectionOne.fieldOneAlt': 'Logo de l\'application',
    'loginPage.sectionTwo.fieldOneAlt': 'Icône de flèche de connexion',
    'loginPage.languageLabel': 'Langue',
    'loginPage.validation.usernameRequired': 'Le nom d\'utilisateur est requis.',
    'loginPage.validation.passwordRequired': 'Le mot de passe est requis.',
    'loginPage.error.invalidCredentials': 'Nom d\'utilisateur ou mot de passe invalide. Veuillez réessayer ou cliquer sur \'Mot de passe oublié ?\' si vous devez le réinitialiser.'
  }
};

export const LanguageProvider = ({ children }) => {
  const [selectedLanguage, setSelectedLanguage] = useState('en');

  useEffect(() => {
    // Load language from localStorage or default to 'en'
    const storedLang = localStorage.getItem('appLanguage');
    if (storedLang && MOCK_TRANSLATIONS[storedLang]) {
      setSelectedLanguage(storedLang);
    }
  }, []);

  const setLanguage = (lang) => {
    if (MOCK_TRANSLATIONS[lang]) {
      setSelectedLanguage(lang);
      localStorage.setItem('appLanguage', lang);
    } else {
      console.warn(`Language '${lang}' not supported.`);
    }
  };

  return (
    <LanguageContext.Provider value={{ selectedLanguage, setLanguage, translations: MOCK_TRANSLATIONS }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
