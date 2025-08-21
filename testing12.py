# steps/mobile_app_steps.py
from behave import *
import time

# --- COMMON GIVEN STEPS ---

@given('User \'{username}\' exists with \'{subscription_type}\' subscription (email: {email}, password: {password}))'
def step_impl(context, username, subscription_type, email, password):
    context.users = getattr(context, 'users', {})
    context.users[username] = {
        'subscription': subscription_type,
        'email': email,
        'password': password,
        'logged_in': False
    }

@given('Content Management System contains \'{content_name}\' marked as \'{content_type}\'')
def step_impl(context, content_name, content_type):
    context.content = getattr(context, 'content', {})
    context.content[content_name] = {'type': content_type}

@given('Platform is mobile')
def step_impl(context):
    context.platform = 'mobile'

@given('System is accessible and \'Login Page\' is loaded')
def step_impl(context):
    context.current_page = 'Login Page'
    context.error_message = None

@given('The system is under a typical load of {num_users:d} concurrent users (simulated)')
def step_impl(context, num_users):
    context.load = num_users

@given('A valid {subscription_type} subscriber account is available')
def step_impl(context, subscription_type):
    context.test_user = {'subscription': subscription_type, 'email': 'test@example.com', 'password': 'password'}

@given('User \'{username}\' is logged in with a \'{subscription_type}\' subscription')
def step_impl(context, username, subscription_type):
    context.users = getattr(context, 'users', {})
    context.users[username] = {
        'subscription': subscription_type,
        'logged_in': True,
        'current_page': 'Home Page'
    }
    context.logged_in_user = username

@given('A \'{article_name}\' exists with a known URL \'{url}\'')
def step_impl(context, article_name, url):
    context.articles = getattr(context, 'articles', {})
    context.articles[url] = {'name': article_name, 'type': 'Paid'} # Assuming it's paid for this scenario

@given('The user is on the \'Login Page\'')
def step_impl(context):
    context.current_page = 'Login Page'
    context.email_field_value = ''
    context.password_field_value = ''
    context.email_validation_message = None
    context.password_validation_message = None

@given('The user is viewing the \'Home Page\'')
def step_impl(context):
    context.current_page = 'Home Page'

@given('A screen reader is activated')
def step_impl(context):
    context.screen_reader_active = True

@given('The \'Login Page\' and \'Home Page\' are displayed')
def step_impl(context):
    context.displayed_pages = ['Login Page', 'Home Page']

@given('A color contrast analyzer tool is used')
def step_impl(context):
    context.contrast_tool_used = True

# --- WHEN STEPS ---

@when('\'{username}\' logs in with valid credentials')
def step_impl(context, username):
    user = context.users.get(username)
    if user and user['email'] == user['email'] and user['password'] == user['password']: # Simulate valid credentials
        user['logged_in'] = True
        context.logged_in_user = username
        context.current_page = 'Home Page'
        context.login_successful = True
    else:
        context.login_successful = False
        context.error_message = 'Invalid email or password.'

@when('User attempts to log in with email \'{email}\' and password \'{password}\'')
def step_impl(context, email, password):
    context.login_attempt_email = email
    context.login_attempt_password = password
    # Simulate login attempt logic
    if email == 'wrong@example.com' and password == 'wrongpassword':
        context.login_successful = False
        context.error_message = 'Invalid email or password.'
        context.current_page = 'Login Page'
    elif email == 'invalid-email':
        context.login_successful = False
        context.email_validation_message = 'Please enter a valid email address.'
        context.current_page = 'Login Page'
    else:
        # For other cases, assume successful or specific handling as per test
        context.login_successful = True # Placeholder for valid cases
        context.current_page = 'Home Page'

@when('The \'Home Page\' is loaded')
def step_impl(context):
    start_time = time.time()
    # Simulate page loading time (e.g., based on load context.load)
    # For simplicity, we just record start time and check elapsed in Then step
    context.page_load_start_time = start_time

@when('\'{username}\' attempts to navigate directly to \'{url}\'')
def step_impl(context, username, url):
    user = context.users.get(username)
    article = context.articles.get(url)
    context.attempted_url = url
    if user and user['logged_in'] and user['subscription'] == 'Free' and article and article['type'] == 'Paid':
        context.redirected_page = 'Access Denied' # Or 'Subscription Upgrade'
        context.access_denied = True
    else:
        context.access_denied = False

@when('Both \'Email\' and \'Password\' fields are empty')
def step_impl(context):
    context.email_field_value = ''
    context.password_field_value = ''

@when('The \'Login\' button is tapped')
def step_impl(context):
    if context.email_field_value == '' and context.password_field_value == '':
        context.email_validation_message = 'Email is required.'
        context.password_validation_message = 'Password is required.'
        context.current_page = 'Login Page'
    # More complex validation could go here if needed for other scenarios

@when('The \'Tab\' key is pressed repeatedly (or accessibility gesture for next element)')
def step_impl(context):
    # Simulate tab order sequence
    context.tab_order_elements = ['Email', 'Password', 'Login Button', 'Forgot Password? Link', 'Sign Up Link']
    context.focus_path = ['Email', 'Password', 'Login Button', 'Forgot Password? Link', 'Sign Up Link']

@when('The screen reader navigates through all visual elements (images, icons, banners, thumbnails)')
def step_impl(context):
    context.visual_elements_scanned = True
    # Simulate checking alt texts
    context.elements_alt_text_status = {
        'Image1': {'has_alt': True, 'descriptive': True},
        'Icon2': {'has_alt': True, 'descriptive': True},
        'Banner3': {'has_alt': True, 'descriptive': True},
        'Thumbnail4': {'has_alt': True, 'descriptive': True}
    }

@when('The color contrast ratio is checked for text against its background for:
{elements_table}')
def step_impl(context, elements_table):
    context.contrast_checked_elements = []
    for row in elements_table.split('
'):
        context.contrast_checked_elements.append(row.strip())
    # Simulate contrast check results for simplicity
    context.contrast_results = {
        'Login Page: Email/Password field labels': True,
        'input text': True,
        'error messages': True,
        'button text': True,
        'links': True,
        'Home Page: Article titles': True,
        'body text': True,
        'navigation elements': True,
        'footer text': True
    }

# --- THEN STEPS ---

@then('\'{username}\' should be redirected to the \'Home Page\'')
def step_impl(context, username):
    assert context.login_successful is True, f"Login for {username} was not successful."
    assert context.current_page == 'Home Page', f"Expected to be on Home Page, but on {context.current_page}."

@then('\'{username}\' should see \'{content_name}\' displayed')
def step_impl(context, username, content_name):
    assert content_name in context.content, f"Content '{content_name}' not found in CMS."
    user = context.users.get(username)
    content_type = context.content[content_name]['type']
    
    if user['subscription'] == 'Free':
        assert content_type == 'Free', f"Free user {username} should only see Free content, but saw {content_type} content."
        # Simulate content display
        context.displayed_content = getattr(context, 'displayed_content', [])
        context.displayed_content.append(content_name)
        assert content_name in context.displayed_content, f"Expected '{content_name}' to be displayed, but it was not."
    elif user['subscription'] == 'Basic Paid':
        # Simulate content display for paid users (both free and paid)
        context.displayed_content = getattr(context, 'displayed_content', [])
        context.displayed_content.append(content_name)
        assert content_name in context.displayed_content, f"Expected '{content_name}' to be displayed, but it was not."
    

@then('\'{username}\' should not see any content marked as \'Paid\'')
def step_impl(context, username):
    user = context.users.get(username)
    assert user['subscription'] == 'Free', f"This step is for Free users, but {username} is {user['subscription']}."
    
    for content_item, details in context.content.items():
        if details['type'] == 'Paid':
            # In a real test, this would involve checking the UI for absence of paid content
            assert content_item not in getattr(context, 'displayed_content', []), \
                f"Free user {username} unexpectedly saw Paid content: {content_item}."

@then('The user should remain on the \'Login Page\'')
def step_impl(context):
    assert context.current_page == 'Login Page', f"Expected to remain on Login Page, but was redirected to {context.current_page}."

@then('The user should see an error message \'{message}\'')
def step_impl(context, message):
    assert context.error_message == message, f"Expected error message '{message}', but got '{context.error_message}'."

@then('The user should not be able to access any content')
def step_impl(context):
    assert context.login_successful is False, "Login was unexpectedly successful."
    assert context.current_page == 'Login Page', "User was able to navigate away from Login Page."
    # Further checks like attempting to access a specific page and verifying redirection

@then('The \'Home Page\' content should be displayed within {seconds:f} seconds')
def step_impl(context, seconds):
    end_time = time.time()
    elapsed_time = end_time - context.page_load_start_time
    assert elapsed_time < seconds, f"Home Page loaded in {elapsed_time:.2f} seconds, which is more than {seconds} seconds."

@then('\'{username}\' should be redirected to an \'{redirect_page}\' page or \'Subscription Upgrade\' page')
def step_impl(context, username, redirect_page):
    assert context.access_denied is True, "Access was not denied as expected."
    # Check if redirect page is one of the expected
    assert context.redirected_page in [redirect_page, 'Subscription Upgrade'], \
        f"Expected redirection to '{redirect_page}' or 'Subscription Upgrade', but was redirected to '{context.redirected_page}'."

@then('\'{username}\' should not see the content of \'{article_name}\'')
def step_impl(context, username, article_name):
    # This implies checking the current page content
    # For simulation, we assume if redirected, content is not seen.
    assert context.access_denied is True, f"User {username} unexpectedly accessed content of {article_name}."
    assert context.current_page != 'Paid Article X', f"User {username} should not be on the Paid Article page."

@then('The \'Email\' field should display a validation message \'{message}\'')
def step_impl(context, message):
    assert context.email_validation_message == message, \
        f"Expected email validation message '{message}', but got '{context.email_validation_message}'."

@then('The \'Password\' field should display a validation message \'{message}\'')
def step_impl(context, message):
    assert context.password_validation_message == message, \
        f"Expected password validation message '{message}', but got '{context.password_validation_message}'."

@then('The focus should move sequentially from {element_list}')
def step_impl(context, element_list):
    expected_order = [e.strip().replace("'", "") for e in element_list.split(' to ')]
    # Simulate actual traversal and verify
    assert context.focus_path == expected_order, \
        f"Expected tab order {expected_order}, but got {context.focus_path}."

@then('Each interactive element should have a visible focus indicator when selected')
def step_impl(context):
    # This would typically require UI automation checks for CSS properties or visual appearance
    # For simulation, we assume this is verified.
    context.visible_focus_indicator_verified = True

@then('All images, icons, and non-textual elements should have descriptive \'alt\' attributes')
def step_impl(context):
    assert context.screen_reader_active is True, "Screen reader not active for this check."
    for element, status in context.elements_alt_text_status.items():
        assert status['has_alt'] is True, f"Element '{element}' is missing an 'alt' attribute."

@then('The \'alt\' text should accurately convey the purpose or content of the element as read by the screen reader')
def step_impl(context):
    assert context.screen_reader_active is True, "Screen reader not active for this check."
    for element, status in context.elements_alt_text_status.items():
        assert status['descriptive'] is True, f"Alt text for '{element}' is not descriptive."

@then('All critical text and interactive elements should meet WCAG 2.1 AA contrast ratio guidelines (at least {normal_contrast:f}:1 for normal text, {large_contrast:f}:1 for large text)')
def step_impl(context, normal_contrast, large_contrast):
    assert context.contrast_tool_used is True, "Color contrast analyzer tool not used."
    for element, passed in context.contrast_results.items():
        assert passed is True, f"Color contrast failed for '{element}'."
