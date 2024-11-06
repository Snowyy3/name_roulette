import flet as ft
from flet import UserControl, Page, Row, Container
from ui.name_generation_view import NameGenerationView
from ui.group_former_view import GroupFormationView
from ui.left_sidebar import LeftSidebar, View


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

        self.content_area = Container(
            content=self.name_generation_view,
            expand=True,
        )

        return Row(
            [self.left_sidebar, self.content_area],
            expand=True,
        )

    def handle_view_change(self, view: View):
        if view == View.NAME_PICKER:
            self.content_area.content = self.name_generation_view
        elif view == View.GROUP_FORMER:
            self.content_area.content = self.group_former_view
        else:  # Settings view
            self.content_area.content = ft.Text("Settings, coming soon!")
        self.content_area.update()

    def on_resize(self, _) -> None:
        if self.page:
            self.left_sidebar.resize(self.page.window.height)
