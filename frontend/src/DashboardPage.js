import React from 'react';
import './DashboardPage.css';

const DashboardPage = () => {
  return (
    <div className="dashboard-page">
      <h2>Welcome to Your Secure Dashboard!</h2>
      <p>You have successfully logged in.</p>
      <p>This is where your personalized content would appear.</p>
      {/* In a real app, you might have a logout button here */}
    </div>
  );
};

export default DashboardPage;
