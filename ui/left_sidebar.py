import flet as ft
from flet import (
    UserControl,
    Container,
    Column,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    Border,
    BorderSide,
    ControlEvent,
)
from ui.views import View


class LeftSidebar(UserControl):
    def __init__(self, on_view_change):
        super().__init__()
        self.on_view_change = on_view_change
        self.current_view = View.NAME_PICKER

    def build(self):
        self.menu_button = IconButton(
            icon=ft.icons.MENU,
            on_click=self.toggle_sidebar,
        )

        self.menu_container = Container(
            content=Container(
                content=self.menu_button,
                alignment=ft.alignment.center,
            ),
            margin=ft.margin.only(top=16, bottom=16),
            height=60,
            width=80,
        )

        self.main_nav = NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=80,
            min_extended_width=180,
            group_alignment=-0.95,
            destinations=[
                NavigationRailDestination(
                    label="Name Picker",
                    icon=ft.icons.PERSON_OUTLINED,  # Changed from SHUFFLE_OUTLINED
                    selected_icon=ft.icons.PERSON,  # Changed from SHUFFLE_ROUNDED
                    padding=10,
                ),
                NavigationRailDestination(
                    label="Group Randomizer",
                    icon=ft.icons.GROUPS_2_OUTLINED,
                    selected_icon=ft.icons.GROUPS_2_ROUNDED,
                    padding=10,
                ),
            ],
            on_change=self.change_main_nav,
            bgcolor=ft.colors.TRANSPARENT,
        )

        self.bottom_nav = NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=80,
            min_extended_width=180,
            group_alignment=-0.9,
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

        self.container = Container(
            content=Column(
                [
                    self.menu_container,
                    Container(
                        content=self.main_nav,
                        height=140,
                    ),
                    Container(
                        expand=True,
                    ),
                    Container(
                        content=self.bottom_nav,
                        height=160,
                        margin=ft.margin.only(bottom=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            ),
            bgcolor="#E6F3FF",
            width=80,
            border=Border(right=BorderSide(width=1, color=ft.colors.OUTLINE)),
            animate=ft.animation.Animation(200, ft.animation.AnimationCurve.EASE_OUT_CUBIC),
        )

        return self.container

    def toggle_sidebar(self, _):
        self.main_nav.extended = not self.main_nav.extended
        self.bottom_nav.extended = self.main_nav.extended

        label_type = ft.NavigationRailLabelType.ALL if self.main_nav.extended else ft.NavigationRailLabelType.NONE
        self.main_nav.label_type = label_type
        self.bottom_nav.label_type = label_type

        self.container.width = 200 if self.main_nav.extended else 80
        self.container.update()
        self.main_nav.update()
        self.bottom_nav.update()

    def update_navigation_state(self, selected_view: View):
        self.current_view = selected_view

        if selected_view in [View.NAME_PICKER, View.GROUP_FORMER]:
            self.main_nav.selected_index = selected_view.value - 1
            self.bottom_nav.selected_index = None
        else:
            self.main_nav.selected_index = None
            self.bottom_nav.selected_index = 0

        self.main_nav.update()
        self.bottom_nav.update()

    def change_bottom_nav(self, _):
        self.update_navigation_state(View.SETTINGS)
        self.on_view_change(View.SETTINGS)

    def change_main_nav(self, event: ControlEvent):
        selected_index = event.control.selected_index
        view = View.NAME_PICKER if selected_index == 0 else View.GROUP_FORMER
        self.update_navigation_state(view)
        self.on_view_change(view)

    def resize(self, height):
        self.container.height = height
        self.container.update()
