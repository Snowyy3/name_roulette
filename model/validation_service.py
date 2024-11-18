import re


class ValidationService:
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        if not username:
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, ""

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        if not password:
            return False, "Password is required"
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        return True, ""

    @staticmethod
    def validate_display_name(display_name: str) -> tuple[bool, str]:
        if not display_name:
            return False, "Display name is required"
        if len(display_name) < 2:
            return False, "Display name must be at least 2 characters long"
        return True, ""
