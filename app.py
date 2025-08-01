```python
import uuid
from typing import Dict, Optional, List, Union

class User:
    """Represents a user in the system with usage limits."""
    def __init__(self, username: str, is_admin: bool = False):
        self.username = username
        self.user_id = str(uuid.uuid4())
        self.is_admin = is_admin
        self.usage_limit: int = -1  # -1 means no limit
        self.current_usage: int = 0

    def set_usage_limit(self, limit: int):
        """Sets the usage limit for the user."""
        if self.is_admin:
            raise PermissionError("Admins cannot have usage limits.")
        if not isinstance(limit, int) or (limit < 0 and limit != -1):
            raise ValueError("Usage limit must be a non-negative integer or -1 for no limit.")
        self.usage_limit = limit
        print(f"Usage limit for user '{self.username}' set to {limit}.")

    def increment_usage(self) -> bool:
        """
        Increments the user's current usage count.
        Returns True if usage is within limits or no limit is set, False otherwise.
        Admins are exempt from usage limits.
        """
        if self.is_admin:
            return True

        if self.usage_limit == -1:
            self.current_usage += 1
            return True
        elif self.current_usage < self.usage_limit:
            self.current_usage += 1
            return True
        else:
            return False

    def get_remaining_usage(self) -> Union[int, float]:
        """Returns the number of remaining usages or float('inf') if unlimited."""
        if self.is_admin or self.usage_limit == -1:
            return float('inf')
        return self.usage_limit - self.current_usage

    def __repr__(self):
        return (f"User(username='{self.username}', is_admin={self.is_admin}, "
                f"limit={self.usage_limit}, current={self.current_usage})")

class UserManager:
    """Manages user accounts, creation, and usage limits."""
    _users: Dict[str, User] = {}  # In-memory storage: username -> User object

    def __init__(self):
        # Initialize with 'Francois' as the predefined admin user if not already present
        if "Francois" not in UserManager._users:
            admin_user = User("Francois", is_admin=True)
            UserManager._users["Francois"] = admin_user
            print("Admin user 'Francois' initialized.")

    def get_or_create_user(self, username: str) -> User:
        """Retrieves an existing user or creates a new one."""
        if username not in UserManager._users:
            new_user = User(username)
            UserManager._users[username] = new_user
            print(f"New user '{username}' created.")
        return UserManager._users[username]

    def get_user(self, username: str) -> Optional[User]:
        """Retrieves a user by username."""
        return UserManager._users.get(username)

    def set_user_limit(self, admin_username: str, target_username: str, limit: int):
        """
        Allows an admin user to set a usage limit for another user.
        Requires the calling user to be an admin.
        """
        admin_user = self.get_user(admin_username)
        if not admin_user or not admin_user.is_admin:
            raise PermissionError(f"User '{admin_username}' is not authorized to set limits.")

        target_user = self.get_user(target_username)
        if not target_user:
            raise ValueError(f"User '{target_username}' not found.")

        target_user.set_usage_limit(limit)

class Chatbot:
    """Handles chatbot interactions, specifically for selecting job options."""
    JOB_OPTIONS: List[str] = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "UI/UX Designer",
        "DevOps Engineer"
    ]

    def display_job_options(self):
        """Displays the list of available job options."""
        print("\nAvailable Job Options:")
        for i, option in enumerate(self.JOB_OPTIONS):
            print(f"{i + 1}. {option}")

    def select_job_option(self) -> Optional[str]:
        """
        Guides the user through selecting a job option via a text-based interface.
        Returns the selected job option or None if the user quits.
        """
        self.display_job_options()
        while True:
            try:
                choice = input("Enter the number of your desired job option (or 'q' to quit): ").strip().lower()
                if choice == 'q':
                    print("Job selection cancelled.")
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(self.JOB_OPTIONS):
                    selected_job = self.JOB_OPTIONS[index]
                    print(f"You have selected: {selected_job}")
                    return selected_job
                else:
                    print("Invalid option. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q'.")

class FoodAnalysis:
    """Manages input and mock analysis of food items."""
    def get_food_input(self) -> str:
        """Prompts the user to enter food items for analysis."""
        print("\n--- Instant Meal Check ---")
        print("Disclaimer: Enter food items to get analysis.")
        return input("Please enter your food items (e.g., 'apple, banana, 2 slices bread'): ").strip()

    def analyze_food_items(self, food_input: str) -> Dict[str, Union[str, List[str]]]:
        """
        Performs a simulated analysis of the entered food items.
        In a real application, this would involve complex AI/NLP and data lookups.
        """
        print(f"Analyzing: '{food_input}'...")
        input_items = [item.strip() for item in food_input.split(',') if item.strip()]

        analysis_result: Dict[str, Union[str, List[str]]] = {
            "input_items": input_items,
            "summary": "No specific analysis performed due to unknown items.",
            "nutritional_highlights": [],
            "potential_concerns": [],
            "suggested_improvements": []
        }

        # Simulate basic analysis based on keywords
        if "apple" in food_input.lower():
            analysis_result["nutritional_highlights"].append("Good source of fiber and Vitamin C.")
        if "banana" in food_input.lower():
            analysis_result["nutritional_highlights"].append("Rich in potassium and Vitamin B6.")
        if "bread" in food_input.lower():
            analysis_result["potential_concerns"].append("Consider whole grain options for improved fiber content.")
        if "sugar" in food_input.lower() or "soda" in food_input.lower():
            analysis_result["potential_concerns"].append("High in added sugars.")
            analysis_result["suggested_improvements"].append("Reduce added sugars for better health outcomes.")
        if "chicken" in food_input.lower():
            analysis_result["nutritional_highlights"].append("Good source of lean protein.")
        if "fries" in food_input.lower() or "fried" in food_input.lower():
            analysis_result["potential_concerns"].append("May be high in unhealthy fats.")
            analysis_result["suggested_improvements"].append("Opt for baked or grilled alternatives.")

        # Generate a more dynamic summary
        summary_parts: List[str] = [f"Your meal consisting of: {', '.join(input_items)} has been analyzed."]
        if analysis_result["nutritional_highlights"]:
            summary_parts.append("Highlights include: " + "; ".join(analysis_result["nutritional_highlights"]) + ".")
        if analysis_result["potential_concerns"]:
            summary_parts.append("Potential concerns: " + "; ".join(analysis_result["potential_concerns"]) + ".")
        if analysis_result["suggested_improvements"]:
            summary_parts.append("Suggestions: " + "; ".join(analysis_result["suggested_improvements"]) + ".")
        
        analysis_result["summary"] = " ".join(summary_parts) if summary_parts else "No detailed analysis available."

        return analysis_result

    def generate_food_analysis_overview(self, analysis_data: Dict[str, Union[str, List[str]]]) -> str:
        """
        Generates a formatted overview of the food analysis results.
        """
        overview_lines: List[str] = ["\n--- Food Analysis Overview ---"]
        
        input_items = analysis_data.get('input_items', [])
        overview_lines.append(f"Input Items: {', '.join(input_items)}")
        
        overview_lines.append(f"Summary: {analysis_data.get('summary', 'No summary available.')}")

        highlights = analysis_data.get('nutritional_highlights')
        if highlights and isinstance(highlights, list):
            overview_lines.append("\nNutritional Highlights:")
            for item in highlights:
                overview_lines.append(f"- {item}")

        concerns = analysis_data.get('potential_concerns')
        if concerns and isinstance(concerns, list):
            overview_lines.append("\nPotential Concerns:")
            for item in concerns:
                overview_lines.append(f"- {item}")

        improvements = analysis_data.get('suggested_improvements')
        if improvements and isinstance(improvements, list):
            overview_lines.append("\nSuggested Improvements:")
            for item in improvements:
                overview_lines.append(f"- {item}")

        overview_lines.append("------------------------------")
        return "\n".join(overview_lines)

class AIJobApp:
    """Main application class to run the AI Job App."""
    def __init__(self):
        self.user_manager = UserManager()
        self.chatbot = Chatbot()
        self.food_analysis = FoodAnalysis()
        self.current_user: Optional[User] = None

    def _login(self) -> bool:
        """Handles user login or creation."""
        while True:
            username = input("Enter your username (or 'q' to quit): ").strip()
            if username.lower() == 'q':
                return False
            self.current_user = self.user_manager.get_or_create_user(username)
            print(f"Logged in as: {self.current_user.username}")
            return True

    def _admin_menu(self):
        """Provides an interface for admin ('Francois') to manage user limits."""
        if not self.current_user or not self.current_user.is_admin:
            print("Access denied. You must be 'Francois' to access this menu.")
            return

        print("\n--- Admin Menu (Francois) ---")
        while True:
            print("1. Set user usage limit")
            print("2. View all users and their limits/usage")
            print("3. Back to main menu")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                target_username = input("Enter username to set limit for: ").strip()
                try:
                    limit_str = input(f"Enter usage limit for '{target_username}' (-1 for no limit): ").strip()
                    limit = int(limit_str)
                    self.user_manager.set_user_limit(self.current_user.username, target_username, limit)
                except (ValueError, PermissionError) as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            elif choice == '2':
                print("\n--- All Users ---")
                if not UserManager._users:
                    print("No users registered yet.")
                else:
                    for user in UserManager._users.values():
                        limit_display = "No Limit" if user.usage_limit == -1 else user.usage_limit
                        print(f"User: {user.username}, Admin: {user.is_admin}, Limit: {limit_display}, Current Usage: {user.current_usage}, Remaining: {user.get_remaining_usage()}")
                print("-----------------")
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        """Main application loop."""
        if not self._login():
            print("Exiting application.")
            return

        while True:
            if not self.current_user:
                print("Error: No user logged in. Exiting.")
                break

            print(f"\nWelcome, {self.current_user.username}!")
            if not self.current_user.is_admin:
                remaining = self.current_user.get_remaining_usage()
                remaining_display = "Unlimited" if remaining == float('inf') else remaining
                print(f"Remaining usages: {remaining_display}")

            print("\nAI Job App Main Menu:")
            print("1. Select Job Options (Chatbot)")
            print("2. Instant Meal Check (Food Analysis)")
            if self.current_user.is_admin:
                print("3. Admin Settings")
            print("0. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                if self.current_user.increment_usage():
                    self.chatbot.select_job_option()
                else:
                    print("Usage limit reached for this account. Please contact support or Francois.")
            elif choice == '2':
                if self.current_user.increment_usage():
                    food_input = self.food_analysis.get_food_input()
                    if food_input:
                        analysis_data = self.food_analysis.analyze_food_items(food_input)
                        overview = self.food_analysis.generate_food_analysis_overview(analysis_data)
                        print(overview)
                    else:
                        print("No food items entered for analysis.")
                else:
                    print("Usage limit reached for this account. Please contact support or Francois.")
            elif choice == '3' and self.current_user.is_admin:
                self._admin_menu()
            elif choice == '0':
                print("Thank you for using the AI Job App!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = AIJobApp()
    app.run()
```