import re
import flet as ft
from flet import (
    UserControl,
    Container,
    Column,
    Text,
    TextField,
    Row,
    ElevatedButton,
    TextButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    alignment,
    padding,
    colors,
    FontWeight,
)


class SignUpView(UserControl):
    def __init__(self, page: ft.Page, on_signup=None, on_switch_to_login=None, auth=None):
        super().__init__()
        self.page = page
        self.on_signup = on_signup
        self.on_switch_to_login = on_switch_to_login
        self.controller = auth.auth  # Access the UserAuthenticationController instead

    def _create_input_fields(self):
        self.display_name_field = TextField(
            label="Display Name",
            border_radius=8,
            text_size=16,
            focused_border_color=colors.GREEN,
            focused_border_width=1,
            border_color=colors.with_opacity(0.25, colors.ON_SURFACE),
            height=56,
        )

        self.username_field = TextField(
            label="Username",
            border_radius=8,
            text_size=16,
            focused_border_color=colors.GREEN,
            focused_border_width=1,
            border_color=colors.with_opacity(0.25, colors.ON_SURFACE),
            height=56,
        )

        self.password_field = TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            text_size=16,
            focused_border_color=colors.GREEN,
            focused_border_width=1,
            border_color=colors.with_opacity(0.25, colors.ON_SURFACE),
            height=56,
        )

        self.username_feedback = Text(size=14, color=colors.RED_500, visible=False)
        self.password_feedback = Text(size=14, color=colors.RED_500, visible=False)
        self.error_text = Text(color="#ef4444", size=14, visible=False)

        self.username_field.on_change = self.validate_username
        self.password_field.on_change = self.validate_password

    def _create_signup_button(self):
        return ElevatedButton(
            content=Text("Sign Up", size=16, weight=FontWeight.W_500),
            style=ft.ButtonStyle(
                color=colors.WHITE,
                bgcolor="#10b981",
                padding=padding.symmetric(vertical=20),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=400,
            on_click=self.handle_signup,
        )

    def _create_login_row(self):
        return Row(
            controls=[
                Text("Already have an account? ", size=14, color="#6b7280"),
                TextButton(
                    text="Log in",
                    style=ft.ButtonStyle(color="#10b981", padding=padding.all(0)),
                    on_click=self.switch_to_login,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        )

    def build(self):
        self._create_input_fields()

        return Container(
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text("Create an account", size=28, weight=FontWeight.BOLD, color="#13343b"),
                    Container(height=32),
                    self.display_name_field,
                    self.username_field,
                    self.username_feedback,
                    self.password_field,
                    self.password_feedback,
                    self.error_text,
                    Container(height=16),
                    self._create_signup_button(),
                    self._create_login_row(),
                ],
            ),
            width=400,
            padding=32,
            alignment=alignment.center,
        )

    def handle_signup(self, e):
        self.clear_error()

        is_valid, error_message = self.controller.validate_signup_input(
            self.username_field.value, self.display_name_field.value, self.password_field.value
        )

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
        is_valid, error_message = self.controller.validate_username_availability(username)

        self.username_feedback.value = error_message if not is_valid else ""
        self.username_feedback.visible = not is_valid
        self.update()

    def validate_password(self, e):
        password = self.password_field.value
        is_valid, error_message = self.controller.validate_password_live(password)

        self.password_feedback.value = error_message if not is_valid else ""
        self.password_feedback.visible = not is_valid
        self.update()
