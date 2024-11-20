import flet as ft
from model.validation_service import ValidationService


class UserAuthenticationController:
    def __init__(self, page, auth):
        self.page = page
        self.auth = auth  # Use the shared instance
        self.current_user = None
        self.validation = ValidationService()
        self.list_controller = None  # Add reference to ListController

    def set_list_controller(self, list_controller):
        """Set the list controller reference"""
        self.list_controller = list_controller

    def handle_login(self, username: str, password: str) -> bool:
        """Handle login attempt"""
        if username is None and password is None:
            # Guest login
            self.current_user = {"display_name": "Guest", "username": None}
            if self.list_controller:
                self.list_controller.handle_user_change()
            return True

        if self.auth.verify_password(username, password):
            display_name = self.auth.get_display_name(username)
            self.current_user = {"display_name": display_name, "username": username}
            if self.list_controller:
                self.list_controller.handle_user_change()
            return True
        return False

    def handle_signup(self, username: str, display_name: str, password: str) -> bool:
        """Handle signup attempt"""
        try:
            self.auth.add_user(username, display_name, password)
            return True
        except ValueError as e:
            return False

    def handle_logout(self):
        """Handle logout"""
        self.current_user = None
        if self.list_controller:
            self.list_controller.handle_user_change()

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None

    def get_current_user(self) -> dict:
        """Get current user info"""
        return self.current_user or {"display_name": "Guest", "username": None}

    def change_password(self, username: str, current_password: str, new_password: str) -> bool:
        """
        Change user's password.

        Args:
            username: Username whose password to change
            current_password: Current password for verification
            new_password: New password to set

        Returns:
            bool: True if password was changed successfully

        Raises:
            ValueError: If current password is incorrect
        """
        return self.auth.change_password(username, current_password, new_password)

    def validate_login_input(self, username: str, password: str) -> tuple[bool, str]:
        """Validate login input"""
        username_valid, username_error = self.validation.validate_username(username)
        if not username_valid:
            return False, username_error

        password_valid, password_error = self.validation.validate_password(password)
        if not password_valid:
            return False, password_error

        return True, ""

    def validate_signup_input(self, username: str, display_name: str, password: str) -> tuple[bool, str]:
        """Validate signup input"""
        display_name_valid, display_name_error = self.validation.validate_display_name(display_name)
        if not display_name_valid:
            return False, display_name_error

        username_valid, username_error = self.validation.validate_username(username)
        if not username_valid:
            return False, username_error

        password_valid, password_error = self.validation.validate_password(password)
        if not password_valid:
            return False, password_error

        return True, ""

    def reset_password(self, username: str, new_password: str) -> tuple[bool, str]:
        """Handle password reset"""
        password_valid, password_error = self.validation.validate_password(new_password)
        if not password_valid:
            return False, password_error

        try:
            # Hash and save new password
            hashed_password = self.auth._hash_password(new_password)
            self.auth.users["users"][username]["password"] = hashed_password
            self.auth.save_users()
            return True, "Password reset successfully"
        except Exception as e:
            return False, str(e)

    def validate_username_availability(self, username: str) -> tuple[bool, str]:
        """Check if username is available"""
        if username in self.auth.users["users"]:
            return False, "Username already exists"
        return self.validation.validate_username(username)

    def validate_password_live(self, password: str) -> tuple[bool, str]:
        """Validate password for live feedback"""
        return self.validation.validate_password(password)
