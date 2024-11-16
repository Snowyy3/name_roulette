# Implementation Plan for Login Screen and User Authentication

## Overview

Implement the login and sign-up screens along with basic user authentication logic for the Name Roulette application. This includes creating new UI components, handling user input, managing user data storage, and integrating authentication flow into the existing application.

## Steps

### 1. User Data Storage

- **Create `users.json`**:
  - Use a JSON file to store user data (username, display name, hashed password).
- **Implement Utility Functions**:
  - Write functions to load and save user data from/to `users.json`.
  - Use Python's `json` module for file operations.

### 2. Password Hashing

- **Use `hashlib` for Hashing**:
  - Implement password hashing using `hashlib.sha256` (very basic, and simple manual solution as this is an educational project)
  - Store only hashed passwords in `users.json`.

### 3. Create LoginView

- **Create `login_view.py`**:
  - Define `LoginView` class extending `UserControl`.
- **Build Login UI**:
  - Implement UI components as per `login_screen_description.md`.
  - Include input fields for username and password with placeholders.
  - Add a "Forgot Password?" link.
  - Add a "Continue" button for login.
  - Add a "Continue as Guest" button.
  - Include a link to switch to the sign-up screen.
- **Add Event Handlers**:
  - Validate input data on submission.
  - Authenticate user credentials against `users.json`.
  - Display error messages for invalid credentials.
  - On successful login, navigate to the main application view.

### 4. Create SignUpView

- **Create `signup_view.py`**:
  - Define `SignUpView` class extending `UserControl`.
- **Build Sign-Up UI**:
  - Implement UI components as per `login_screen_description.md`.
  - Include input fields for display name, username, and password.
  - Add a "Sign Up" button.
  - Include a link to switch back to the login screen.
- **Add Event Handlers**:
  - Validate input data (e.g., password complexity, unique username).
  - Hash the password and save the new user to `users.json`.
  - Display error messages for any issues.
  - On successful sign-up, optionally log the user in or redirect to the login screen.

### 5. Update MainView

- **Modify `main_view.py`**:
  - Update `handle_view_change` to include `LoginView` and `SignUpView`.
  - On application start, check if a user is authenticated.
    - If not, display `LoginView` instead of the main content.
- **Manage Navigation**:
  - Provide functionality to switch between login, sign-up, and main views.
  - Update the AppBar title and actions based on the current view.

### 6. Form Validation and Error Handling

- **Implement Validation**:
  - Ensure all required fields are filled.
  - Validate password complexity during sign-up.
- **Display Error Messages**:
  - Show error messages below the relevant input fields in red (`#ef4444`).
  - Use user-friendly language for errors.

### 7. Success Messages

- **Use SnackBar for Notifications**:
  - Display success messages upon successful login or sign-up.
  - Example: "Hello, `<user's display name>`!"
- **Handle Post-Login Navigation**:
  - Redirect authenticated users to the main application view.

### 8. Password Visibility Toggle

- **Implement Toggle Functionality**:
  - Use `TextField` with `password=True, can_reveal_password=True` for password fields.

### 9. Testing

- **Test All Flows**:
  - Verify login with valid and invalid credentials.
  - Test sign-up with existing and new usernames.
  - Ensure error messages and success messages display correctly.
  - Test navigation between views.

### 10. Optional Enhancements

- **Forgot Password Functionality**:
  - Implement a basic password reset mechanism.
- **Password Strength Indicator**:
  - Provide feedback on password strength during sign-up.
- **Session Management**:
  - Implement user session handling (optional for this demo).

### 11. User Account Display in Other Views

- **Modify Existing Views**:
  - Replace the existing User account display with a button showing "Guest" and a downwards arrow when no user is logged in.
  - Enclose the button in a rounded shape.
- **Logged-in State**:
  - When the user is logged in, replace "Guest" with the user's display name.
  - When the button is pressed, show options: "Change Password" and "Log Out".

### 12. Change Password Functionality

- **Implement Change Password Dialog**:
  - Create a pop-up dialog with three input fields: Current password, New password, Confirm new password.
  - Add "Cancel" and "Save Changes" buttons.
- **Handle Password Change Logic**:
  - Validate current password.
  - Ensure new passwords match and meet complexity requirements.
  - Update `users.json` with the new hashed password.

### 13. Log Out Functionality

- **Implement Log Out**:
  - On selecting "Log Out", clear authenticated user state.
  - Update UI to show "Guest" again.

## Notes

- **Security Considerations**:
  - While using basic hashing for educational purposes, remind users that this is not secure for production use.
- **Code Organization**:
  - Keep authentication logic modular for potential future enhancements.
- **User Experience**:
  - Ensure the UI is responsive and user-friendly across different screen sizes.
