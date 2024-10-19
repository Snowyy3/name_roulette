import flet as ft
from flet import (
    UserControl,
    Page,
    NavigationRail,
    NavigationRailDestination,
    Row,
    Container,
)
from flet import ControlEvent

from ui.name_generation_view import NameGenerationView


class MainView(UserControl):
    def __init__(self, page: Page, controller) -> None:
        super().__init__()
        self.page = page
        self.controller = controller
        self.name_generation_view = NameGenerationView(self.controller)

    def build(self) -> Row:  # type: ignore
        # Left sidebar
        self.left_sidebar = NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=60,
            min_extended_width=200,
            leading=ft.IconButton(icon=ft.icons.MENU, on_click=self.toggle_left_sidebar),
            group_alignment=-0.9,
            destinations=[
                NavigationRailDestination(
                    label="Name Picker",
                    icon=ft.icons.SHUFFLE_ROUNDED,
                    selected_icon=ft.icons.SHUFFLE_ROUNDED,
                ),
                NavigationRailDestination(
                    label="Group Randomizer",
                    icon=ft.icons.GROUPS_2_ROUNDED,
                    selected_icon=ft.icons.GROUPS_2_ROUNDED,
                ),
                NavigationRailDestination(
                    label="Settings",
                    icon=ft.icons.SETTINGS,
                    selected_icon=ft.icons.SETTINGS,
                ),
            ],
            on_change=self.change_left_sidebar,
        )

        # Left sidebar container
        self.left_sidebar_container = Container(
            content=self.left_sidebar,
            bgcolor=ft.colors.PRIMARY_CONTAINER,
            width=60,
            height=self.page.window.height if self.page else None,
            animate=ft.animation.Animation(200, ft.animation.AnimationCurve.EASE_OUT_CUBIC),
        )

        self.content_area = Container(
            content=self.name_generation_view,
            expand=True,
        )

        return Row([
            self.left_sidebar_container,
            self.content_area
        ])

    def toggle_left_sidebar(self, event: ControlEvent) -> None:
        self.left_sidebar.extended = not self.left_sidebar.extended
        self.left_sidebar.label_type = (
            ft.NavigationRailLabelType.ALL if self.left_sidebar.extended
            else ft.NavigationRailLabelType.NONE
        )
        self.left_sidebar_container.width = 200 if self.left_sidebar.extended else 60
        self.left_sidebar_container.update()
        self.left_sidebar.update()

    def change_left_sidebar(self, event: ControlEvent) -> None:
        selected_index = event.control.selected_index
        if selected_index == 0:
            self.content_area.content = self.name_generation_view
        elif selected_index == 1:
            self.content_area.content = ft.Text("Group Randomizer, coming soon!")
        elif selected_index == 2:
            self.content_area.content = ft.Text("Settings, coming soon!")

        self.content_area.update()
