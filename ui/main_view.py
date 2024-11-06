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
            group_alignment=-0.95,  # Top group alignment
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
            ],
            on_change=self.change_left_sidebar,
            bgcolor=ft.colors.TRANSPARENT,
        )

        # Bottom navigation rail for settings
        self.bottom_nav = NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=80,  # Remember to match top rail width
            min_extended_width=180,
            group_alignment=0,  # This pushes content to bottom
            destinations=[
                NavigationRailDestination(
                    label="Settings",
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                    padding=10,
                ),
            ],
            on_change=self.change_bottom_nav,
            bgcolor=ft.colors.TRANSPARENT,
        )

        # Left sidebar container with fixed heights (very important)
        self.left_sidebar_container = Container(
            content=Column(
                [
                    Container(  # Menu button container
                        content=self.menu_button,
                        margin=ft.margin.only(top=16, left=16, bottom=16),
                        height=60,
                    ),
                    Container(  # Main navigation container
                        content=self.left_sidebar,
                        height=160,  # Fixed height for main navigation
                    ),
                    Container(  # Spacer
                        expand=True,
                    ),
                    Container(  # Settings navigation container
                        content=self.bottom_nav,
                        height=140,  # Fixed height for settings
                        margin=ft.margin.only(bottom=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            ),
            bgcolor="#E6F3FF",
            width=100,  # Increased from 60
            height=self.page.window.height if self.page else 600,  # Ensure full height
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
        self.bottom_nav.extended = self.left_sidebar.extended  # Also toggle bottom nav
        
        label_type = (
            ft.NavigationRailLabelType.ALL 
            if self.left_sidebar.extended 
            else ft.NavigationRailLabelType.NONE
        )
        self.left_sidebar.label_type = label_type
        self.bottom_nav.label_type = label_type
        
        self.left_sidebar_container.width = 200 if self.left_sidebar.extended else 100  # Updated from 60
        self.left_sidebar_container.update()
        self.left_sidebar.update()
        self.bottom_nav.update()

    def change_bottom_nav(self, event: ControlEvent) -> None:
        """Handles changes in the selected index of the bottom navigation."""
        self.left_sidebar.selected_index = None  # Deselect top nav
        self.content_area.content = ft.Text("Settings, coming soon!")
        self.content_area.update()

    def change_left_sidebar(self, event: ControlEvent) -> None:
        """Handles changes in the selected index of the left sidebar navigation."""
        self.bottom_nav.selected_index = None  # Deselect bottom nav
        selected_index = event.control.selected_index
        if selected_index == 0:
            self.content_area.content = self.name_generation_view
        elif selected_index == 1:
            self.content_area.content = self.group_former_view
        self.content_area.update()

    def on_resize(self, event) -> None:
        """Updates the height of the left sidebar container on window resize."""
        if self.page:
            self.left_sidebar_container.height = self.page.window.height
            self.left_sidebar_container.update()
