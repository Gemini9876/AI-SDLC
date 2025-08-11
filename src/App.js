import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';

function App() {
  // In a real app, this would be managed by global state (e.g., Context API, Redux)
  // For this example, we'll simulate a 'logged in' state for redirection.
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    // Simulate redirection delay as per Gherkin scenario
    setTimeout(() => {
      console.log("Redirecting to dashboard...");
      // In a real app, navigate('/dashboard'); would happen here
    }, 2000);
  };

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={isLoggedIn ? <Navigate to="/dashboard" /> : <LoginPage onLoginSuccess={handleLoginSuccess} />} />
        <Route path="/dashboard" element={<h2>Welcome to your Dashboard! (Logged In)</h2>} />
        {/* Add more routes as needed */}
      </Routes>
    </div>
  );
}

export default App;
