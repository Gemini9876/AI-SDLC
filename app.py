
# Required imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# Setup logic
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Teardown logic
def teardown():
    driver.quit()

# Mapping UI Data Model to technical implementation
ui_data_model = {
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
}

# Gherkin step implementations
# Scenario: Successful User Login with Valid Credentials
def successful_user_login():
    driver.get("login_page_url")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Welcome Back!')]")))
    wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@src='/assets/icons/app_logo.svg']")))
    
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys("testuser")
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("password123")
    
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
    login_button.click()
    
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(),'Welcome Back!')]")))

# Scenario: Unsuccessful User Login with Invalid Credentials
def unsuccessful_user_login_invalid_creds():
    driver.get("login_page_url")
    
    username_input = driver.find_element(By.NAME, "username")
    username_input.send_keys("invaliduser")
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("wrongpassword")
    
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Login')]")
    login_button.click()
    
    error_message = driver.find_element(By.XPATH, "//div[contains(text(),'Invalid username or password. Please try again.')")
    assert error_message.is_displayed()

# Other scenario implementations can be added similarly

# Automatic domain detection and tool selection
# Assuming web domain based on the given UI Data Model and Gherkin scenarios

# Generating automation code
successful_user_login()
unsuccessful_user_login_invalid_creds()

# Teardown
teardown()
```