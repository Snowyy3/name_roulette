import flet as ft


class UserAuthenticationController:
    def __init__(self, page, auth):
        self.page = page
        self.auth = auth  # Use the shared instance
        self.current_user = None

    def handle_login(self, username: str, password: str) -> bool:
        """Handle login attempt"""
        if username is None and password is None:
            # Guest login
            self.current_user = {"display_name": "Guest", "username": None}
            return True

        if self.auth.verify_password(username, password):
            display_name = self.auth.get_display_name(username)
            self.current_user = {"display_name": display_name, "username": username}
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
