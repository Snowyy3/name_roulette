
1. General Layout:
   - Center the forms vertically and horizontally on the page.
   - Set the maximum width of the forms to 400 pixels.
   - Use padding of 2rem (32 pixels) around the form content.
   - Use the 'Inter' font family for all text.

2. Login Screen:

   a. Header:
      - Display "Welcome back" as the main heading.
      - Center-align the heading.
      - Use a font size of 28 pixels and a font weight of 700 (bold).
      - Set the color to #13343b.
      - Add a bottom margin of 2rem (32 pixels) to the heading.

   b. Input Fields:
      - Create two input fields: one for username and one for password.
      - Label the first input field with placeholder text "Username".
      - Label the second input field with placeholder text "Password".
      - Style input fields as follows:
        * Width: 100% of container
        * Padding: 0.75rem (12 pixels) vertically, 1rem (16 pixels) horizontally
        * Border: 1 pixel solid, color #e0e0e0
        * Border radius: 8 pixels
        * Font size: 1rem (16 pixels)
        * Placeholder text color: #9ca3af
      - On focus, change the border color to #10b981 (green).
      - Add a margin of 1rem (16 pixels) between input fields.

   c. Password Visibility Toggle:
      - Use textfield with `password=True, can_reveal_password=True`

   d. Forgot Password Link:
      - Add a "Forgot Password?" link below the password field.
      - Align the link to the right.
      - Set the link color to #10b981 (green).
      - Use a font size of 0.875rem (14 pixels).
      - Add a bottom margin of 1rem (16 pixels) to the link.

   e. Login Button:
      - Label the button "Continue".
      - Style the button as follows:
        * Width: 100% of container
        * Padding: 0.75rem (12 pixels) vertically
        * Background color: #10b981 (green)
        * Text color: white
        * Border: none
        * Border radius: 8 pixels
        * Font size: 1rem (16 pixels)
        * Font weight: 500 (medium)
      - On hover, change the background color to #059669 (darker green).

   f. Sign Up Section:
      - Add "New here? Sign up" text below the login button.
      - Center-align this text.
      - Set the text color to #6b7280 (gray).
      - Use a font size of 0.875rem (14 pixels).
      - Style "Sign up" as a link with color #10b981 (green) and font weight 500 (medium).

   g. Divider:
      - Add an "OR" divider below the sign-up section.
      - Create a horizontal line on both sides of "OR".
      - Style the divider as follows:
        * Line color: #e0e0e0
        * "OR" text color: #6b7280 (gray)
        * "OR" font size: 0.875rem (14 pixels)
      - Center the "OR" text vertically and horizontally between the lines.

   h. Continue as Guest button
      - Similar to Continue button, with some differences
      - Same background color as the page, but turns light grey when hovered over
      - Text: "<icon> Continue as Guest"
      - Icon: icons.PERSON_OFF (colored grey)

3. Sign Up Screen:

   a. Header:
      - Display "Create an account" as the main heading.
      - Use the same styling as the login screen header.

   b. Input Fields:
      - Create three input fields: Display name, Username, and Password.
      - Use the same styling as the login screen input fields.
      - Add appropriate placeholder text for each field.

   c. Password Visibility Toggle:
      - Implement the same password visibility toggle as in the login screen.

   d. Sign Up Button:
      - Label the button "Sign Up".
      - Use the same styling as the login button.

   e. Login Link:
      - Add "Already have an account? Log in" text below the sign-up button.
      - Style it similarly to the sign-up link on the login screen.

4. Functionality:
   - Implement form validation for both login and sign-up forms.
   - For the login form, check for non-empty username and password.
   - For the sign-up form ensure password meets complexity requirements (defined later).
   - On form submission, simulate a login or sign-up process (you can use simple checks against hardcoded credentials or a mock database).
   - Show appropriate error messages for invalid inputs or failed login/sign-up attempts.
   - On successful login or sign-up, display a success message (use snackbar, saying "Hello, <user's display name>!).

5. Error Handling:
   - Display error messages in red (#ef4444) below the relevant input fields.
   - Use a font size of 0.875rem (14 pixels) for error messages.
