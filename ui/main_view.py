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
            group_alignment=-0.9,
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
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS,
                    selected_icon=ft.icons.SETTINGS,
                    label="Settings"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    selected_icon=ft.icons.ACCOUNT_CIRCLE,
                    label="User Account"
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
            height=self.page.height if self.page else None,  # Handle potential None value
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        main_stack = ft.Stack([
            self.content_area,
            self.sidebar_container
        ], expand=True)  # Ensure the Stack expands to fill available space

        self.controls.append(main_stack)

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
        elif selected_index == 2:
            # TODO: Implement Settings View
            self.content_area.content = ft.Text("Settings View (Coming Soon)")
        elif selected_index == 3:
            # TODO: Implement User Account View
            self.content_area.content = ft.Text("User Account View (Coming Soon)")
        self.content_area.update()
