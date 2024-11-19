import flet as ft
from flet import (
    UserControl,
    Page,
    Row,
    Column,
    Container,
    Text,
    IconButton,
    PopupMenuButton,
    PopupMenuItem,
    TextField,
    TextButton,
    AlertDialog,
    SnackBar,
    MainAxisAlignment,
    CrossAxisAlignment,
    alignment,
    padding,
    margin,
    colors,
    Icon,
    TextAlign,
)
from ui.name_generation_view import NameGenerationView
from ui.group_former_view import GroupFormationView
from ui.left_sidebar import LeftSidebar
from ui.views import View
from ui.login_view import LoginView
from ui.signup_view import SignUpView


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
            page=self.page,
            on_login=self.handle_login,
            on_switch_to_signup=lambda: self.handle_view_change(View.SIGNUP),
            auth=controller,  # Pass controller instead of auth
        )

        self.signup_view = SignUpView(
            page=self.page,
            on_signup=self.handle_signup,
            on_switch_to_login=lambda: self.handle_view_change(View.LOGIN),
            auth=controller,  # Pass controller instead of auth
        )

        self.manage_lists_btn = ft.IconButton(
            icon=ft.icons.BOOKMARKS_OUTLINED,
            on_click=lambda _: self.handle_view_change(View.MANAGE_LISTS),
        )

        self.user_account_button = ft.PopupMenuButton(
            content=Container(
            content=Row(
                controls=[
                Icon(ft.icons.PERSON_OFF_ROUNDED, color="#6b7280"),  # Default to guest icon
                Text("Guest", size=14, color="#6b7280"),
                Icon(ft.icons.ARROW_DROP_DOWN, color="#6b7280"),
                ],
                tight=True,
            ),
            padding=ft.padding.all(8),
            border_radius=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            ink=False,  # Disable hover effect
            ),
            items=[
            PopupMenuItem(
                text="Log In",
                on_click=lambda _: self.handle_view_change(View.LOGIN),
            )
            ],
        )

        # Update AppBar with user account button
        self.page.appbar = ft.AppBar(
            title=Text(self.current_view.name.replace("_", " ").title()),
            bgcolor="#CCE0FF",
            actions=[
                Container(
                    content=Row(
                        controls=[
                            self.manage_lists_btn,
                            self.user_account_button,
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
            alignment=ft.alignment.center,
            # alignment=ft.alignment.top_left,
        )

        return Row(
            controls=[self.left_sidebar, self.content_area],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def handle_view_change(self, view: View):
        """Handle view changes by updating the AppBar title and content area."""
        self._update_previous_view(view)
        self._update_appbar(view)
        self._update_content_area(view)

    def _update_previous_view(self, view: View):
        if self.current_view not in [View.LOGIN, View.SIGNUP] or view not in [View.LOGIN, View.SIGNUP]:
            self.previous_view = self.current_view
        self.current_view = view

    def _update_appbar(self, view: View):
        self.page.appbar.title.value = view.name.replace("_", " ").title()
        self.manage_lists_btn.icon = ft.icons.BOOKMARKS if view == View.MANAGE_LISTS else ft.icons.BOOKMARKS_OUTLINED
        self.user_account_button.icon = (
            ft.icons.MANAGE_ACCOUNTS if view == View.USER_ACCOUNTS else ft.icons.MANAGE_ACCOUNTS_OUTLINED
        )
        self._update_ui_elements()

    def _update_ui_elements(self):
        self.page.update()
        self.manage_lists_btn.update()
        self.user_account_button.update()

    def _update_content_area(self, view: View):
        if not isinstance(self.content_area.content, Column):
            return

        content_column = self.content_area.content
        content_column.controls.clear()

        self._set_column_alignment(content_column, view)
        view_content = self._get_view_content(view)
        content_column.controls.append(view_content)
        self.content_area.update()

    def _set_column_alignment(self, column: Column, view: View):
        if view in [View.LOGIN, View.SIGNUP]:
            column.alignment = ft.MainAxisAlignment.CENTER
        else:
            column.alignment = ft.MainAxisAlignment.START
            column.controls.append(Container(height=40))

    def _get_view_content(self, view: View):
        view_map = {
            View.NAME_PICKER: self.name_generation_view,
            View.GROUP_FORMER: self.group_former_view,
            View.SETTINGS: Text("Settings, coming soon!"),
            View.MANAGE_LISTS: Text("Manage Lists, coming soon!"),
            View.USER_ACCOUNTS: Text("User Accounts, coming soon!"),
            View.LOGIN: self.login_view,
            View.SIGNUP: self.signup_view,
        }
        return view_map.get(view, Text("Page not found"))

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
                SnackBar(
                    content=Text(f"Welcome{' back' if username else ''}, {user['display_name']}!"),
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
                SnackBar(
                    content=Text("Account created successfully! Please log in."),
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
        self._update_button_appearance(user)
        self._update_menu_items(user)
        self.user_account_button.update()

    def _update_button_appearance(self, user):
        button_content = self.user_account_button.content.content.controls
        is_guest = user["username"] is None

        icon_name = ft.icons.PERSON_OFF_ROUNDED if is_guest else ft.icons.MANAGE_ACCOUNTS_ROUNDED
        display_text = "Guest" if is_guest else user["display_name"]
        button_color = "#6b7280" if is_guest else "#0b855d"

        button_content[0].name = icon_name
        button_content[1].value = display_text

        for control in button_content:
            control.color = button_color

    def _update_menu_items(self, user):
        if user["username"] is None:
            self.user_account_button.items = [
                PopupMenuItem(text="Log In", on_click=lambda _: self.handle_view_change(View.LOGIN))
            ]
        else:
            self.user_account_button.items = [
                PopupMenuItem(text="Change Password", on_click=self.show_change_password_dialog),
                PopupMenuItem(text="Log Out", on_click=self.handle_logout),
            ]

    def show_change_password_dialog(self, e):
        dialog = self._create_password_dialog()
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _create_password_dialog(self):
        password_fields = self._create_password_fields()
        feedback_texts = self._create_feedback_texts()

        return ft.AlertDialog(
            title=Text("Change Password"),
            content=Container(
                width=400,
                content=ft.Column(tight=True, controls=self._get_dialog_controls(password_fields, feedback_texts)),
            ),
            actions=[
                TextButton("Cancel", on_click=lambda e: self._close_dialog()),
                TextButton("Save", on_click=lambda e: self._handle_password_save(password_fields, feedback_texts)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _create_password_fields(self):
        current_password = TextField(
            label="Current Password", password=True, can_reveal_password=True, border_radius=8, text_size=16, height=56
        )

        new_password = TextField(
            label="New Password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            text_size=16,
            height=56,
            on_change=self._validate_new_password,
        )

        confirm_password = TextField(
            label="Confirm New Password",
            password=True,
            can_reveal_password=True,
            border_radius=8,
            text_size=16,
            height=56,
            on_change=self._validate_confirm_password,
        )

        return current_password, new_password, confirm_password

    def _create_feedback_texts(self):
        password_feedback = Text(size=14, color="#ef4444", visible=False)
        confirm_feedback = Text(size=14, color="#ef4444", visible=False)
        error_text = Text(color="#ef4444", size=14, visible=False, text_align=TextAlign.CENTER)

        return password_feedback, confirm_feedback, error_text

    def _get_dialog_controls(self, password_fields, feedback_texts):
        current_password, new_password, confirm_password = password_fields
        password_feedback, confirm_feedback, error_text = feedback_texts

        return [
            current_password,
            Container(height=8),
            new_password,
            password_feedback,
            Container(height=8),
            confirm_password,
            confirm_feedback,
            Container(height=8),
            error_text,
        ]

    def _validate_new_password(self, e):
        password = e.control.value
        password_feedback = e.control.page.dialog.content.content.controls[3]
        confirm_password = e.control.page.dialog.content.content.controls[6]
        confirm_feedback = e.control.page.dialog.content.content.controls[7]

        is_valid, error_message = self.controller.auth.validation.validate_password(password)

        password_feedback.value = error_message
        password_feedback.visible = not is_valid
        password_feedback.color = "#ef4444" if not is_valid else "#10b981"

        if confirm_password.value and password != confirm_password.value:
            confirm_feedback.value = "Passwords do not match"
            confirm_feedback.visible = True
        else:
            confirm_feedback.visible = False

        e.control.page.update()

    def _validate_confirm_password(self, e):
        new_password = e.control.page.dialog.content.content.controls[2]
        confirm_feedback = e.control.page.dialog.content.content.controls[7]
        if new_password.value != e.control.value:
            confirm_feedback.value = "Passwords do not match"
            confirm_feedback.visible = True
        else:
            confirm_feedback.visible = False
        e.control.page.update()

    def _handle_password_save(self, password_fields, feedback_texts):
        current_password, new_password, confirm_password = password_fields
        error_text = feedback_texts[2]

        if not current_password.value or not new_password.value or not confirm_password.value:
            error_text.value = "Please fill in all fields"
            error_text.visible = True
            self.page.update()
            return

        if new_password.value != confirm_password.value:
            error_text.value = "Passwords do not match"
            error_text.visible = True
            self.page.update()
            return

        try:
            self.controller.auth.change_password(
                self.controller.auth.current_user["username"], current_password.value, new_password.value
            )
            self._close_dialog()
            self.page.show_snack_bar(SnackBar(content=Text("Password changed successfully"), bgcolor="#10b981"))
        except ValueError as err:
            error_text.value = str(err)
            error_text.visible = True
            self.page.update()

    def _close_dialog(self):
        self.page.dialog.open = False
        self.page.update()
