```
class User:
    def __init__(self, email, password, profile_info, profile_picture, two_factor_authentication, privacy_settings):
        self.email = email
        self.password = password
        self.profile_info = profile_info
        self.profile_picture = profile_picture
        self.two_factor_authentication = two_factor_authentication
        self.privacy_settings = privacy_settings

    def login(self, email, password):
        if self.email == email and self.password == password:
            return "User logged in successfully"
        else:
            return "Invalid email or password"

    def reset_password(self):
        new_password = input("Enter new password: ")
        self.password = new_password
        return "Password reset successfully"

    def update_profile_info(self, new_info):
        self.profile_info = new_info

    def upload_profile_picture(self, picture):
        self.profile_picture = picture

    def change_email(self, new_email):
        self.email = new_email
        return "Email address changed successfully"

    def set_privacy_settings(self, new_settings):
        self.privacy_settings = new_settings
        return "Privacy settings updated successfully"


user1 = User("test@example.com", "password123", {"name": "Test User", "age": 30}, None, False, {"visible_email": True, "visible_age": False})

# User login and password reset feature
print(user1.login("test@example.com", "password123"))
print(user1.reset_password())

# User registration and two-factor authentication
user2 = User("newuser@example.com", "newpassword123", {}, None, True, {"visible_email": True, "visible_age": False})
print("User registered successfully with two-factor authentication: ", user2.two_factor_authentication)

# User profile management and privacy settings
user1.update_profile_info({"name": "Updated User", "age": 35})
user1.upload_profile_picture("profile_pic.jpg")
user1.change_email("newemail@example.com")
user1.set_privacy_settings({"visible_email": False, "visible_age": True})
```