import React, { useState } from 'react';
import LoginPage from './LoginPage';
import DashboardPage from './DashboardPage';
import './App.css'; // For basic styling, if needed

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // This App component acts as a simple router for demonstration purposes.
  // In a real application, you would use React Router (e.g., react-router-dom).

  return (
    <div className="App">
      {isLoggedIn ? (
        <DashboardPage />
      ) : (
        <LoginPage setIsLoggedIn={setIsLoggedIn} />
      )}
    </div>
  );
}

export default App;
