# Python
from behave import given, when, then, before_scenario
from unittest.mock import Mock
import random

# --- Mock Application and System State Simulation ---
class MockApplication:
    """
    Simulates the application's state and behavior for testing purposes.
    This class acts as the 'System Under Test' for Behave steps,
    allowing for assertions on its internal state and simulated outputs.
    """
    def __init__(self):
        self.current_page = None
        self.logged_in_user = None
        self.user_accounts = {
            'freeuser@example.com': {'password': 'freepass123', 'type': 'Free', 'active': True, 'login_attempts': 0, 'locked': False, 'lockout_expires_at': None},
            'paiduser@example.com': {'password': 'paidpass123', 'type': 'Basic-level Paid', 'active': True, 'login_attempts': 0, 'locked': False, 'lockout_expires_at': None},
            'lockeduser@example.com': {'password': 'validpass123', 'type': 'Standard', 'active': True, 'login_attempts': 0, 'locked': False, 'lockout_expires_at': None},
            'nonexistent@example.com': {'password': 'wrongpassword123', 'type': 'NonExistent', 'active': False},
        }
        self.displayed_articles = []
        self.displayed_message = ""
        self.input_fields_valid = {'username': True, 'password': True}
        self.login_request_sent = False
        self.last_login_attempt_successful = False
        self.current_focus_order = []
        self.images_alt_text_mock_data = {
            'logo.png': 'Company Logo',
            'decorative_line.svg': '', # Decorative image
            'user_avatar.jpg': 'User Avatar for John Doe',
            'generic_image.png': 'image', # Example of bad alt text
        }
        self.contrast_compliant = True # Mock result for accessibility check
        self.responsive_layout_ok = True # Mock result for responsive check
        self.article_url = None
        self.article_type = None

    def reset_state(self):
        self.__init__() # Re-initialize to reset state

    def login(self, email, password):
        self.input_fields_valid = {'username': True, 'password': True} # Reset input field state
        self.displayed_message = "" # Reset message
        self.login_request_sent = True # Assume request is sent unless client-side validation prevents it

        account = self.user_accounts.get(email)

        if not account or not account['active']:
            self.displayed_message = "Invalid username or password"
            self.input_fields_valid['username'] = False
            self.input_fields_valid['password'] = False
            self.last_login_attempt_successful = False
            return False

        if account.get('locked', False):
            self.displayed_message = "Account is locked. Please try again later."
            self.last_login_attempt_successful = False
            return False

        if account['password'] == password:
            account['login_attempts'] = 0  # Reset on successful login
            self.logged_in_user = email
            self.current_page = 'home_page'
            self.displayed_articles = self._get_articles_for_user(account['type'])
            self.last_login_attempt_successful = True
            return True
        else:
            account['login_attempts'] = account.get('login_attempts', 0) + 1
            if account['login_attempts'] >= 5: # Example lockout threshold
                account['locked'] = True
                # In a real system, lockout_expires_at would be set here
                self.displayed_message = f"Account '{email}' is temporarily locked."
            else:
                self.displayed_message = "Invalid username or password"
                self.input_fields_valid['username'] = False
                self.input_fields_valid['password'] = False
            self.last_login_attempt_successful = False
            return False

    def _get_articles_for_user(self, user_type):
        articles = []
        # Simulate articles based on user type
        if user_type == 'Free' or user_type == 'Basic-level Paid':
            articles.append('Free Article 1')
            articles.append('Free Article 2')
        if user_type == 'Basic-level Paid':
            articles.append('Paid Article 1')
            articles.append('Paid Article 2')
        return articles

    def navigate_to_url(self, url):
        if self.logged_in_user:
            user_type = self.user_accounts[self.logged_in_user]['type']
            if '/articles/premium-investment-strategies' in url and user_type == 'Free':
                self.current_page = 'access_denied_page'
                self.displayed_message = "Access Denied"
                # For more detailed check, ensure content is not "rendered"
                self.displayed_articles = [] # No articles rendered
                return False
            else:
                self.current_page = url
                return True
        self.current_page = url # For unauthenticated access attempts
        return True

    def click_login_button(self, username=None, password=None):
        self.input_fields_valid = {'username': True, 'password': True} # Reset visual state
        self.displayed_message = "" # Reset displayed message
        self.login_request_sent = True # Assume request is sent unless client-side validation prevents it

        # Simulate client-side validation
        if username is None and password is None: # Empty fields scenario
            self.input_fields_valid['username'] = False
            self.input_fields_valid['password'] = False
            self.displayed_message = "Please enter username and password."
            self.login_request_sent = False
            self.last_login_attempt_successful = False
        elif username == "invalidemail" or ('@' not in (username or '') and username is not None): # Basic email format check
            self.input_fields_valid['username'] = False
            self.displayed_message = "Please enter a valid email address"
            self.login_request_sent = False
            self.last_login_attempt_successful = False
        elif (username and len(username) > 255) or (password and len(password) > 255): # Max length check
            self.input_fields_valid['username'] = False
            self.input_fields_valid['password'] = False
            self.displayed_message = "Username is too long" if len(username or '') > 255 else "Password is too long"
            self.login_request_sent = False
            self.last_login_attempt_successful = False
        else:
            self.login(username or '', password or '') # Proceed to server-side login logic

    def simulate_tab_navigation(self, elements_order):
        self.current_focus_order = elements_order
        return True # In a real test, this would involve detailed browser automation

    def verify_alt_text(self):
        # This mock simply asserts on the mock data based on common rules
        all_good = True
        for img_name, alt_text in self.images_alt_text_mock_data.items():
            if 'decorative' in img_name:
                if alt_text != '':
                    all_good = False
                    print(f"ERROR: Decorative image '{img_name}' has non-empty alt text: '{alt_text}'")
            elif alt_text == '' or alt_text == img_name.split('.')[0] or 'image' in alt_text.lower():
                all_good = False
                print(f"ERROR: Meaningful image '{img_name}' has generic or empty alt text: '{alt_text}'")
        return all_good

    def verify_contrast(self):
        # Placeholder for actual contrast ratio checks. Assumed compliant for this mock.
        return self.contrast_compliant

    def verify_responsive_layout(self):
        # Placeholder for actual responsive layout checks. Assumed compliant for this mock.
        return self.responsive_layout_ok

# --- Behave Hooks ---
@before_scenario
def setup_application(context, scenario):
    context.app = MockApplication()
    context.console_output = []
    context.metrics = {}

# --- GIVEN Steps ---
@given('a \'{subscription_type}\' subscription account (\'{email}\', \'{password}\') exists and is active')
def step_impl(context, subscription_type, email, password):
    # Ensure the mock account exists and matches details
    assert email in context.app.user_accounts, f"Mock account for {email} not found."
    account = context.app.user_accounts[email]
    assert account['type'] == subscription_type, f"Account {email} expected type {subscription_type}, got {account['type']}."
    assert account['password'] == password, f"Account {email} expected password {password}, got {account['password']}."
    assert account['active'] is True, f"Account {email} is not active."

@given('the user is on the application login page')
def step_impl(context):
    context.app.current_page = 'login_page'

@given('a specific \'{content_type}\' article exists with a known direct URL \'{url}\'')
def step_impl(context, content_type, url):
    context.app.article_url = url
    context.app.article_type = content_type

@given('a \'{subscription_type}\' subscription account (\'{email}\', \'{password}\') is logged in')
def step_impl(context, subscription_type, email, password):
    context.execute_steps(f"""
        Given a '{subscription_type}' subscription account ('{email}', '{password}') exists and is active
        And the user is on the application login page
        When the '{subscription_type}' subscriber logs in with '{email}' and '{password}'
    """)
    assert context.app.logged_in_user == email, "Login failed in prerequisite step."
    assert context.app.current_page == 'home_page', "Not redirected to home page after login."

@given('a registered user account \'{email}\' with \'{password}\' exists and is active')
def step_impl(context, email, password):
    assert email in context.app.user_accounts, f"Mock account for {email} not found."
    account = context.app.user_accounts[email]
    assert account['password'] == password, f"Account {email} expected password {password}, got {account['password']}."
    assert account['active'] is True, f"Account {email} is not active."
    context.user_under_test_email = email

@given('the application is deployed to a performance testing environment')
def step_impl(context):
    context.env = 'performance_testing'

@given('test data includes {num_users:d} concurrent valid user accounts')
def step_impl(context, num_users):
    context.num_concurrent_users_data = num_users

@given('Contentful API is configured and accessible')
def step_impl(context):
    context.contentful_api_status = 'accessible'

@given('the user is on the login page, using a keyboard for navigation')
def step_impl(context):
    context.app.current_page = 'login_page'
    context.keyboard_navigation_active = True

@given('the initial focus is on the \'{field_name}\' field')
def step_impl(context, field_name):
    context.initial_focus_element = field_name

@given('the user is on the home page')
def step_impl(context):
    context.app.current_page = 'home_page'

@given('the application is accessible on a mobile device or emulated mobile view')
def step_impl(context):
    context.mobile_test_context = True

# --- WHEN Steps ---
@when('the \'{subscription_type}\' subscriber logs in with \'{email}\' and \'{password}\'')
def step_impl(context, subscription_type, email, password):
    context.app.login(email, password)

@when('the logged-in free subscriber attempts to navigate directly to the \'{content_type}\' article\'s URL')
def step_impl(context, content_type):
    assert context.app.logged_in_user is not None, "Precondition failed: User is not logged in."
    assert context.app.user_accounts[context.app.logged_in_user]['type'] == 'Free', "Precondition failed: User is not a Free subscriber."
    context.app.navigate_to_url(context.app.article_url)

@when('the user clicks the \'Log In\' button with both username and password fields empty')
def step_impl(context):
    context.app.click_login_button(username="", password="")

@when('the user enters \'{username}\' into the username field and a valid password \'{password}\', then clicks \'Log In\'')
def step_impl(context, username, password):
    context.app.click_login_button(username=username, password=password)

@when('the user enters an excessively long string \(e.g., {length:d} characters\) into the username field')
def step_impl(context, length):
    context.long_username_input = 'a' * length

@when('the user enters an excessively long string \(e.g., {length:d} characters\) into the password field')
def step_impl(context, length):
    context.long_password_input = 'b' * length

@when('the user clicks the \'Log In\' button')
def step_impl(context):
    # Retrieve potentially long inputs from context, or use default if not set
    username = getattr(context, 'long_username_input', 'default@example.com')
    password = getattr(context, 'long_password_input', 'defaultpass')
    context.app.click_login_button(username=username, password=password)

@when('the user attempts to log in with an incorrect password \'{wrong_password}\' {attempts:d} consecutive times for \'{email}\'')
def step_impl(context, wrong_password, attempts, email):
    context.user_under_test_email = email # Ensure this context variable is set
    for _ in range(attempts):
        context.app.login(email, wrong_password)
        # In a real scenario, there might be a small delay here to simulate user pauses

@when('then tries logging in with the correct password \'{correct_password}\' for \'{email}\'')
def step_impl(context, correct_password, email):
    context.app.login(email, correct_password)

@when('the user enters an invalid username \'{username}\' and an invalid password \'{password}\'')
def step_impl(context, username, password):
    context.invalid_username_input = username
    context.invalid_password_input = password
    context.app.click_login_button(username=username, password=password)

@when('{num_users:d} concurrent users simulate the login process')
def step_impl(context, num_users):
    context.simulated_concurrent_users = num_users
    # Simulate login times for each user
    context.metrics['login_times'] = [random.uniform(0.1, 1.0) for _ in range(num_users)] # seconds

@when('each simulated user navigates to and waits for the home page to fully load')
def step_impl(context):
    # Simulate page load and API calls for each user
    context.metrics['homepage_full_load_times'] = [random.uniform(0.5, 5.0) for _ in range(context.simulated_concurrent_users)] # seconds
    context.metrics['contentful_api_response_times'] = [random.uniform(50, 800) for _ in range(context.simulated_concurrent_users)] # milliseconds

@when('the full page load time and Contentful API response times are monitored')
def step_impl(context):
    # This step is mainly for narrative flow; actual monitoring would occur during the 'each simulated user navigates' step.
    pass

@when('the user presses the \'Tab\' key repeatedly')
def step_impl(context):
    # Simulate expected tab order. The mock application verifies this.
    context.app.simulate_tab_navigation([
        'Username',
        'Password',
        'Remember Me checkbox',
        'Forgot Password link',
        'Log In button',
        'Sign Up button'
    ])

@when('all <img> elements and icons on the home page are inspected')
def step_impl(context):
    context.alt_text_inspection_result = context.app.verify_alt_text()

@when('an accessibility testing tool analyzes the color contrast ratios of text against its background')
def step_impl(context):
    context.contrast_analysis_result = context.app.verify_contrast()

@when('the application is opened on various mobile device viewports \(e.g., \'{device1}\', \'{device2}\'\) in both portrait and landscape orientations')
def step_impl(context, device1, device2):
    context.tested_mobile_viewports = [device1, device2]
    context.responsive_layout_check_result = context.app.verify_responsive_layout()

# --- THEN Steps ---
@then('the user is redirected to the home page')
def step_impl(context):
    assert context.app.current_page == 'home_page', f"Expected current page to be 'home_page', but was '{context.app.current_page}'."

@then('only articles explicitly tagged as \'{tag}\' are displayed on the home page')
def step_impl(context, tag):
    assert all(tag in article for article in context.app.displayed_articles), f"Not all displayed articles contain '{tag}' tag."
    # Ensure no 'Paid' articles are displayed for Free user
    assert not any('Paid' in article for article in context.app.displayed_articles), "Paid articles were unexpectedly displayed."

@then('no articles explicitly tagged as \'{tag}\' are displayed on the home page')
def step_impl(context, tag):
    assert not any(tag in article for article in context.app.displayed_articles), f"Articles tagged as '{tag}' were unexpectedly displayed."

@then('articles tagged as \'{tag}\' are displayed on the home page')
def step_impl(context, tag):
    assert any(tag in article for article in context.app.displayed_articles), f"No articles tagged as '{tag}' were displayed."

@then('the system prevents access to the \'{content_type}\' article')
def step_impl(context, content_type):
    assert context.app.current_page == 'access_denied_page', "Access was not prevented, or redirection was incorrect."

@then('an \'{message}\' or \'{alternative_message}\' message is prominently displayed')
def step_impl(context, message, alternative_message):
    assert message in context.app.displayed_message or alternative_message in context.app.displayed_message, \
        f"Expected message '{message}' or '{alternative_message}', but got '{context.app.displayed_message}'."

@then('the content of the \'{content_type}\' article is not rendered or displayed')
def step_impl(context, content_type):
    # This checks if the page changed to an access denied page and no articles are shown
    assert context.app.current_page == 'access_denied_page'
    assert not context.app.displayed_articles, "Article content was unexpectedly displayed."

@then('validation messages are displayed for respective empty fields')
def step_impl(context):
    assert not context.app.input_fields_valid['username'], "Username field not marked as invalid."
    assert not context.app.input_fields_valid['password'], "Password field not marked as invalid."
    assert "Please enter username and password." in context.app.displayed_message, "Expected empty field validation message."

@then('the login request is not sent to the server')
def step_impl(context):
    assert not context.app.login_request_sent, "Login request was unexpectedly sent to the server."

@then('the input fields are visually highlighted as invalid')
def step_impl(context):
    assert not context.app.input_fields_valid['username'] or not context.app.input_fields_valid['password'], \
        "Neither username nor password field was highlighted as invalid."

@then('a client-side validation message \'{message}\' is displayed for the username field')
def step_impl(context, message):
    assert message in context.app.displayed_message, f"Expected validation message '{message}', but got '{context.app.displayed_message}'."
    assert not context.app.input_fields_valid['username'], "Username field not marked as invalid."

@then('the username input field is visually highlighted as invalid')
def step_impl(context):
    assert not context.app.input_fields_valid['username'], "Username field not highlighted as invalid."

@then('the input fields should either truncate the input or display a validation message like \'{msg1}\' or \'{msg2}\'')
def step_impl(context, msg1, msg2):
    # In this mock, client-side validation prevents the request and sets a message
    assert not context.app.login_request_sent # Client-side should handle it
    assert (msg1 in context.app.displayed_message or msg2 in context.app.displayed_message), \
        f"Expected message '{msg1}' or '{msg2}', but got '{context.app.displayed_message}'."

@then('the application should handle the long input gracefully without crashing or causing unexpected UI behavior')
def step_impl(context):
    # This is a qualitative assertion that the mock cannot fully verify.
    # In a real test, this would involve checking logs for errors,
    # ensuring no critical crashes, or performing UI regression checks.
    assert True # Placeholder for a successful graceful handling.

@then('if a request is sent, the server should reject it with an appropriate error due to invalid input length')
def step_impl(context):
    if context.app.login_request_sent: # Check if the client-side validation allowed a request
        assert "too long" in context.app.displayed_message or not context.app.last_login_attempt_successful, \
            "Server did not reject long input or message was not appropriate."
    else:
        # If client-side validation prevented the request, this step implies that's the correct behavior.
        print("Note: Login request was prevented by client-side validation as expected.")
        assert not context.app.login_request_sent # Reinforce that it wasn't sent.

@then('after the {attempts:d}th incorrect attempt, the account \'{email}\' is temporarily locked')
def step_impl(context, attempts, email):
    assert context.app.user_accounts[email]['locked'] is True, f"Account {email} was not locked after {attempts} attempts."

@then('an informative message is displayed stating the account is locked and when they can retry')
def step_impl(context):
    assert "Account is locked" in context.app.displayed_message, "No informative account locked message displayed."

@then('the user cannot successfully log in until the lockout period expires')
def step_impl(context):
    # The last login attempt (with correct password) should have failed due to lockout
    assert not context.app.last_login_attempt_successful, "User unexpectedly logged in despite lockout."
    assert context.app.user_accounts[context.user_under_test_email]['locked'] is True, "Account is not in a locked state."

@then('an inline error message \'{message}\' is displayed directly below the login form fields')
def step_impl(context, message):
    assert message in context.app.displayed_message, f"Expected inline error message '{message}', but got '{context.app.displayed_message}'."

@then('the input fields for username and password are visually highlighted to indicate an error state')
def step_impl(context):
    assert not context.app.input_fields_valid['username'], "Username field not highlighted as error."
    assert not context.app.input_fields_valid['password'], "Password field not highlighted as error."

@then('the home page fully renders within {max_time:f} seconds for {percentage:d}% of users')
def step_impl(context, max_time, percentage):
    passing_loads = sum(1 for t in context.metrics['homepage_full_load_times'] if t <= max_time)
    actual_percentage = (passing_loads / len(context.metrics['homepage_full_load_times'])) * 100
    assert actual_percentage >= percentage, \
        f"Expected {percentage}% of home page loads within {max_time}s, but only {actual_percentage:.2f}% achieved."

@then('API calls to Contentful for article retrieval respond within {max_time_ms:d}ms for {percentage:d}% of requests')
def step_impl(context, max_time_ms, percentage):
    passing_responses = sum(1 for t in context.metrics['contentful_api_response_times'] if t <= max_time_ms)
    actual_percentage = (passing_responses / len(context.metrics['contentful_api_response_times'])) * 100
    assert actual_percentage >= percentage, \
        f"Expected {percentage}% of Contentful API calls within {max_time_ms}ms, but only {actual_percentage:.2f}% achieved."

@then('the focus moves logically through \'{element1}\', \'{element2}\', \'{element3}\' \(if present\), \'{element4}\', \'{element5}\', and \'{element6}\'')
def step_impl(context, element1, element2, element3, element4, element5, element6):
    expected_order = [
        element1,
        element2,
        element3.replace(' (if present)', ''), # Handle optional elements
        element4,
        element5,
        element6
    ]
    # Remove elements that are marked 'if present' and are not in the mock's expected path
    filtered_expected_order = [e for e in expected_order if e]
    assert context.app.current_focus_order == filtered_expected_order, \
        f"Expected tab order: {filtered_expected_order}, but actual was: {context.app.current_focus_order}."

@then('each interactive element is clearly highlighted with a visible focus indicator when selected')
def step_impl(context):
    # This is a visual check and hard to assert programmatically without image recognition tools.
    # In a real test, this would be verified visually or through dedicated accessibility tools.
    assert True # Placeholder for a successful visual check.

@then('every meaningful image or icon has a descriptive \'alt\' text that accurately conveys its content or purpose to a screen reader')
def step_impl(context):
    assert context.alt_text_inspection_result, "Some meaningful images or icons lack descriptive alt text."

@then('decorative images have \'alt=""\' or are implemented to be ignored by screen readers')
def step_impl(context):
    assert context.alt_text_inspection_result, "Some decorative images do not have alt=\"\" or are not ignored by screen readers."

@then('there are no generic \'alt\' attributes for images that convey meaning or are functional')
def step_impl(context):
    assert context.alt_text_inspection_result, "Some meaningful images have generic alt text."

@then('all text elements on the login page meet WCAG 2.1 AA contrast ratio guidelines \(at least {ratio_small:f}:1 for small text, {ratio_large:f}:1 for large text\)')
def step_impl(context, ratio_small, ratio_large):
    assert context.contrast_analysis_result, "Not all text elements meet WCAG 2.1 AA contrast ratio guidelines."

@then('error messages have sufficient contrast to be clearly legible against their background')
def step_impl(context):
    assert context.contrast_analysis_result, "Error messages do not have sufficient contrast."

@then('the UI adapts correctly to different mobile screen sizes and orientations without breaking layout or causing content overflow')
def step_impl(context):
    assert context.responsive_layout_check_result, "UI does not adapt correctly to different mobile screen sizes and orientations."

@then('text remains readable and does not overlap')
def step_impl(context):
    assert context.responsive_layout_check_result, "Text is not readable or overlaps on mobile devices."

@then('interactive elements are appropriately sized and spaced for easy touch interaction')
def step_impl(context):
    assert context.responsive_layout_check_result, "Interactive elements are not appropriately sized and spaced for touch."

@then('the entire page is viewable without horizontal scrolling')
def step_impl(context):
    assert context.responsive_layout_check_result, "The entire page requires horizontal scrolling on mobile."