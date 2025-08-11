// Mock UI Data Model (simulating a fetch from a CMS like Contentful)
const UI_DATA_MODEL = {
  "loginPage": {
    "sectionOne": {
      "fieldOne": "/assets/icons/app_logo.svg",
      "fieldTwo": "Welcome Back!",
      "fieldThree": "Username",
      "fieldFour": "Password"
    },
    "sectionTwo": {
      "fieldOne": "/assets/icons/login_arrow.svg",
      "fieldTwo": "Login",
      "fieldThree": "Forgot Password?",
      "fieldFour": {
        "dropDownOption1": "English",
        "dropDownOption2": "Español",
        "dropDownOption3": "Français"
      }
    }
  }
};

export const fetchDataModel = () => {
  // In a real application, this would be an API call to fetch UI data, e.g.:
  // return fetch('/api/ui-data').then(res => res.json());
  return UI_DATA_MODEL;
};

export const loginUser = async (username, password) => {
  try {
    const response = await fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      // Clear error message from validation errors for general login errors
      const errorMessage = data.detail || 'Login failed. Please try again.';
      if (errorMessage.includes('Invalid username or password')) {
        throw new Error('Invalid username or password. Please try again or click \'Forgot Password?\' if you need to reset it.');
      } else if (errorMessage.includes('Too many failed login attempts')) {
        throw new Error(errorMessage + ' Please try again later.');
      } else if (errorMessage.includes('temporarily locked')) {
        throw new Error(errorMessage);
      }
      throw new Error(errorMessage);
    }

    return data; // Contains message and token on success
  } catch (error) {
    console.error('API Error:', error);
    throw error; // Re-throw to be caught by component
  }
};
