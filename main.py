import flet as ft
from flet import Page

from ui.main_view import MainView
from controller.main_controller import MainController


def main(page: Page) -> None:
    page.title = "Name roulette (v0.5)"
    page.theme_mode = ft.ThemeMode.LIGHT  # Can set to system later, add add toggle
    page.padding = 0
    page.window.min_width = 400
    page.window.min_height = 400
    page.auto_scroll = False
    page.scroll = None

    main_controller = MainController(page)
    main_view = MainView(page, main_controller)  # Create an instance of the MainView class

    page.add(main_view)  # Add the main_view to the page


if __name__ == "__main__":
    ft.app(target=main)
