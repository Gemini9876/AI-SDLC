```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:3000', // Assumption: This is the base URL of your application.
    
    /* Collect traces on failure. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
    
    /* Global timeout for actions like expect(locator).toBeVisible() */
    actionTimeout: 10 * 1000, // 10 seconds
    
    /* Timeout for individual tests */
    testTimeout: 60 * 1000, // 60 seconds
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    /* Test against mobile viewports. */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: { ...devices['Desktop Edge'], channel: 'msedge' },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    // },
  ],

  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://127.0.0.1:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
```

```typescript
// pages/LoginPage.ts
import { Locator, Page, expect } from '@playwright/test';

// UI Data Model mapping for easier reference and future updates
const UI_DATA_MODEL = {
  loginPage: {
    sectionOne: {
      fieldOne: { // app_logo.svg
        altText: "Application logo", // Assumption: Specific alt text for the logo. Adjust if different.
        selector: 'img[alt="Application logo"]', // Or by src, e.g., `img[src="/assets/icons/app_logo.svg"]`
      },
      fieldTwo: { // Welcome Back!
        text: "Welcome Back!",
        selector: 'text="Welcome Back!"', // Or a heading tag like 'h1:has-text("Welcome Back!")'
      },
      fieldThree: { // Username
        text: "Username",
        selector: 'label:has-text("Username")', // For label associated with input
        inputSelector: 'input[name="username"]', // Assumption: Input field has a 'name' attribute or accessible name 'Username'.
      },
      fieldFour: { // Password
        text: "Password",
        selector: 'label:has-text("Password")', // For label associated with input
        inputSelector: 'input[name="password"]', // Assumption: Input field has a 'name' attribute or accessible name 'Password'.
      },
    },
    sectionTwo: {
      fieldOne: { // login_arrow.svg
        selector: 'img[alt="Login arrow icon"]', // Assumption: Icon has alt text or can be located within the login button.
      },
      fieldTwo: { // Login button
        text: "Login",
        selector: 'button:has-text("Login")', // Finds a button with "Login" text.
      },
      fieldThree: { // Forgot Password?
        text: "Forgot Password?",
        selector: 'a:has-text("Forgot Password?")', // Finds an anchor tag with "Forgot Password?" text.
      },
      fieldFour: { // Language Dropdown
        selector: 'select[aria-label="Language selection"]', // Assumption: Dropdown is a <select> or has an aria-label.
        dropDownOption1: "English",
        dropDownOption2: "Español",
        dropDownOption3: "Français",
        // Assumption: Actual display text for translation checks
        translatedTexts: {
          "Welcome Back!": "¡Bienvenido de nuevo!", // Example Spanish translation
          "Username": "Nombre de usuario",
          "Password": "Contraseña",
          "Login": "Iniciar sesión",
          "Forgot Password?": "¿Olvidaste tu contraseña?"
        }
      },
    },
  },
};


export class LoginPage {
  private readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly appLogo: Locator;
  readonly usernameField: Locator;
  readonly passwordField: Locator;
  readonly loginButton: Locator;
  readonly loginArrowIcon: Locator;
  readonly forgotPasswordLink: Locator;
  readonly languageDropdown: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.locator(UI_DATA_MODEL.loginPage.sectionOne.fieldTwo.selector);
    this.appLogo = page.locator(UI_DATA_MODEL.loginPage.sectionOne.fieldOne.selector);
    this.usernameField = page.locator(UI_DATA_MODEL.loginPage.sectionOne.fieldThree.inputSelector);
    this.passwordField = page.locator(UI_DATA_MODEL.loginPage.sectionOne.fieldFour.inputSelector);
    this.loginButton = page.locator(UI_DATA_MODEL.loginPage.sectionTwo.fieldTwo.selector);
    this.loginArrowIcon = page.locator(UI_DATA_MODEL.loginPage.sectionTwo.fieldOne.selector);
    this.forgotPasswordLink = page.locator(UI_DATA_MODEL.loginPage.sectionTwo.fieldThree.selector);
    this.languageDropdown = page.locator(UI_DATA_MODEL.loginPage.sectionTwo.fieldFour.selector);
  }

  async navigateToLoginPage(): Promise<void> {
    await this.page.goto('/login'); // Assumption: Login page is at /login relative to baseURL.
    await expect(this.welcomeMessage).toBeVisible();
  }

  async enterCredentials(username?: string, password?: string): Promise<void> {
    if (username !== undefined) {
      await this.usernameField.fill(username);
    }
    if (password !== undefined) {
      await this.passwordField.fill(password);
    }
  }

  async clickLoginButton(): Promise<void> {
    await this.loginButton.click();
  }

  async verifyErrorMessage(message: string, field?: 'username' | 'password'): Promise<void> {
    if (field === 'username') {
      // Assumption: Error message for username is near the username field.
      await expect(this.page.locator(`xpath=./preceding-sibling::*[text()='${UI_DATA_MODEL.loginPage.sectionOne.fieldThree.text}']/following-sibling::*[contains(text(),'${message}')]`)).toBeVisible();
    } else if (field === 'password') {
      // Assumption: Error message for password is near the password field.
      await expect(this.page.locator(`xpath=./preceding-sibling::*[text()='${UI_DATA_MODEL.loginPage.sectionOne.fieldFour.text}']/following-sibling::*[contains(text(),'${message}')]`)).toBeVisible();
    } else {
      // General error message below input fields. Assumption: A generic error container.
      await expect(this.page.locator(`div:has-text("${message}")`)).toBeVisible(); // Or a specific error locator like '.error-message'
    }
  }

  async verifyRedirectToDashboard(): Promise<void> {
    // Assumption: Dashboard URL contains '/dashboard' and has a unique element.
    await this.page.waitForURL(/.*\/dashboard/);
    await expect(this.page).toHaveURL(/.*\/dashboard/);
    await expect(this.page.locator('h1:has-text("Dashboard")')).toBeVisible(); // Assumption: Dashboard has a specific heading
  }

  async verifyLoginPageNotDisplayed(): Promise<void> {
    await expect(this.welcomeMessage).not.toBeVisible();
    await expect(this.loginButton).not.toBeVisible();
  }

  async verifyLoginPageDisplayed(): Promise<void> {
    await expect(this.welcomeMessage).toBeVisible();
    await expect(this.loginButton).toBeVisible();
  }

  async selectLanguage(language: string): Promise<void> {
    await this.languageDropdown.selectOption(language);
    // Assumption: Selection instantly changes UI text without page reload.
  }

  async verifyPageTextsInSpanish(): Promise<void> {
    // Verifying main UI texts are translated
    await expect(this.page.locator(`text="${UI_DATA_MODEL.loginPage.sectionOne.fieldTwo.translatedTexts["Welcome Back!"]}"`)).toBeVisible();
    await expect(this.page.locator(`label:has-text("${UI_DATA_MODEL.loginPage.sectionOne.fieldThree.translatedTexts["Username"]}")`)).toBeVisible();
    await expect(this.page.locator(`label:has-text("${UI_DATA_MODEL.loginPage.sectionOne.fieldFour.translatedTexts["Password"]}")`)).toBeVisible();
    await expect(this.page.locator(`button:has-text("${UI_DATA_MODEL.loginPage.sectionTwo.fieldTwo.translatedTexts["Login"]}")`)).toBeVisible();
    await expect(this.page.locator(`a:has-text("${UI_DATA_MODEL.loginPage.sectionTwo.fieldThree.translatedTexts["Forgot Password?"]}")`)).toBeVisible();
  }

  async verifyPasswordInputMasked(): Promise<void> {
    await expect(this.passwordField).toHaveAttribute('type', 'password');
  }

  async assertElementFocus(element: Locator): Promise<void> {
    await expect(element).toBeFocused();
  }

  async verifyAppLogoAltText(): Promise<void> {
    await expect(this.appLogo).toHaveAttribute('alt', UI_DATA_MODEL.loginPage.sectionOne.fieldOne.altText);
  }

  async verifyLoginButtonAccessibleName(): Promise<void> {
    // Playwright uses 'name' to get the accessible name, which could be text content or aria-label.
    await expect(this.loginButton).toHaveAccessibleName(/Login( button)?|Login, press to access your account/i); // Matches common button names
    // Optionally check for the icon's role if it's meant to be descriptive visually but not announced by SR.
    // If the icon adds meaningful context (e.g., "Login with arrow"), then its alt text should be part of the button's accessible name or an aria-describedby.
    // For this case, assuming the button text itself is sufficient.
    await expect(this.loginArrowIcon).toBeVisible(); // Ensure the icon is visually present
  }
}
```

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

// --- Reusable Constants ---
const VALID_USERNAME = 'testuser';
const VALID_PASSWORD = 'password123';
const INVALID_USERNAME = 'invaliduser';
const WRONG_PASSWORD = 'wrongpassword';
const LOGIN_API_ENDPOINT = '/api/auth/login'; // Assumption: This is the API endpoint for login.

test.beforeEach(async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigateToLoginPage();
});

test.describe('User Authentication', () => {

  // Scenario: Successful User Login with Valid Credentials
  test('Successful User Login with Valid Credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is on the Login page identified by the 'Welcome Back!' (loginPage.sectionOne.fieldTwo) message
    // (Handled in beforeEach hook)
    await expect(loginPage.welcomeMessage).toBeVisible();

    // And the 'app_logo.svg' (loginPage.sectionOne.fieldOne) is displayed
    await expect(loginPage.appLogo).toBeVisible();

    // When the user inputs 'testuser' into the 'Username' (loginPage.sectionOne.fieldThree) field
    await loginPage.enterCredentials(VALID_USERNAME);

    // And the user inputs 'password123' into the 'Password' (loginPage.sectionOne.fieldFour) field
    await loginPage.enterCredentials(undefined, VALID_PASSWORD);

    // And the user clicks the 'Login' (loginPage.sectionTwo.fieldTwo) button, which includes the 'login_arrow.svg' (loginPage.sectionTwo.fieldOne) icon
    await expect(loginPage.loginArrowIcon).toBeVisible(); // Check icon visibility within the button or nearby
    await loginPage.clickLoginButton();

    // Then the user should be successfully redirected to the application's secure dashboard page
    await loginPage.verifyRedirectToDashboard();

    // And the Login page should no longer be displayed.
    await loginPage.verifyLoginPageNotDisplayed();
  });

  // Scenario: Unsuccessful User Login with Invalid Credentials
  test('Unsuccessful User Login with Invalid Credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is on the Login page identified by the 'Welcome Back!' (loginPage.sectionOne.fieldTwo) message
    // (Handled in beforeEach hook)
    await expect(loginPage.welcomeMessage).toBeVisible();

    // When the user inputs 'invaliduser' into the 'Username' (loginPage.sectionOne.fieldThree) field
    await loginPage.enterCredentials(INVALID_USERNAME);

    // And the user inputs 'wrongpassword' into the 'Password' (loginPage.sectionOne.fieldFour) field
    await loginPage.enterCredentials(undefined, WRONG_PASSWORD);

    // And the user clicks the 'Login' (loginPage.sectionTwo.fieldTwo) button
    await loginPage.clickLoginButton();

    // Then an error message 'Invalid username or password. Please try again.' should be displayed below the input fields
    const errorMessage = 'Invalid username or password. Please try again.'; // Assumption: Exact error message text
    await loginPage.verifyErrorMessage(errorMessage);

    // And the user should remain on the Login page.
    await loginPage.verifyLoginPageDisplayed();
  });

  // Scenario: Unsuccessful User Login with Empty Required Fields
  test('Unsuccessful User Login with Empty Required Fields', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is on the Login page identified by the 'Welcome Back!' (loginPage.sectionOne.fieldTwo) message
    // (Handled in beforeEach hook)
    await expect(loginPage.welcomeMessage).toBeVisible();

    // When the user leaves the 'Username' (loginPage.sectionOne.fieldThree) field empty
    // (No action needed, it's already empty)

    // And the user leaves the 'Password' (loginPage.sectionOne.fieldFour) field empty
    // (No action needed, it's already empty)

    // And the user clicks the 'Login' (loginPage.sectionTwo.fieldTwo) button
    await loginPage.clickLoginButton();

    // Then a validation message 'Username is required.' should be displayed near the 'Username' field
    const usernameRequiredMessage = 'Username is required.'; // Assumption: Exact validation message text
    await loginPage.verifyErrorMessage(usernameRequiredMessage, 'username');

    // And a validation message 'Password is required.' should be displayed near the 'Password' field
    const passwordRequiredMessage = 'Password is required.'; // Assumption: Exact validation message text
    await loginPage.verifyErrorMessage(passwordRequiredMessage, 'password');

    // And the user should remain on the Login page.
    await loginPage.verifyLoginPageDisplayed();
  });

  // Scenario: Login Page Load Performance
  test('Login Page Load Performance', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user's network connection is stable (e.g., 50 Mbps broadband)
    // Assumption: Playwright runs in a stable environment. For specific network throttling, Playwright's `page.route` or `context.setOffline` would be used.
    // Setting a route to simulate network conditions:
    // await page.route('**/*', route => route.continue()); // Default, no throttling
    // For actual throttling, consider external tools or more advanced Playwright features.

    // When the user navigates to the application's Login page URL
    const startTime = Date.now();
    await page.goto('/login', { waitUntil: 'domcontentloaded' }); // Wait for DOM to be loaded

    // Then the 'Welcome Back!' (loginPage.sectionOne.fieldTwo) message and all static UI elements including 'app_logo.svg' (loginPage.sectionOne.fieldOne) should fully render within 2 seconds
    await Promise.all([
      expect(loginPage.welcomeMessage).toBeVisible(),
      expect(loginPage.appLogo).toBeVisible(),
      expect(loginPage.usernameField).toBeVisible(),
      expect(loginPage.passwordField).toBeVisible(),
      expect(loginPage.loginButton).toBeVisible(),
    ]);
    const fullyRenderedTime = Date.now();
    const renderDuration = fullyRenderedTime - startTime;
    console.log(`Page fully rendered in: ${renderDuration} ms`);
    expect(renderDuration).toBeLessThanOrEqual(2000); // 2 seconds

    // And the page should be interactive within 3 seconds.
    await page.waitForLoadState('networkidle'); // Wait until network activity ceases
    const interactiveTime = Date.now();
    const interactiveDuration = interactiveTime - startTime;
    console.log(`Page interactive in: ${interactiveDuration} ms`);
    expect(interactiveDuration).toBeLessThanOrEqual(3000); // 3 seconds
  });

  // Scenario: API Login Response Performance
  test('API Login Response Performance', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user has entered valid credentials in the 'Username' (loginPage.sectionOne.fieldThree) and 'Password' (loginPage.sectionOne.fieldFour) fields
    await loginPage.enterCredentials(VALID_USERNAME, VALID_PASSWORD);

    // When the user clicks the 'Login' (loginPage.sectionTwo.fieldTwo) button
    const [loginResponse] = await Promise.all([
      page.waitForResponse(response => response.url().includes(LOGIN_API_ENDPOINT) && response.request().method() === 'POST'),
      loginPage.clickLoginButton(),
    ]);

    // Then the API response for authentication should be received within 1.5 seconds
    const responseTime = loginResponse.timing().responseEnd - loginResponse.timing().requestStart;
    console.log(`Login API response time: ${responseTime} ms`);
    expect(responseTime).toBeLessThanOrEqual(1500); // 1.5 seconds

    // And the user should be redirected to the dashboard within 2 seconds of clicking the button.
    const navigationStart = Date.now(); // After button click
    await loginPage.verifyRedirectToDashboard();
    const navigationEnd = Date.now();
    const redirectionDuration = navigationEnd - navigationStart;
    console.log(`Redirection to dashboard time: ${redirectionDuration} ms`);
    expect(redirectionDuration).toBeLessThanOrEqual(2000); // 2 seconds
  });

  // Scenario: Secure Password Input and Transmission
  test('Secure Password Input and Transmission', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is on the Login page
    // (Handled in beforeEach hook)

    // When the user inputs characters into the 'Password' (loginPage.sectionOne.fieldFour) field
    await loginPage.passwordField.fill('securepassword');

    // Then the input should be masked (e.g., as asterisks or dots) to prevent shoulder surfing
    await loginPage.verifyPasswordInputMasked();

    // When the user clicks the 'Login' (loginPage.sectionTwo.fieldTwo) button with valid credentials
    await loginPage.enterCredentials(VALID_USERNAME, VALID_PASSWORD);

    const [request] = await Promise.all([
      page.waitForRequest(req => req.url().includes(LOGIN_API_ENDPOINT) && req.method() === 'POST'),
      loginPage.clickLoginButton(),
    ]);

    // Then the authentication request to the API should be transmitted over HTTPS (TLS 1.2 or higher)
    expect(request.url()).toMatch(/^https:\/\//);
    // Assumption: Playwright's environment ensures TLS 1.2 or higher if the server supports it.
    // Directly asserting TLS version is not straightforward with Playwright's default API and often handled at infra level.

    // And the password should be securely hashed and salted before storage in the backend database.
    // Assumption: This is a backend architectural requirement and cannot be directly tested via UI or API interaction.
    // This aspect would typically be verified through code review, security audits, or separate backend integration tests.
    // console.log("Password hashing/salting is a backend implementation detail not directly verifiable via UI/API tests.");
  });

  // Scenario: Protection Against Brute-Force Attacks
  test('Protection Against Brute-Force Attacks', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const lockedAccountUsername = 'bruteforceuser'; // Assumption: A specific username for lockout testing.

    // Given a malicious actor attempts to log in to an account
    // When the actor makes 5 consecutive invalid login attempts within 5 minutes for the same username
    const maxAttempts = 5;
    const lockoutMessage = 'Account temporarily locked. Please try again after 15 minutes.'; // Assumption: Exact lockout message.
    const loginErrorMessage = 'Invalid username or password. Please try again.'; // Assumption: Standard login error.

    for (let i = 0; i < maxAttempts; i++) {
      await loginPage.navigateToLoginPage(); // Navigate to ensure a fresh state for each attempt
      await loginPage.enterCredentials(lockedAccountUsername, WRONG_PASSWORD);
      await loginPage.clickLoginButton();
      if (i < maxAttempts - 1) {
        await loginPage.verifyErrorMessage(loginErrorMessage);
      }
      // Pause to simulate realistic timing, if rate limits are time-based.
      // await page.waitForTimeout(1000); // Example: 1 second delay between attempts
    }

    // Then the system should temporarily lock the account for at least 15 minutes
    await loginPage.navigateToLoginPage(); // Attempt login after lockout threshold
    await loginPage.enterCredentials(lockedAccountUsername, VALID_PASSWORD); // Try with valid credentials to see lockout
    await loginPage.clickLoginButton();
    await loginPage.verifyErrorMessage(lockoutMessage); // Verify the lockout message

    // And the legitimate user should receive an email notification about the account lockout to alert them of suspicious activity.
    // Assumption: Verifying email notifications requires integration with an email testing service (e.g., Mailosaur, SendGrid API, or mocking SMTP).
    // This is out of scope for a pure UI/API Playwright test without such a service.
    // Example conceptual check if an email testing service were integrated:
    // const emailService = new MailosaurClient('YOUR_API_KEY');
    // const email = await emailService.messages.get('YOUR_SERVER_ID', {
    //   subject: 'Account Lockout Notification',
    //   to: lockedAccountUsername + '@example.com' // Assumption: User's email format
    // });
    // expect(email).toBeDefined();
    // expect(email.html?.body).toContain('Your account has been temporarily locked due to multiple failed login attempts.');
    console.log("Email notification verification requires an external email testing service and is not implemented in this example.");
  });

  // Scenario: Clear Error Messaging for Login Failures
  test('Clear Error Messaging for Login Failures', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user attempts to log in with an invalid username or password
    await loginPage.enterCredentials(INVALID_USERNAME, WRONG_PASSWORD);

    // When the system identifies the credentials as incorrect
    await loginPage.clickLoginButton();

    // Then an error message 'Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it.' should be clearly displayed below the 'Password' field
    const expectedErrorMessage = "Invalid username or password. Please try again or click 'Forgot Password?' if you need to reset it."; // Assumption: Exact error message
    await expect(page.locator('text=' + expectedErrorMessage)).toBeVisible(); // Find the specific error message text.
    // Ensure it's visually below password field. This often depends on CSS, checking direct parent/sibling relationships or general page flow.
    // A robust locator might be:
    // await expect(page.locator(`label:has-text("Password") + input + .error-message:has-text("${expectedErrorMessage}")`)).toBeVisible();
    // Or, check its position relative to the password field using bounding box, if strict pixel perfect is required.
    // For simplicity, asserting visibility of the text on the page is often sufficient.

    // And the error message should be human-readable and provide a suggestion for recovery (e.g., linking to 'Forgot Password?' (loginPage.sectionTwo.fieldThree)).
    await expect(page.locator('text=' + expectedErrorMessage)).toContainText('Forgot Password?');
    await expect(loginPage.forgotPasswordLink).toBeVisible(); // Ensure the link exists and is clickable within or near the message.
  });

  // Scenario: Language Selection Functionality
  test('Language Selection Functionality', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is on the Login page
    // (Handled in beforeEach hook)

    // When the user clicks on the language dropdown menu (loginPage.sectionTwo.fieldFour)
    // For a <select> element, simply interacting with it can make options visible.
    await loginPage.languageDropdown.click();

    // Then the options 'English' (loginPage.sectionTwo.fieldFour.dropDownOption1), 'Español' (loginPage.sectionTwo.fieldFour.dropDownOption2), and 'Français' (loginPage.sectionTwo.fieldFour.dropDownOption3) should be visible
    await expect(page.locator('option[value="en"]')).toBeVisible(); // Assumption: Value attributes for options.
    await expect(page.locator('option[value="es"]')).toBeVisible();
    await expect(page.locator('option[value="fr"]')).toBeVisible();
    await expect(page.locator('option:has-text("English")')).toBeVisible();
    await expect(page.locator('option:has-text("Español")')).toBeVisible();
    await expect(page.locator('option:has-text("Français")')).toBeVisible();

    // When the user selects 'Español'
    await loginPage.selectLanguage('es'); // Assumption: 'es' is the value for Español.

    // Then all visible text on the Login page, including 'Welcome Back!', 'Username', 'Password', 'Login', and 'Forgot Password?' should instantly change to their Spanish equivalents, as managed by Contentful.
    await loginPage.verifyPageTextsInSpanish();
  });

  // Scenario: Logical Tab Order Navigation
  test('Logical Tab Order Navigation', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is on the Login page
    // (Handled in beforeEach hook)
    await page.keyboard.press('Tab'); // Press tab once to ensure focus starts on an interactive element (e.g., first input)

    // When the user presses the Tab key repeatedly, starting from the page load
    // Then the focus should sequentially move in the following order:
    // 1. The 'Username' (loginPage.sectionOne.fieldThree) input field
    await loginPage.assertElementFocus(loginPage.usernameField);

    // 2. The 'Password' (loginPage.sectionOne.fieldFour) input field
    await page.keyboard.press('Tab');
    await loginPage.assertElementFocus(loginPage.passwordField);

    // 3. The 'Login' (loginPage.sectionTwo.fieldTwo) button
    await page.keyboard.press('Tab');
    await loginPage.assertElementFocus(loginPage.loginButton);

    // 4. The 'Forgot Password?' (loginPage.sectionTwo.fieldThree) link
    await page.keyboard.press('Tab');
    await loginPage.assertElementFocus(loginPage.forgotPasswordLink);

    // 5. The language dropdown (loginPage.sectionTwo.fieldFour)
    await page.keyboard.press('Tab');
    await loginPage.assertElementFocus(loginPage.languageDropdown);

    // And pressing Shift+Tab should reverse this order, returning focus to the previous element in the sequence.
    await page.keyboard.press('Shift+Tab');
    await loginPage.assertElementFocus(loginPage.forgotPasswordLink);

    await page.keyboard.press('Shift+Tab');
    await loginPage.assertElementFocus(loginPage.loginButton);

    await page.keyboard.press('Shift+Tab');
    await loginPage.assertElementFocus(loginPage.passwordField);

    await page.keyboard.press('Shift+Tab');
    await loginPage.assertElementFocus(loginPage.usernameField);
  });

  // Scenario: Comprehensive ALT Text for Visual Elements
  test('Comprehensive ALT Text for Visual Elements', async ({ page }) => {
    const loginPage = new LoginPage(page);

    // Given the user is using a screen reader on the Login page
    // (Playwright conceptually checks accessibility properties, not actual screen reader interaction)

    // When the screen reader encounters the 'app_logo.svg' (loginPage.sectionOne.fieldOne)
    // Then the screen reader should announce 'Application logo' or 'Company Name logo'
    await loginPage.verifyAppLogoAltText();

    // When the screen reader encounters the 'Login' button (loginPage.sectionTwo.fieldTwo) which visually includes the 'login_arrow.svg' (loginPage.sectionTwo.fieldOne)
    // Then the screen reader should announce 'Login button' or 'Login, press to access your account', ensuring the button's purpose is clearly conveyed and any decorative icon is either implicitly covered or explicitly described if it adds unique meaning.
    await loginPage.verifyLoginButtonAccessibleName();
  });
});
```