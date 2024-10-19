import flet as ft
from flet import (
    UserControl,
    Row,
    Column,
    Container,
    VerticalDivider,
    Text,
    TextField,
    ElevatedButton,
    RadioGroup,
    Radio,
)


class NameGenerationView(UserControl):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.num_names_input = TextField(value="", width=50, on_change=self.validate_input)
        self.selected_num = "1"
        self.randomize_button = ElevatedButton(
            text="Randomize",
            on_click=self.generate_random_name,
            width=200,
            disabled=False,
        )
        self.input_area = self._build_input_area()
        self.output_area = self._build_output_area()

    def build(self) -> Row:
        return Row(
            [
                self.input_area,
                self._build_divider(),
                self._build_right_column(),
            ],
            spacing=0,
            expand=True,
        )

    def _build_input_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Enter Names (one per line)"),
                    TextField(
                        multiline=True,
                        min_lines=10,
                        max_lines=20,
                        expand=True,
                        on_change=self.validate_input,
                    ),
                ],
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=1,
            padding=20,
        )

    def _build_divider(self) -> VerticalDivider:
        return VerticalDivider(width=1, color=ft.colors.OUTLINE)

    def _build_right_column(self) -> Column:
        return Column(
            [
                self._build_filter_area(),
                self.output_area,
            ],
            expand=1,
            alignment=ft.MainAxisAlignment.START,
        )

    def _build_filter_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Number of names to pick:"),
                    RadioGroup(
                        value=self.selected_num,
                        on_change=self.update_selected_num,
                        content=Row(
                            [
                                Radio(value="1", label="1"),
                                Radio(value="2", label="2"),
                                Radio(value="3", label="3"),
                                Radio(value="custom", label="Custom:"),
                                self.num_names_input,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ),
                    self.randomize_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=20,
        )

    def _build_output_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Generated Name(s):"),
                    Text(
                        "",
                        style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
        )

    def update_selected_num(self, e):
        self.selected_num = e.control.value
        if self.selected_num != "custom":
            self.num_names_input.value = ""
            self.num_names_input.update()
        self.validate_input()

    def validate_input(self, e=None):
        num_names = self._get_num_names()
        names = self._get_cleaned_names()
        self.randomize_button.disabled = num_names > len(names)
        self.randomize_button.update()

    def generate_random_name(self, e):
        num_names = self._get_num_names()
        names = self._get_cleaned_names()
        generated_names = self.controller.generate_name(names, num_names)
        self._update_output_area(generated_names)

    def _get_num_names(self) -> int:
        try:
            return int(self.num_names_input.value) if self.selected_num == "custom" else int(self.selected_num)
        except ValueError:
            return 0

    def _get_cleaned_names(self) -> list[str]:
        if (
            self.input_area.content
            and isinstance(self.input_area.content, Column)
            and len(self.input_area.content.controls) > 1
        ):
            input_text = self.input_area.content.controls[1].value if self.input_area.content.controls[1] else ""
            if input_text:
                return [name.strip() for name in input_text.splitlines() if name.strip()]
        return []

    def _update_output_area(self, generated_names: list[str]):
        if self.output_area and self.output_area.content and self.output_area.content.controls:
            self.output_area.content.controls[1].value = "\n".join(generated_names)
            self.output_area.update()
