import flet as ft
from flet import UserControl, Page, Row, Container, Column
from ui.name_generation_view import NameGenerationView
from ui.group_former_view import GroupFormationView
from ui.left_sidebar import LeftSidebar
from ui.views import View


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
        self.current_view = View.NAME_PICKER

        self.manage_lists_btn = ft.IconButton(
            icon=ft.icons.BOOKMARKS_OUTLINED,
            on_click=lambda _: self.handle_view_change(View.MANAGE_LISTS),
        )
        self.user_accounts_btn = ft.IconButton(
            icon=ft.icons.MANAGE_ACCOUNTS_OUTLINED,
            on_click=lambda _: self.handle_view_change(View.USER_ACCOUNTS),
        )

        # Set the AppBar with adjusted icon spacing
        self.page.appbar = ft.AppBar(
            title=ft.Text(self.current_view.name.replace("_", " ").title()),
            bgcolor="#CCE0FF",
            actions=[
                Container(
                    content=Row(
                        controls=[
                            self.manage_lists_btn,
                            self.user_accounts_btn,
                        ],
                        spacing=10,  # Add spacing between icons
                    ),
                    margin=ft.margin.only(right=20),  # Add right margin to move icons away from edge
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
        self.current_view = view
        self.page.appbar.title.value = view.name.replace("_", " ").title()
        self.page.update()

        self.manage_lists_btn.icon = ft.icons.BOOKMARKS if view == View.MANAGE_LISTS else ft.icons.BOOKMARKS_OUTLINED
        self.user_accounts_btn.icon = (
            ft.icons.MANAGE_ACCOUNTS if view == View.USER_ACCOUNTS else ft.icons.MANAGE_ACCOUNTS_OUTLINED
        )
        self.manage_lists_btn.update()
        self.user_accounts_btn.update()

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

            # Ensure we have space for the view content
            if len(content_column.controls) < 2:
                content_column.controls.append(view_content)
            else:
                content_column.controls[1] = view_content

            self.content_area.update()

    def on_resize(self, _) -> None:
        if self.page:
            self.left_sidebar.resize(self.page.window.height)
