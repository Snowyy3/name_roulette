import flet as ft
from flet import Page

from ui.main_view import MainView
from controller.main_controller import MainController


def main(page: Page) -> None:
    page.title = "Name Roulette (v0.8)"
    page.theme_mode = ft.ThemeMode.LIGHT  # Can set to system later, add add toggle
    page.padding = 0
    page.window.min_width = 600
    page.window.min_height = 400

    page.auto_scroll = False
    page.scroll = None
    page.window.maximized = True

    main_controller = MainController(page)
    main_view = MainView(page, main_controller)

    page.add(main_view)


if __name__ == "__main__":
    ft.app(target=main)
