import json
import hashlib
import os


class UserAuthentication:
    def __init__(self, file_path=r"data/users.json"):
        """Initialize user authentication with users file path."""
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        """Load users from JSON file."""
        if not os.path.exists(self.file_path):
            return {"users": {}}

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {"users": {}}

    def save_users(self):
        """Save users to JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(self.users, file, indent=4)

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username: str, display_name: str, password: str) -> bool:
        """
        Add a new user to the system.

        Args:
            username: Unique username
            display_name: User's display name
            password: Plain text password to be hashed

        Returns:
            bool: True if user was added successfully

        Raises:
            ValueError: If username already exists
        """
        if username in self.users["users"]:
            raise ValueError("Username already exists")

        hashed_password = self._hash_password(password)
        self.users["users"][username] = {"display_name": display_name, "password": hashed_password}
        self.save_users()
        return True

    def verify_password(self, username: str, password: str) -> bool:
        """
        Verify user's password.

        Args:
            username: Username to verify
            password: Plain text password to verify

        Returns:
            bool: True if password matches
        """
        if username not in self.users["users"]:
            return False

        hashed_password = self._hash_password(password)
        return self.users["users"][username]["password"] == hashed_password

    def get_display_name(self, username: str) -> str:
        """
        Get user's display name.

        Args:
            username: Username to look up

        Returns:
            str: User's display name or None if user not found
        """
        user = self.users["users"].get(username)
        return user["display_name"] if user else None

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
        if not self.verify_password(username, current_password):
            raise ValueError("Current password is incorrect")

        self.users["users"][username]["password"] = self._hash_password(new_password)
        self.save_users()
        return True
