import flet as ft


class LoginView(ft.UserControl):
    def __init__(self, page: ft.Page, on_login=None, on_switch_to_signup=None, auth=None):
        super().__init__()
        self.page = page
        self.on_login = on_login
        self.on_switch_to_signup = on_switch_to_signup
        self.auth = auth  # Use the shared instance

    def build(self):
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

        self.error_text = ft.Text(color=ft.colors.RED_500, size=14, visible=False)

        return ft.Container(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Welcome back",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#13343b",
                    ),
                    ft.Container(height=32),  # Spacing
                    self.username_field,
                    ft.Container(height=16),  # Spacing
                    self.password_field,
                    ft.Container(
                        content=ft.Text(
                            "Forgot Password?",
                            color="#10b981",
                            size=14,
                        ),
                        alignment=ft.alignment.center_right,
                        margin=ft.margin.only(top=8, bottom=16),
                        on_click=self.handle_forgot_password,
                    ),
                    self.error_text,
                    ft.Container(height=16),  # Spacing
                    ft.ElevatedButton(
                        content=ft.Text(
                            "Continue",
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
                        on_click=self.handle_login,
                    ),
                    ft.Container(height=16),  # Spacing
                    ft.Row(
                        controls=[
                            ft.Text("New here? ", size=14, color="#6b7280"),
                            ft.TextButton(  # Changed from Text to TextButton
                                text="Sign up",
                                style=ft.ButtonStyle(
                                    color="#10b981",
                                    padding=ft.padding.all(0),
                                ),
                                on_click=self.switch_to_signup,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Divider(color="#e0e0e0", thickness=1),
                                ft.Text("OR", size=14, color="#6b7280"),
                                ft.Divider(color="#e0e0e0", thickness=1),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        margin=ft.margin.symmetric(vertical=16),
                    ),
                    ft.TextButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.PERSON_OFF, color="#6b7280"),
                                ft.Text("Continue as Guest", color="#6b7280"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        width=400,
                        on_click=self.handle_guest_login,
                    ),
                ],
            ),
            width=400,
            padding=32,
            alignment=ft.alignment.center,
        )

    def validate_input(self) -> tuple[bool, str]:
        """Validate login form input fields.

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not self.username_field.value:
            return False, "Username is required"
        if not self.password_field.value:
            return False, "Password is required"
        if len(self.username_field.value) < 3:
            return False, "Username must be at least 3 characters long"
        if len(self.password_field.value) < 6:
            return False, "Password must be at least 6 characters long"
        return True, ""

    def handle_login(self, e):
        # Clear any previous errors
        self.clear_error()

        # Validate input
        is_valid, error_message = self.validate_input()
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
            title=ft.Text("Reset Password"),
            content=ft.Container(
                width=400,
                content=ft.Column(
                    tight=True,
                    controls=[
                        self.reset_username_field,
                        ft.Container(height=16),
                        self.reset_password_field,
                    ],
                ),
            ),
            actions=[
                ft.TextButton("Cancel", on_click=self.close_dialog),
                ft.TextButton("Reset", on_click=self.reset_password),
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
            self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields"), open=True)
            self.page.update()
            return

        if username in self.auth.users["users"]:
            # Hash the new password before saving
            hashed_password = self.auth._hash_password(new_password)
            self.auth.users["users"][username]["password"] = hashed_password
            self.auth.save_users()
            self.page.snack_bar = ft.SnackBar(ft.Text("Password reset successfully"), open=True)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username not found"), open=True)

        self.page.dialog.open = False
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
