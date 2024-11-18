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
    Icon,
    Divider,
    MainAxisAlignment,
    CrossAxisAlignment,
    alignment,
    padding,
    margin,
    icons,
    colors,
    FontWeight,
    SnackBar,
)


class LoginView(UserControl):
    def __init__(self, page: ft.Page, on_login=None, on_switch_to_signup=None, auth=None):
        super().__init__()
        self.page = page
        self.on_login = on_login
        self.on_switch_to_signup = on_switch_to_signup
        self.controller = auth.auth  # Access the UserAuthenticationController instead

    def _create_input_fields(self):
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

        self.error_text = Text(color=colors.RED_500, size=14, visible=False)

    def _create_forgot_password_link(self):
        return Container(
            content=Text("Forgot Password?", color="#10b981", size=14),
            alignment=alignment.center_right,
            margin=margin.only(top=0, bottom=8),
            on_click=self.handle_forgot_password,
        )

    def _create_login_button(self):
        return ElevatedButton(
            content=Text("Continue", size=16, weight=FontWeight.W_500),
            style=ft.ButtonStyle(
                color=colors.WHITE,
                bgcolor="#10b981",
                padding=padding.symmetric(vertical=20),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=400,
            on_click=self.handle_login,
        )

    def _create_signup_row(self):
        return Row(
            controls=[
                Text("New here? ", size=14, color="#6b7280"),
                TextButton(
                    text="Sign up",
                    style=ft.ButtonStyle(color="#10b981", padding=padding.only(top=0, bottom=0)),
                    on_click=self.switch_to_signup,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        )

    def _create_divider_section(self):
        return Container(
            content=Row(
                controls=[
                    Divider(color="#e0e0e0", thickness=1),
                    Text("OR", size=14, color="#6b7280"),
                    Divider(color="#e0e0e0", thickness=1),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            padding=padding.symmetric(vertical=16),
        )

    def _create_guest_button(self):
        return TextButton(
            content=Row(
                controls=[
                    Icon(icons.PERSON_OFF, color="#6b7280"),
                    Text("Continue as Guest", color="#6b7280"),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                bgcolor=colors.SURFACE_VARIANT,
                padding=padding.symmetric(vertical=20),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=400,
            on_click=self.handle_guest_login,
        )

    def build(self) -> Container:
        self._create_input_fields()

        return Container(
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text("Welcome back", size=28, weight=FontWeight.BOLD, color="#13343b"),
                    Container(height=32),
                    self.username_field,
                    self.password_field,
                    self._create_forgot_password_link(),
                    self.error_text,
                    self._create_login_button(),
                    self._create_signup_row(),
                    self._create_divider_section(),
                    self._create_guest_button(),
                ],
            ),
            width=400,
            padding=32,
            alignment=alignment.center,
        )

    def handle_login(self, e):
        self.clear_error()

        is_valid, error_message = self.controller.validate_login_input(
            self.username_field.value, self.password_field.value
        )

        if not is_valid:
            self.show_error(error_message)
            return

        if self.on_login:
            self.on_login(self.username_field.value, self.password_field.value)

    def handle_guest_login(self, e):
        if self.on_login:
            self.on_login(None, None)  # Pass None to indicate guest login

    def handle_forgot_password(self, e):
        # Create references to the input fields
        self.reset_username_field = ft.TextField(label="Username", border_radius=8, text_size=16, height=56)
        self.reset_password_field = ft.TextField(
            label="New Password", password=True, can_reveal_password=True, border_radius=8, text_size=16, height=56
        )

        self.page.dialog = ft.AlertDialog(
            title=Text("Reset Password"),
            content=Container(
                width=400,
                content=Column(
                    tight=True,
                    controls=[
                        self.reset_username_field,
                        Container(height=16),
                        self.reset_password_field,
                    ],
                ),
            ),
            actions=[
                TextButton("Cancel", on_click=self.close_dialog),
                TextButton("Reset", on_click=self.reset_password),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

    def reset_password(self, e):
        username = self.reset_username_field.value
        new_password = self.reset_password_field.value

        if not username or not new_password:
            self.page.snack_bar = SnackBar(Text("Please fill in all fields"), open=True)
            self.page.update()
            return

        success, message = self.controller.reset_password(username, new_password)

        if success:
            self.page.dialog.open = False
            self.page.show_snack_bar(SnackBar(Text("Password reset successfully"), bgcolor="#10b981"))
        else:
            self.page.show_snack_bar(SnackBar(Text(message), bgcolor="#ef4444"))
        self.page.update()

    def switch_to_signup(self, e):
        if self.on_switch_to_signup:
            self.on_switch_to_signup()

    def show_error(self, message: str):
        self.error_text.value = message
        self.error_text.visible = True
        self.error_text.color = "#ef4444"  # Set error color to red
        self.update()

    def clear_error(self):
        self.error_text.visible = False
        self.update()
