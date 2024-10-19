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

    def build(self) -> Row:
        # Left column (input area)
        self.input_area = Container(
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
                alignment=ft.MainAxisAlignment.START,  # Align to top
            ),
            expand=1,
            padding=20,
        )

        # Right column (filter and output area)
        self.filter_area = Container(
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
                alignment=ft.MainAxisAlignment.START,  # Align to top
            ),
            padding=20,
        )

        self.output_area = Container(
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
                alignment=ft.MainAxisAlignment.START,  # Align to top
            ),
            expand=True,
            padding=20,
        )

        right_column = Column([self.filter_area, self.output_area], expand=1, alignment=ft.MainAxisAlignment.START)

        # Vertical divider
        self.divider = VerticalDivider(width=1, color=ft.colors.OUTLINE)

        # Main layout
        return Row(
            [
                self.input_area,
                self.divider,
                right_column,
            ],
            spacing=0,
            expand=True,
        )

    def update_selected_num(self, e):
        self.selected_num = e.control.value
        if self.selected_num != "custom":
            self.num_names_input.value = ""
            self.num_names_input.update()
        self.validate_input()

    def validate_input(self, e=None):
        try:
            num_names = int(self.num_names_input.value) if self.selected_num == "custom" else int(self.selected_num)
        except ValueError:
            num_names = 0
        names = []
        if self.input_area.content and self.input_area.content.controls:
            input_text = self.input_area.content.controls[1].value
            if input_text:
                names = [name.strip() for name in input_text.splitlines() if name.strip()]

        self.randomize_button.disabled = num_names > len(names)
        self.randomize_button.update()

    def generate_random_name(self, e):
        # Get the number of names to generate
        try:
            num_names = int(self.num_names_input.value) if self.selected_num == "custom" else int(self.selected_num)
        except ValueError:
            num_names = 0
        # Split names by new line and strip spaces
        names = []
        if self.input_area.content and self.input_area.content.controls:
            input_text = self.input_area.content.controls[1].value
            if input_text:
                names = [name.strip() for name in input_text.splitlines() if name.strip()]

        # Call the controller to generate names
        generated_names = self.controller.generate_name(names, num_names)

        # Update the output area
        if self.output_area.content and self.output_area.content.controls:
            self.output_area.content.controls[1].value = "\n".join(generated_names)
        else:
            print("Error: Output area not properly initialized")
        self.output_area.update()
