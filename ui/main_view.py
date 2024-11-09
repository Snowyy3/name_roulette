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

    def build(self) -> Row:
        """Builds the main layout of the application.

        Returns:
            Row: The root layout containing the sidebar and content area.
        """
        self.left_sidebar = LeftSidebar(self.handle_view_change)

        # Create the header with proper Row initialization
        header_row = Row(
            controls=[
                ft.Text(self.current_view.name.replace("_", " ").title()),
                Container(expand=True),  # Replaces Spacer
                ft.IconButton(
                    icon=ft.icons.LIST_ALT_ROUNDED,
                    on_click=lambda e: self.handle_view_change(View.MANAGE_LISTS),
                ),
                ft.IconButton(
                    icon=ft.icons.MANAGE_ACCOUNTS,
                    on_click=lambda e: self.handle_view_change(View.USER_ACCOUNTS),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.header = Container(
            content=header_row,
            bgcolor="#CCE0FF",  # Slightly darker than left sidebar
            padding=10,
        )

        # Create main content column with proper initialization
        main_content = Column(
            controls=[
                self.header,
                self.name_generation_view,  # Default view content
            ],
            expand=True,
        )

        # Update content_area with proper initialization
        self.content_area = Container(
            content=main_content,
            expand=True,
        )

        return Row(
            controls=[self.left_sidebar, self.content_area],
            expand=True,
        )

    def handle_view_change(self, view: View):
        self.current_view = view  # Update the current view

        # Update header text using the properly initialized Row
        if isinstance(self.header.content, Row):
            title_text = self.header.content.controls[0]
            if isinstance(title_text, ft.Text):
                title_text.value = view.name.replace("_", " ").title()
                self.header.update()

        # Update content below header with proper type checking
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

            content_column.controls[1] = view_content
            self.content_area.update()

    def on_resize(self, _) -> None:
        if self.page:
            self.left_sidebar.resize(self.page.window.height)
