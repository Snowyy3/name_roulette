import flet as ft
from flet import (
    UserControl,
    Page,
    NavigationRail,
    NavigationRailDestination,
    Row,
    Container,
    Column,
    IconButton,
    Border,
    BorderSide,
    ControlEvent,
)

from ui.name_generation_view import NameGenerationView
from ui.group_former_view import GroupFormationView


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

    def build(self) -> Row: # type: ignore
        """Builds the main layout of the application.

        Returns:
            Row: The root layout containing the sidebar and content area.
        """
        self.menu_button = IconButton(
            icon=ft.icons.MENU,
            on_click=self.toggle_left_sidebar,
        )

        # Left sidebar
        self.left_sidebar = NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=80,
            min_extended_width=180,
            group_alignment=-0.95,
            destinations=[
                NavigationRailDestination(
                    label="Name Picker",
                    icon=ft.icons.SHUFFLE_OUTLINED,
                    selected_icon=ft.icons.SHUFFLE_ROUNDED,
                    padding=10,
                ),
                NavigationRailDestination(
                    label="Group Randomizer",
                    icon=ft.icons.GROUPS_2_OUTLINED,
                    selected_icon=ft.icons.GROUPS_2_ROUNDED,
                    padding=10,
                ),
                NavigationRailDestination(
                    label="Settings",
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                    padding=10,
                ),
            ],
            on_change=self.change_left_sidebar,
            bgcolor=ft.colors.TRANSPARENT,  # Make the NavigationRail background transparent (to make the color defined below works for all the sidebar)
        )

        # Left sidebar container
        self.left_sidebar_container = Container(
            content=Column(
                [
                    Container(
                        content=self.menu_button,
                        margin=ft.margin.only(top=16, left=8, bottom=16),
                    ),
                    Container(
                        content=self.left_sidebar,
                        expand=True,
                        height=(self.page.window.height - 100 if self.page and self.page.window.height else 0),  # Subtract space for menu button
                    ),
                ],
                expand=True,
            ),
            bgcolor="#E6F3FF",  # Left sidebar color (Pastel light blue)
            width=60,
            border=Border(right=BorderSide(width=1, color=ft.colors.OUTLINE)),
            animate=ft.animation.Animation(200, ft.animation.AnimationCurve.EASE_OUT_CUBIC),
        )

        self.content_area = Container(
            content=self.name_generation_view,
            expand=True,
        )

        return Row(
            [self.left_sidebar_container, self.content_area],
            expand=True,
        )

    def toggle_left_sidebar(self, event: ControlEvent) -> None:
        """Toggles the expanded state of the left sidebar."""
        self.left_sidebar.extended = not self.left_sidebar.extended
        self.left_sidebar.label_type = (
            ft.NavigationRailLabelType.ALL
            if self.left_sidebar.extended
            else ft.NavigationRailLabelType.NONE
        )
        self.left_sidebar_container.width = 200 if self.left_sidebar.extended else 60
        self.left_sidebar_container.update()
        self.left_sidebar.update()

    def change_left_sidebar(self, event: ControlEvent) -> None:
        """Handles changes in the selected index of the left sidebar navigation."""
        selected_index = event.control.selected_index
        if selected_index == 0:
            self.content_area.content = self.name_generation_view
        elif selected_index == 1:
            self.content_area.content = self.group_former_view
        elif selected_index == 2:
            self.content_area.content = ft.Text("Settings, coming soon!")
        self.content_area.update()

    def on_resize(self, event) -> None:
        """Updates the height of the left sidebar container on window resize."""
        if self.page:
            self.left_sidebar_container.height = self.page.window.height
            self.left_sidebar_container.update()