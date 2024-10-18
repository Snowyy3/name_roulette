import flet as ft
from ui.name_generation_view import NameGenerationView

class MainView(ft.UserControl):
    def __init__(self, page: ft.Page, controller):
        super().__init__()
        self.page = page
        self.controller = controller
        self.name_generation_view = NameGenerationView(self.controller)
        self.is_expanded = False

    def build(self):
        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE,
            extended=False,
            min_width=60,
            min_extended_width=200,
            leading=ft.IconButton(icon=ft.icons.MENU, on_click=self.toggle_sidebar),
            group_alignment=-1,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.SHUFFLE,
                    selected_icon=ft.icons.SHUFFLE,
                    label="Name Generation"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.GROUP,
                    selected_icon=ft.icons.GROUP,
                    label="Group Formation"
                ),
            ],
            on_change=self.sidebar_change,
        )

        self.content_area = ft.Container(
            content=self.name_generation_view,
            expand=True
        )

        self.sidebar_container = ft.Container(
            content=self.sidebar,
            bgcolor=ft.colors.SURFACE_VARIANT,
            width=60,
            height=self.page.window_height if self.page else None,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        main_row = ft.Row([
            self.sidebar_container,
            ft.VerticalDivider(width=1),
            self.content_area
        ], expand=True, spacing=0)

        self.controls.append(ft.Container(content=main_row, expand=True))

    def toggle_sidebar(self, e):
        self.is_expanded = not self.is_expanded
        self.sidebar.extended = self.is_expanded
        self.sidebar.label_type = (
            ft.NavigationRailLabelType.ALL if self.is_expanded
            else ft.NavigationRailLabelType.NONE
        )
        self.sidebar_container.width = 200 if self.is_expanded else 60
        self.sidebar_container.update()
        self.sidebar.update()

    def sidebar_change(self, e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            self.content_area.content = self.name_generation_view
        elif selected_index == 1:
            # TODO: Implement Group Formation View
            self.content_area.content = ft.Text("Group Formation View (Coming Soon)")
        self.content_area.update()
