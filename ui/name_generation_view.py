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
    ControlEvent,
)


class NameGenerationView(UserControl):
    """
    View for name generation in the Name Roulette application.

    Args:
        controller (NameGenerationController): The controller managing this view's logic.
    """

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.num_names_input = TextField(
            value="",
            width=40,
            height=35,
            text_align="center",  # Centers text horizontally
            content_padding=8,  # Adds padding to center text vertically
            on_change=self.validate_input,
        )
        self.selected_num = "1"
        self.randomize_button = ElevatedButton(
            text="Randomize",
            on_click=self.generate_random_name,
            width=200,
            disabled=False,
            height=50,
        )
        self.names_input = TextField(  # Create reference to input field
            multiline=True,
            min_lines=8,
            max_lines=20,
            expand=True,
            on_change=self.validate_input,
            border=ft.InputBorder.OUTLINE,
        )
        self.output_label = Text("Generated name:")  # Store reference to label
        self.output_text = Text(  # Store reference to output text
            "",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            weight=ft.FontWeight.BOLD,
        )
        self.input_area = self._build_input_area()
        self.output_area = self._build_output_area()

    def build(self) -> Row:
        """Builds the main layout of the Name Generation view."""
        return Row(
            controls=[
                self.input_area,
                self._build_divider(),
                self._build_filter_area(),
                self._build_divider(),
                self.output_area,
            ],
            spacing=0,
            expand=True,
            height=self.page.height if self.page else None,  # Add height constraint
            alignment=ft.MainAxisAlignment.START,  # Align horizontally
            vertical_alignment=ft.CrossAxisAlignment.START,  # Align vertically to top
        )

    def _build_input_area(self) -> Container:
        """Builds the input area for entering names.

        Returns:
            Container: A container holding the name input TextField.
        """
        return Container(
            content=Column(
                [
                    Text("Enter names (one per line)"),
                    Container(
                        content=self.names_input,  # Use the stored reference
                        expand=True,
                    ),
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,  # Enable scrolling
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,  # Align container content to top
        )

    def _build_divider(self) -> VerticalDivider:
        """Builds a vertical divider between input and output areas.

        Returns:
            VerticalDivider: A simple vertical divider.
        """
        return VerticalDivider(width=7, color=ft.colors.GREY, thickness=1)

    def _build_filter_area(self) -> Container:
        """Builds the filter area with number selection and randomize button.

        Returns:
            Container: A container holding the filter controls.
        """
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
                                Row(
                                    [
                                        Radio(value="custom", label="Custom: "),
                                        self.num_names_input,
                                    ],
                                    spacing=8,  # Tight spacing between Custom label and input
                                ),
                            ],
                            spacing=16,  # Consistent spacing between radio options
                        ),
                    ),
                    self.randomize_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,  # Change from False to True
            padding=20,
            alignment=ft.alignment.top_left,  # Align container content to top
        )

    def _build_output_area(self) -> Container:
        """Builds the output area to display the generated names.

        Returns:
            Container: A container holding the generated names.
        """
        return Container(
            content=Column(
                [
                    self.output_label,
                    self.output_text,
                ],
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,  # Change from False to True
            padding=20,
            alignment=ft.alignment.top_left,  # Align container content to top
        )

    def update_selected_num(self, e: ControlEvent) -> None:
        """Updates the selected number of names to pick and validates input.

        Args:
            e (ControlEvent): The event triggered by the RadioGroup.
        """
        self.selected_num = e.control.value
        if self.selected_num != "custom":
            self.num_names_input.value = ""
            self.num_names_input.update()
        self.validate_input()

    def validate_input(self, e: ControlEvent = None) -> None:
        """Validates the input and enables/disables the randomize button."""
        names = self._get_cleaned_names()
        num_names = self._get_num_names()

        # Debug prints to help identify the issue
        print(f"Names: {names}")
        print(f"Number of names: {num_names}")
        print(f"Selected num: {self.selected_num}")
        print(f"Custom input value: {self.num_names_input.value}")

        # New validation logic
        is_valid = len(names) > 0  # Must have at least one name
        if self.selected_num == "custom":
            is_valid = is_valid and num_names > 0 and num_names <= len(names)
        else:
            is_valid = is_valid and int(self.selected_num) <= len(names)

        self.randomize_button.disabled = not is_valid
        self.randomize_button.update()

    def generate_random_name(self, e: ControlEvent) -> None:
        """Generates random names and updates the output area.

        Args:
            e (ControlEvent): The event triggered by the randomize button.
        """
        num_names = self._get_num_names()
        names = self._get_cleaned_names()
        generated_names = self.controller.generate_name(names, num_names)
        self._update_output_area(generated_names)

    def _get_num_names(self) -> int:
        """Retrieves the number of names to generate from user input.

        Returns:
            int: The number of names to generate.
        """
        try:
            if self.selected_num == "custom":
                value = self.num_names_input.value.strip()
                return int(value) if value else 0
            return int(self.selected_num)
        except ValueError:
            return 0

    def _get_cleaned_names(self) -> list[str]:
        """Retrieves and cleans the list of names from the input area.

        Returns:
            list[str]: A list of cleaned names.
        """
        input_text = self.names_input.value if self.names_input.value else ""
        return [name.strip() for name in input_text.splitlines() if name.strip()]

    def _update_output_area(self, generated_names: list[str]):
        """Updates the output area with the generated names.

        Args:
            generated_names (list[str]): The list of generated names.
        """
        if self.output_area and self.output_area.content:
            # Update label based on number of names
            self.output_label.value = "Generated names:" if len(generated_names) > 1 else "Generated name:"
            self.output_text.value = "\n".join(generated_names)
            self.output_area.update()
