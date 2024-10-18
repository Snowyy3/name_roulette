import flet as ft
from ui.main_view import MainView
from controller.main_controller import MainController

def main(page: ft.Page):
    page.title = "Name Roulette"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0  # Remove padding
    page.window.min_width = 600  # Set minimum window width
    page.window.min_height = 400  # Set minimum window height
    page.auto_scroll = False
    page.scroll = None

    main_controller = MainController(page)
    main_view = MainView(page, main_controller)

    page.add(main_view)

ft.app(target=main)
