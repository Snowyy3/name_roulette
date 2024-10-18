import flet as ft
from ui.name_generation_view import NameGenerationView

class MainView(ft.UserControl):
    def __init__(self, page: ft.Page, controller):
        super().__init__()
        self.page = page
        self.controller = controller
        self.name_generation_view = NameGenerationView(self.controller)

    def build(self):
        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
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

        main_content = ft.Row(
            [
                ft.Container(
                    content=self.sidebar,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    width=100,
                    expand=False,
                ),
                ft.VerticalDivider(width=1),
                self.content_area,
            ],
            expand=True,
            spacing=0,
        )

        self.controls.append(
            ft.Container(
                content=main_content,
                expand=True,
                height=self.page.height if self.page else None,
            )
        )

    def sidebar_change(self, e):
        if e.control.selected_index == 0:
            self.content_area.content = self.name_generation_view
        elif e.control.selected_index == 1:
            # TODO: Implement Group Formation View
            self.content_area.content = ft.Text("Group Formation View (Coming Soon)")
        self.content_area.update()
