import flet as ft
from flet import (
    UserControl,
    ElevatedButton,
    Row,
    Column,
    Container,
    Dropdown,
    Text,
    Page,
)


class NameGenerationView(UserControl):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller

    def build(self):  # type: ignore
        return Container(
            content=Text("Name Picker, coming soon!"),
            expand=True,
            alignment=ft.alignment.center,
        )
