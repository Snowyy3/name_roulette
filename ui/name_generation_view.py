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
from model.name_generator import NameGenerator


class NameGenerationView(UserControl):
    """A view component for the name generation interface.

    This class provides the UI for entering names, selecting generation options,
    and displaying generated names.

    Attributes:
        controller: The controller managing this view's business logic.
        name_generator (NameGenerator): Handler for name generation operations.
        num_names_input (TextField): Input field for custom number selection.
        selected_num (str): Currently selected number of names to generate.
        randomize_button (ElevatedButton): Button to trigger name generation.
        names_input (TextField): Input field for the list of names.
        output_label (Text): Label for the output area.
        output_text (Text): Display area for generated names.
    """

    def __init__(self, controller) -> None:
        """Initialize the name generation view.

        Args:
            controller: The controller managing this view's business logic.
        """
        super().__init__()
        self.controller = controller
        self.name_generator = NameGenerator()
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
                            spacing=24,  # Consistent spacing between radio options
                        ),
                    ),
                    self.randomize_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
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
            expand=True,
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
        """UI event handler for input validation."""
        names = self.name_generator.get_cleaned_names(self.names_input.value or "")
        is_valid = self.name_generator.validate_input(names, self.selected_num, self.num_names_input.value)
        self.randomize_button.disabled = not is_valid
        self.randomize_button.update()

    def generate_random_name(self, e: ControlEvent) -> None:
        """UI event handler for name generation."""
        generated_names = self.name_generator.process_name_generation(
            self.names_input.value or "", self.selected_num, self.num_names_input.value
        )
        self._update_output_area(generated_names)

    def _update_output_area(self, generated_names: list[str]) -> None:
        """Update the output area with generated names.

        Args:
            generated_names (list[str]): The list of generated names to display.
        """
        if self.output_area and self.output_area.content:
            # Update label based on number of names
            self.output_label.value = "Generated names:" if len(generated_names) > 1 else "Generated name:"
            self.output_text.value = "\n".join(generated_names)
            self.output_area.update()
