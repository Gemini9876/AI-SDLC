```python
# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

USERS_FILE = os.path.join(DATA_DIR, 'users.json')
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.json')
FOOD_NUTRITION_FILE = os.path.join(DATA_DIR, 'food_nutrition.json')

```
```python
# auth_manager.py
import json
import os
from config import USERS_FILE

class AuthManager:
    @staticmethod
    def _load_users():
        """Loads user data from the JSON file."""
        if not os.path.exists(USERS_FILE):
            return {}
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} # Return empty if file is malformed

    @staticmethod
    def _save_users(users):
        """Saves user data to the JSON file."""
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)

    def register_user(self, username, password, is_admin=False):
        """
        Registers a new user.
        For a production system, passwords should be hashed (e.g., using bcrypt).
        """
        users = self._load_users()
        if username in users:
            return False, "Username already exists."
        
        users[username] = {
            "password": password, 
            "is_admin": is_admin,
            "usage_limit": -1 if is_admin else 5, # -1 indicates unlimited usage for admins
            "current_usage": 0
        }
        self._save_users(users)
        return True, "Registration successful."

    def login_user(self, username, password):
        """Authenticates a user."""
        users = self._load_users()
        user_data = users.get(username)
        if user_data and user_data["password"] == password:
            return True, "Login successful.", user_data["is_admin"]
        return False, "Invalid username or password.", False

    def get_user_role(self, username):
        """Returns the role of a user (admin or user)."""
        users = self._load_users()
        return 'admin' if users.get(username, {}).get("is_admin") else 'user'

```
```python
# user_manager.py
from auth_manager import AuthManager

class UserManager:
    def __init__(self):
        self.auth_manager = AuthManager()

    def set_usage_limit(self, admin_username, target_username, limit):
        """
        Allows an admin user to set a usage limit for another user.
        -1 means unlimited usage.
        """
        if self.auth_manager.get_user_role(admin_username) != 'admin':
            return False, "Permission denied: Only administrators can set usage limits."

        users = self.auth_manager._load_users()
        if target_username not in users:
            return False, "Target user not found."
        
        try:
            limit = int(limit)
            if limit < -1:
                return False, "Usage limit must be a non-negative integer or -1 for unlimited."
            
            users[target_username]["usage_limit"] = limit
            self.auth_manager._save_users(users)
            return True, f"Usage limit for '{target_username}' set to {limit}."
        except ValueError:
            return False, "Invalid limit. Please enter a number."

    def increment_usage(self, username):
        """Increments the current usage count for a user."""
        users = self.auth_manager._load_users()
        if username in users:
            users[username]["current_usage"] += 1
            self.auth_manager._save_users(users)
            return True
        return False

    def check_usage(self, username):
        """Returns the current usage and usage limit for a user."""
        users = self.auth_manager._load_users()
        user_data = users.get(username)
        if user_data:
            limit = user_data.get("usage_limit", -1)
            current = user_data.get("current_usage", 0)
            return current, limit
        return 0, -1 # Default if user not found (should not happen for logged-in users)

    def can_use_feature(self, username):
        """Checks if a user can use a feature based on their usage limit."""
        current, limit = self.check_usage(username)
        if limit == -1: # Unlimited usage for admins or specially set users
            return True, ""
        if current < limit:
            return True, ""
        return False, f"You have reached your usage limit of {limit} uses. Please contact an administrator."

```
```python
# chatbot.py
import json
import os
from config import JOBS_FILE

class Chatbot:
    def __init__(self):
        self.jobs = {}
        self._load_jobs_data()

    def _load_jobs_data(self):
        """Loads job data from the JSON file."""
        if not os.path.exists(JOBS_FILE):
            os.makedirs(os.path.dirname(JOBS_FILE), exist_ok=True)
            # Create a default jobs.json if it doesn't exist
            default_jobs = {
                "Software Engineer": "Develops, tests, and maintains software applications, ensuring code quality and scalability. Requires strong programming skills and problem-solving abilities.",
                "Data Scientist": "Analyzes complex datasets to extract insights, build predictive models, and support decision-making. Proficiency in statistics, machine learning, and programming languages like Python/R is essential.",
                "Product Manager": "Defines product vision, strategy, and roadmap, overseeing the entire product lifecycle from conception to launch. Requires strong leadership, communication, and market analysis skills.",
                "UX Designer": "Focuses on user experience, designing intuitive and engaging interfaces for digital products. Involves user research, wireframing, prototyping, and usability testing."
            }
            with open(JOBS_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_jobs, f, indent=4)
        
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            self.jobs = json.load(f)

    def get_job_options(self):
        """Returns a list of available job titles."""
        if not self.jobs:
            return ["No job options available."]
        return list(self.jobs.keys())

    def get_job_details(self, job_title):
        """Returns the detailed description for a given job title."""
        return self.jobs.get(job_title, "Job details not found for the selected option.")

```
```python
# food_analyzer.py
import json
import os
from config import FOOD_NUTRITION_FILE

class FoodAnalyzer:
    def __init__(self):
        self.nutrition_data = {}
        self._load_nutrition_data()

    def _load_nutrition_data(self):
        """Loads nutritional data from the JSON file."""
        if not os.path.exists(FOOD_NUTRITION_FILE):
            os.makedirs(os.path.dirname(FOOD_NUTRITION_FILE), exist_ok=True)
            # Create a default food_nutrition.json if it doesn't exist
            default_nutrition = {
                "apple": {"calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
                "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
                "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
                "broccoli": {"calories": 55, "protein": 3.7, "carbs": 11, "fat": 0.6},
                "milk": {"calories": 103, "protein": 8, "carbs": 12, "fat": 2.4},
                "bread": {"calories": 265, "protein": 10, "carbs": 49, "fat": 3.2},
                "egg": {"calories": 78, "protein": 6, "carbs": 0.6, "fat": 5.3},
                "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13}
            }
            with open(FOOD_NUTRITION_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_nutrition, f, indent=4)
        
        with open(FOOD_NUTRITION_FILE, 'r', encoding='utf-8') as f:
            self.nutrition_data = json.load(f)

    def analyze_food_items(self, food_input):
        """
        Analyzes a comma-separated string of food items and provides nutritional information.
        """
        items = [item.strip().lower() for item in food_input.split(',') if item.strip()]
        
        if not items:
            return "Please enter at least one food item for analysis."

        analysis_results = {}
        total_calories = 0.0
        total_protein = 0.0
        total_carbs = 0.0
        total_fat = 0.0
        
        found_any_data = False

        for item in items:
            nutrition = self.nutrition_data.get(item)
            if nutrition:
                analysis_results[item] = nutrition
                total_calories += nutrition.get("calories", 0.0)
                total_protein += nutrition.get("protein", 0.0)
                total_carbs += nutrition.get("carbs", 0.0)
                total_fat += nutrition.get("fat", 0.0)
                found_any_data = True
            else:
                analysis_results[item] = "Nutrition information not found."
        
        overview = "\n--- Food Analysis Overview ---\n"
        for item, details in analysis_results.items():
            if isinstance(details, dict):
                overview += f"  {item.capitalize()}: Calories={details['calories']:.1f}, Protein={details['protein']:.1f}g, Carbs={details['carbs']:.1f}g, Fat={details['fat']:.1f}g\n"
            else:
                overview += f"  {item.capitalize()}: {details}\n"

        if found_any_data:
            overview += "\n--- Total Nutritional Summary (Approximate) ---\n"
            overview += f"  Total Calories: {total_calories:.1f}\n"
            overview += f"  Total Protein: {total_protein:.1f}g\n"
            overview += f"  Total Carbs: {total_carbs:.1f}g\n"
            overview += f"  Total Fat: {total_fat:.1f}g\n"
        else:
            overview += "\nNo nutritional data found for any of the entered items.\n"

        return overview

```
```python
# main.py
import os
import sys
from auth_manager import AuthManager
from user_manager import UserManager
from chatbot import Chatbot
from food_analyzer import FoodAnalyzer
from config import DATA_DIR, USERS_FILE

def setup_data_directory():
    """Ensures the data directory and initial user data exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        # Initialize with default users if file doesn't exist or is empty
        auth_mgr = AuthManager()
        print("Setting up initial user data...")
        auth_mgr.register_user("admin", "adminpassword", is_admin=True)
        auth_mgr.register_user("francois", "define", is_admin=True) # User story specific: "Francois to define"
        auth_mgr.register_user("user", "userpassword", is_admin=False)
        print("Default users created: 'admin' (adminpassword), 'francois' (define), 'user' (userpassword)")

def main():
    """Main application entry point."""
    setup_data_directory()

    auth_manager = AuthManager()
    user_manager = UserManager()
    job_chatbot = Chatbot()
    food_analyzer = FoodAnalyzer()

    current_user = None
    is_admin = False

    while True:
        if not current_user:
            print("\n--- Welcome to the AI System ---")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                success, message, admin_status = auth_manager.login_user(username, password)
                print(message)
                if success:
                    current_user = username
                    is_admin = admin_status
            elif choice == '2':
                username = input("Enter desired username: ").strip()
                password = input("Enter desired password: ").strip()
                # All new registrations are non-admin by default
                success, message = auth_manager.register_user(username, password, is_admin=False)
                print(message)
            elif choice == '3':
                sys.exit("Exiting application. Goodbye!")
            else:
                print("Invalid choice. Please try again.")
        else:
            print(f"\n--- Welcome, {current_user} ({'Admin' if is_admin else 'User'}) ---")
            print("1. AI Job Jobs options (Chatbot)")
            print("2. Instant Meal Check (Food Analysis)")
            if is_admin:
                print("3. Define User Restrictions")
            print("4. My Usage Status")
            print("5. Logout")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                can_use, msg = user_manager.can_use_feature(current_user)
                if can_use:
                    user_manager.increment_usage(current_user)
                    print("\n--- AI Job Jobs Chatbot ---")
                    print("Available Job Options:")
                    options = job_chatbot.get_job_options()
                    if options:
                        for i, option in enumerate(options):
                            print(f"{i+1}. {option}")
                        
                        while True:
                            job_choice = input("Enter the number of the job you're interested in, or 'back' to return to main menu: ").strip()
                            if job_choice.lower() == 'back':
                                break
                            try:
                                index = int(job_choice) - 1
                                if 0 <= index < len(options):
                                    selected_job = options[index]
                                    details = job_chatbot.get_job_details(selected_job)
                                    print(f"\nDetails for {selected_job}:\n{details}\n")
                                else:
                                    print("Invalid job number.")
                            except ValueError:
                                print("Invalid input. Please enter a number or 'back'.")
                    else:
                        print("No job options are currently available.")
                else:
                    print(f"\n{msg}\n")

            elif choice == '2':
                can_use, msg = user_manager.can_use_feature(current_user)
                if can_use:
                    user_manager.increment_usage(current_user)
                    print("\n--- Instant Meal Check ---")
                    food_input = input("Enter food items separated by commas (e.g., apple, rice, chicken breast): ").strip()
                    analysis = food_analyzer.analyze_food_items(food_input)
                    print(analysis)
                else:
                    print(f"\n{msg}\n")

            elif choice == '3' and is_admin:
                print("\n--- Define User Restrictions ---")
                target_user = input("Enter username to set limit for: ").strip()
                limit_str = input("Enter usage limit (-1 for unlimited): ").strip()
                
                success, message = user_manager.set_usage_limit(current_user, target_user, limit_str)
                print(message)
            
            elif choice == '4':
                current_usage, usage_limit = user_manager.check_usage(current_user)
                limit_display = "Unlimited" if usage_limit == -1 else usage_limit
                print(f"\n--- Your Usage Status ---")
                print(f"  Current Uses: {current_usage}")
                print(f"  Usage Limit: {limit_display}")
                if usage_limit != -1 and current_usage >= usage_limit:
                    print("  You have reached your usage limit.")
                print("--------------------------")

            elif choice == '5':
                current_user = None
                is_admin = False
                print("Logged out successfully.")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

```