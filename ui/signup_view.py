import flet as ft
import re


class SignUpView(ft.UserControl):
    def __init__(self, page: ft.Page, on_signup=None, on_switch_to_login=None, auth=None):
        super().__init__()
        self.page = page
        self.on_signup = on_signup
        self.on_switch_to_login = on_switch_to_login
        self.auth = auth  # Use the shared instance

    def build(self):
        self.display_name_field = ft.TextField(
            label="Display Name",
            border_radius=8,
            text_size=16,
            focused_border_color=ft.colors.GREEN,
            border_color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
            height=56,
        )

        self.username_field = ft.TextField(
            label="Username",
            border_radius=8,
            text_size=16,
            focused_border_color=ft.colors.GREEN,
            border_color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
            height=56,
        )

        self.password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            text_size=16,
            focused_border_color=ft.colors.GREEN,
            border_color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
            height=56,
        )

        self.username_feedback = ft.Text(
            size=14,
            color=ft.colors.RED_500,
            visible=False,
        )

        self.password_feedback = ft.Text(
            size=14,
            color=ft.colors.RED_500,
            visible=False,
        )

        self.username_field.on_change = self.validate_username
        self.password_field.on_change = self.validate_password

        self.error_text = ft.Text(
            color="#ef4444",  # Red color for errors
            size=14,
            visible=False,
        )

        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Create an account",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#13343b",
                    ),
                    ft.Container(height=32),
                    self.display_name_field,
                    ft.Container(height=16),
                    self.username_field,
                    self.username_feedback,
                    ft.Container(height=16),
                    self.password_field,
                    self.password_feedback,
                    ft.Container(height=16),
                    self.error_text,
                    ft.Container(height=16),
                    ft.ElevatedButton(
                        content=ft.Text(
                            "Sign Up",
                            size=16,
                            weight=ft.FontWeight.W_500,
                        ),
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor="#10b981",
                            padding=ft.padding.symmetric(vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        width=400,
                        on_click=self.handle_signup,
                    ),
                    ft.Container(height=16),
                    ft.Row(
                        controls=[
                            ft.Text("Already have an account? ", size=14, color="#6b7280"),
                            ft.TextButton(  # Changed from Text to TextButton
                                text="Log in",
                                style=ft.ButtonStyle(
                                    color="#10b981",
                                    padding=ft.padding.all(0),
                                ),
                                on_click=self.switch_to_login,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
            width=400,
            padding=32,
            alignment=ft.alignment.center,
        )

    def validate_input(self) -> tuple[bool, str]:
        """Validate sign-up form input fields.

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        # Display name validation
        if not self.display_name_field.value:
            return False, "Display name is required"
        if len(self.display_name_field.value) < 2:
            return False, "Display name must be at least 2 characters long"

        # Username validation
        if not self.username_field.value:
            return False, "Username is required"
        if len(self.username_field.value) < 3:
            return False, "Username must be at least 3 characters long"
        if not re.match(r"^[a-zA-Z0-9_]+$", self.username_field.value):
            return False, "Username can only contain letters, numbers, and underscores"

        # Password validation
        if not self.password_field.value:
            return False, "Password is required"
        if len(self.password_field.value) < 6:
            return False, "Password must be at least 6 characters long"
        if not any(c.isupper() for c in self.password_field.value):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in self.password_field.value):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in self.password_field.value):
            return False, "Password must contain at least one number"

        return True, ""

    def handle_signup(self, e):
        # Clear any previous errors
        self.clear_error()

        # Validate input
        is_valid, error_message = self.validate_input()
        if not is_valid:
            self.show_error(error_message)
            return

        if self.on_signup:
            self.on_signup(self.username_field.value, self.display_name_field.value, self.password_field.value)

    def show_error(self, message: str):
        self.error_text.value = message
        self.error_text.visible = True
        self.update()

    def clear_error(self):
        self.error_text.visible = False
        self.update()

    def switch_to_login(self, e):
        if self.on_switch_to_login:
            self.on_switch_to_login()

    def validate_username(self, e):
        username = self.username_field.value
        if len(username) < 3:
            self.username_feedback.value = "Username must be at least 3 characters long"
            self.username_feedback.visible = True
        elif not re.match(r"^[a-zA-Z0-9_]+$", username):
            self.username_feedback.value = "Username can only contain letters, numbers, and underscores"
            self.username_feedback.visible = True
        elif username in self.auth.users["users"]:
            self.username_feedback.value = "Username already exists"
            self.username_feedback.visible = True
        else:
            self.username_feedback.visible = False
        self.update()

    def validate_password(self, e):
        password = self.password_field.value
        if len(password) < 6:
            self.password_feedback.value = "Password must be at least 6 characters long"
            self.password_feedback.visible = True
        elif not any(c.isupper() for c in password):
            self.password_feedback.value = "Password must contain at least one uppercase letter"
            self.password_feedback.visible = True
        elif not any(c.islower() for c in password):
            self.password_feedback.value = "Password must contain at least one lowercase letter"
            self.password_feedback.visible = True
        elif not any(c.isdigit() for c in password):
            self.password_feedback.value = "Password must contain at least one number"
            self.password_feedback.visible = True
        else:
            self.password_feedback.visible = False
        self.update()
