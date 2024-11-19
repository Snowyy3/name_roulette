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

    page.window.width = 1600
    page.window.height = 900
    page.window.full_screen = False
    page.window.title_bar_hidden = False
    page.window.title_bar_buttons_hidden = False

    main_controller = MainController(page)
    main_view = MainView(page, main_controller)

    page.add(main_view)


if __name__ == "__main__":
    ft.app(target=main)
