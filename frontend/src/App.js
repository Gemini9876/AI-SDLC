import React from 'react';
import LoginPage from './components/LoginPage';
import { LanguageProvider } from './context/LanguageContext';
import './App.css'; // Basic styling

function App() {
  return (
    <LanguageProvider>
      <div className="App">
        <LoginPage />
      </div>
    </LanguageProvider>
  );
}

export default App;
