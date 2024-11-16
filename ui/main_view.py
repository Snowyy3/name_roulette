import flet as ft
from flet import UserControl, Page, Row, Container, Column
from ui.name_generation_view import NameGenerationView
from ui.group_former_view import GroupFormationView
from ui.left_sidebar import LeftSidebar
from ui.views import View
from .login_view import LoginView
from .signup_view import SignUpView


class MainView(UserControl):
    """
    Main view for the Name Roulette application, managing navigation and content display.

    Args:
        page (Page): The Flet Page instance.
        controller (MainController): The controller managing application logic.
    """

    def __init__(self, page: Page, controller) -> None:
        super().__init__()
        self.page = page
        self.controller = controller
        self.name_generation_view = NameGenerationView(self.controller)
        self.group_former_view = GroupFormationView(self.controller)
        self.page.on_resize = self.on_resize
        self.current_view = View.NAME_PICKER  # Default to NAME_PICKER instead of LOGIN
        self.previous_view = None  # Track previous view

        self.login_view = LoginView(
            page=self.page, on_login=self.handle_login, on_switch_to_signup=lambda: self.handle_view_change(View.SIGNUP)
        )

        self.signup_view = SignUpView(
            page=self.page, on_signup=self.handle_signup, on_switch_to_login=lambda: self.handle_view_change(View.LOGIN)
        )

        self.manage_lists_btn = ft.IconButton(
            icon=ft.icons.BOOKMARKS_OUTLINED,
            on_click=lambda _: self.handle_view_change(View.MANAGE_LISTS),
        )

        self.user_account_button = ft.PopupMenuButton(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.PERSON_OFF_ROUNDED, color="#6b7280"),  # Default to guest icon
                        ft.Text("Guest", size=14, color="#6b7280"),
                        ft.Icon(ft.icons.ARROW_DROP_DOWN, color="#6b7280"),
                    ],
                    tight=True,
                ),
                padding=ft.padding.all(8),
                border_radius=20,
                bgcolor=ft.colors.SURFACE_VARIANT,
            ),
            items=[ft.PopupMenuItem(text="Log In", on_click=lambda _: self.handle_view_change(View.LOGIN))],
        )

        # Update AppBar with user account button
        self.page.appbar = ft.AppBar(
            title=ft.Text(self.current_view.name.replace("_", " ").title()),
            bgcolor="#CCE0FF",
            actions=[
                Container(
                    content=Row(
                        controls=[
                            self.manage_lists_btn,
                            self.user_account_button,  # Replace user_account_button with user_account_button
                        ],
                        spacing=10,
                    ),
                    margin=ft.margin.only(right=20),
                )
            ],
        )

    def build(self) -> Row:
        """Builds the main layout of the application.

        Returns:
            Row: The root layout containing the sidebar and content area.
        """
        self.left_sidebar = LeftSidebar(self.handle_view_change)

        # Create main content column with top alignment and padding
        main_content = Column(
            controls=[
                Container(
                    height=40,  # Add spacing at top
                ),
                self.name_generation_view,  # Default view content
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            spacing=0,  # Ensure no extra spacing between containers
        )

        # Update content_area with top alignment
        self.content_area = Container(
            content=main_content,
            expand=True,
            alignment=ft.alignment.top_left,
        )

        return Row(
            controls=[self.left_sidebar, self.content_area],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def handle_view_change(self, view: View):
        """Handle view changes by updating the AppBar title and content area.

        Args:
            view (View): The view to switch to.
        """
        # Store previous view before changing, but only if not switching between LOGIN/SIGNUP
        if self.current_view not in [View.LOGIN, View.SIGNUP] or view not in [View.LOGIN, View.SIGNUP]:
            self.previous_view = self.current_view

        self.current_view = view
        self.page.appbar.title.value = view.name.replace("_", " ").title()
        self.page.update()

        self.manage_lists_btn.icon = ft.icons.BOOKMARKS if view == View.MANAGE_LISTS else ft.icons.BOOKMARKS_OUTLINED
        self.user_account_button.icon = (
            ft.icons.MANAGE_ACCOUNTS if view == View.USER_ACCOUNTS else ft.icons.MANAGE_ACCOUNTS_OUTLINED
        )
        self.manage_lists_btn.update()
        self.user_account_button.update()

        # Update content
        if isinstance(self.content_area.content, Column):
            content_column = self.content_area.content

            if view == View.NAME_PICKER:
                view_content = self.name_generation_view
            elif view == View.GROUP_FORMER:
                view_content = self.group_former_view
            elif view == View.SETTINGS:
                view_content = ft.Text("Settings, coming soon!")
            elif view == View.MANAGE_LISTS:
                view_content = ft.Text("Manage Lists, coming soon!")
            elif view == View.USER_ACCOUNTS:
                view_content = ft.Text("User Accounts, coming soon!")
            elif view == View.LOGIN:
                view_content = self.login_view
            elif view == View.SIGNUP:
                view_content = self.signup_view

            # Ensure we have space for the view content
            if len(content_column.controls) < 2:
                content_column.controls.append(view_content)
            else:
                content_column.controls[1] = view_content

            self.content_area.update()

    def on_resize(self, _) -> None:
        if self.page:
            self.left_sidebar.resize(self.page.window.height)

    def handle_login(self, username: str, password: str):
        """Handle login with navigation to previous view."""
        if self.controller.auth.handle_login(username, password):
            self.update_user_display()
            # Return to previous view or NAME_PICKER if none
            target_view = self.previous_view if self.previous_view else View.NAME_PICKER
            self.handle_view_change(target_view)
            # Show welcome message with user's name
            user = self.controller.auth.get_current_user()
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Welcome{' back' if username else ''}, {user['display_name']}!"),
                    bgcolor="#10b981",  # Green background
                    duration=2000,  # 2 seconds
                )
            )
        else:
            self.login_view.show_error("Invalid username or password")

    def handle_signup(self, username: str, display_name: str, password: str):
        """Handle signup with success message."""
        if self.controller.auth.handle_signup(username, display_name, password):
            self.handle_view_change(View.LOGIN)
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Account created successfully! Please log in."),
                    bgcolor="#10b981",  # Green background
                    duration=2000,  # 2 seconds
                )
            )
        else:
            self.signup_view.show_error("Username already exists")

    def handle_logout(self, e=None):
        self.controller.auth.handle_logout()
        self.update_user_display()
        self.handle_view_change(View.LOGIN)

    def update_user_display(self):
        """Update user account button display based on login state"""
        user = self.controller.auth.get_current_user()
        button_content = self.user_account_button.content.content.controls

        # Update icon and text
        if user["username"] is None:  # Guest mode
            button_content[0].name = ft.icons.PERSON_OFF_ROUNDED
            button_content[1].value = "Guest"
            # Update menu items for guest
            self.user_account_button.items = [
                ft.PopupMenuItem(text="Log In", on_click=lambda _: self.handle_view_change(View.LOGIN))
            ]
        else:  # Logged in user
            button_content[0].name = ft.icons.MANAGE_ACCOUNTS_ROUNDED
            button_content[1].value = user["display_name"]
            # Update menu items for logged in user
            self.user_account_button.items = [
                ft.PopupMenuItem(text="Change Password", on_click=self.show_change_password_dialog),
                ft.PopupMenuItem(text="Log Out", on_click=self.handle_logout),
            ]

        # Update colors based on state
        for control in button_content:
            control.color = "#6b7280"

        self.user_account_button.update()

    def show_change_password_dialog(self, e):
        def handle_save_password(e):
            try:
                self.controller.auth.change_password(
                    self.controller.auth.current_user["username"], current_password.value, new_password.value
                )
                dialog.open = False
                self.page.update()
                self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Password changed successfully")))
            except ValueError as err:
                error_text.value = str(err)
                error_text.visible = True
                self.page.update()

        current_password = ft.TextField(label="Current Password", password=True, can_reveal_password=True)
        new_password = ft.TextField(label="New Password", password=True, can_reveal_password=True)
        error_text = ft.Text(color="red", visible=False)

        dialog = ft.AlertDialog(
            title=ft.Text("Change Password"),
            content=ft.Column(
                controls=[
                    current_password,
                    new_password,
                    error_text,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, "open", False)),
                ft.TextButton("Save", on_click=handle_save_password),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
