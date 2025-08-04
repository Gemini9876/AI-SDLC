```python
import sys

class AppConfig:
    """
    Configuration settings for the AI Food Analysis Chatbot.
    """
    DISCLAIMER = (
        "Disclaimer: This tool provides a preliminary food analysis for informational purposes only. "
        "It is not a substitute for professional nutritional advice or medical consultation. "
        "Always consult with a qualified health professional for dietary concerns."
    )
    # Placeholder for usage limit, as 'Francois to define'
    USAGE_LIMIT_PER_USER = 3
    DEFAULT_USER_ID = "anonymous_user_session" # Simple session-based user ID for tracking

class UserManager:
    """
    Manages user-specific data, such as usage limits.
    """
    def __init__(self, config: AppConfig):
        self.config = config
        self._user_usage = {} # Stores {user_id: count_of_analyses}

    def increment_usage(self, user_id: str):
        """Increments the analysis count for a given user."""
        self._user_usage[user_id] = self._user_usage.get(user_id, 0) + 1

    def can_analyze(self, user_id: str) -> bool:
        """Checks if a user can perform another analysis based on the defined limit."""
        current_usage = self._user_usage.get(user_id, 0)
        return current_usage < self.config.USAGE_LIMIT_PER_USER

class FoodAnalyzer:
    """
    Simulates the AI component for food analysis.
    """
    def analyze(self, food_items_input: str) -> str:
        """
        Performs a simulated food analysis based on the input string and returns an overview.
        """
        if not food_items_input.strip():
            return "No specific food items were provided for analysis. Please enter items like 'chicken rice broccoli'."

        analysis_parts = []
        lower_input = food_items_input.lower()
        words = lower_input.split()

        # Simulate basic keyword-based analysis
        has_protein = any(item in words for item in ["chicken", "beef", "fish", "eggs", "tofu", "beans"])
        has_veggies = any(item in words for item in ["broccoli", "spinach", "carrot", "salad", "vegetables", "fruit"])
        has_carbs = any(item in words for item in ["rice", "pasta", "bread", "potato", "oats"])
        has_junk = any(item in words for item in ["pizza", "burger", "fries", "donut", "soda", "chips"])

        if has_junk:
            analysis_parts.append("This meal contains some items often associated with processed or fast food.")
            analysis_parts.append("Consider incorporating more whole foods for balance.")
        else:
            if has_protein and has_carbs and has_veggies:
                analysis_parts.append("This appears to be a well-balanced meal with protein, carbs, and vegetables.")
            elif has_protein and has_carbs:
                analysis_parts.append("Good protein and energy source. Add more vegetables for a complete meal.")
            elif has_protein and has_veggies:
                analysis_parts.append("Excellent protein and vitamin source. Consider a healthy carb for sustained energy.")
            elif has_carbs and has_veggies:
                analysis_parts.append("Rich in carbohydrates and fiber. Ensure adequate protein intake.")
            elif has_protein:
                analysis_parts.append("Contains protein. Pair with carbohydrates and vegetables for a balanced diet.")
            elif has_veggies:
                analysis_parts.append("Rich in vitamins and fiber. Consider adding protein and carbohydrates.")
            elif has_carbs:
                analysis_parts.append("Contains carbohydrates for energy. Pair with protein and vegetables.")
            else:
                analysis_parts.append("The input did not contain commonly recognized food groups for detailed analysis.")

        if not analysis_parts:
            analysis_parts.append(f"General analysis for: '{food_items_input}'.")
        
        # Add a generic summary if specific items weren't strongly categorized
        if len(analysis_parts) == 1 and "General analysis" in analysis_parts[0]:
             analysis_parts.append("Please provide a more descriptive list of food items for a comprehensive overview.")

        return "\n".join(analysis_parts)

class ChatbotInterface:
    """
    Handles all user input and output interactions for the chatbot.
    """
    def display_message(self, message: str):
        """Prints a message to the console."""
        print(message)

    def get_input(self, prompt: str) -> str:
        """Prompts the user for input and returns their response."""
        return input(prompt).strip()

class AIChatbotApp:
    """
    Main application class for the AI Food Analysis Chatbot.
    Orchestrates interaction between components.
    """
    def __init__(self):
        self.config = AppConfig()
        self.user_manager = UserManager(self.config)
        self.food_analyzer = FoodAnalyzer()
        self.chatbot = ChatbotInterface()
        self.current_user_id = self.config.DEFAULT_USER_ID # Simulates a single user session

    def run(self):
        """
        Starts the chatbot application and runs its main loop.
        """
        self.chatbot.display_message("Welcome to the AI Food Analysis Chatbot!")
        self.chatbot.display_message("\n" + self.config.DISCLAIMER)

        while True:
            if not self.user_manager.can_analyze(self.current_user_id):
                self.chatbot.display_message(
                    f"\nYou have reached your usage limit of {self.config.USAGE_LIMIT_PER_USER} analyses. "
                    "Please contact Francois for more information or wait for your limit to reset."
                )
                break # Exit the application if usage limit reached

            # Initial User Input - Text Based
            food_input = self.chatbot.get_input("\n--- ENTER FOOD ITEMS ---\nEnter the food items you consumed (e.g., 'chicken rice broccoli'): ")

            self.chatbot.display_message("\nAnalyzing your meal...")

            # Core AI Output - Food Analysis Overview
            analysis_overview = self.food_analyzer.analyze(food_input)
            self.chatbot.display_message("\n--- FOOD ANALYSIS OVERVIEW ---")
            self.chatbot.display_message(analysis_overview)
            self.chatbot.display_message("------------------------------")

            self.user_manager.increment_usage(self.current_user_id)

            # Jobs options user can select with chatbot
            while True:
                choice = self.chatbot.get_input("\n--- JOB OPTIONS ---\nSelect an option:\n1. Analyze another meal\n2. Exit Chatbot\nEnter your choice (1 or 2): ")
                if choice == '1':
                    break # Break out of inner loop to continue with another analysis
                elif choice == '2':
                    self.chatbot.display_message("\nThank you for using the AI Food Analysis Chatbot. Goodbye!")
                    return # Exit the application
                else:
                    self.chatbot.display_message("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    app = AIChatbotApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting chatbot. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
```