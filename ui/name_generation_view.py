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
    Divider,
    IconButton,
    icons,
)
from model.name_generator import NameGenerator
import asyncio  # Add this import at the top with other imports


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
            content=Row(
                [
                    ft.Icon(icons.SHUFFLE_ROUNDED),
                    Text("Randomize"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            on_click=self.generate_random_name,
            width=200,
            disabled=False,
            height=50,
        )
        self.clear_result_button = ElevatedButton(
            content=Row(
                [
                    ft.Icon(icons.CLEAR_ROUNDED),
                    Text("Clear Result"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            on_click=self.clear_result,
            width=200,
            disabled=True,
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
        self.output_label = Text("Generated name:", weight=ft.FontWeight.BOLD)  # Store reference to label
        self.output_text = Text(  # Store reference to output text
            "",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            weight=ft.FontWeight.BOLD,
        )
        self.selected_gender_filter = "none"
        self.male_count_input = TextField(
            value="",
            width=40,
            height=35,
            text_align="center",
            content_padding=8,
        )
        self.female_count_input = TextField(
            value="",
            width=40,
            height=35,
            text_align="center",
            content_padding=8,
        )
        self.copy_button = IconButton(
            icon=icons.COPY_ALL_ROUNDED,
            icon_size=20,
            visible=False,  # Initially hidden
            tooltip="Copy to clipboard",
            on_click=self.copy_to_clipboard,
        )
        self.save_list_button = IconButton(
            icon=icons.BOOKMARK_ADD_OUTLINED,
            icon_size=20,
            tooltip="Save as list",
            on_click=self.handle_save_list_click,
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
                    Row(
                        [
                            Text("Enter names (one per line)", weight=ft.FontWeight.BOLD),
                            self.save_list_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    Container(
                        content=self.names_input,  # Use the stored reference
                        expand=True,
                    ),
                ],
                spacing=20,  # Spacing between title and input field
                expand=True,
                scroll=ft.ScrollMode.AUTO,  # Enable scrolling
            ),
            expand=True,
            padding=20,  # Padding around the input area
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
                    Text("Number of names to pick:", weight=ft.FontWeight.BOLD),
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
                            spacing=32,  # Consistent spacing between radio options
                        ),
                    ),
                    Divider(height=1, color=ft.colors.GREY_400),  # Add thin gray divider
                    Text("Gender filter:", weight=ft.FontWeight.BOLD),
                    RadioGroup(
                        value=self.selected_gender_filter,
                        on_change=self.update_selected_gender,
                        content=Column(
                            [
                                Radio(value="none", label="None"),
                                Row(
                                    [
                                        Radio(value="male", label="At least "),
                                        self.male_count_input,
                                        Text(" males"),
                                    ],
                                    spacing=8,  
                                ),
                                Row(
                                    [
                                        Radio(value="female", label="At least "),
                                        self.female_count_input,
                                        Text(" females"),
                                    ],
                                    spacing=8,  # Tight spacing between elements
                                ),
                            ],
                            spacing=8,  # Spacing between radio options
                        ),
                    ),
                    self.randomize_button,
                    self.clear_result_button,
                ],
                spacing=20,  # Spacing between filter elements
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,  # Padding around the filter area
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
                    Row(
                        [
                            self.output_label,
                            self.copy_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.output_text,
                ],
                spacing=20,  # Spacing between label and output text
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,  # Padding around the output area
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

    def clear_result(self, e: ControlEvent) -> None:
        """Clear the generated result and disable the clear button."""
        self.output_text.value = ""
        self.output_label.value = "Generated name:"
        self.clear_result_button.disabled = True
        self.copy_button.visible = False  # Hide copy button when clearing
        self.output_area.update()
        self.clear_result_button.update()

    def _update_output_area(self, generated_names: list[str]) -> None:
        """Update the output area with generated names.

        Args:
            generated_names (list[str]): The list of generated names to display.
        """
        if self.output_area and self.output_area.content:
            # Update label based on number of names
            self.output_label.value = "Generated names:" if len(generated_names) > 1 else "Generated name:"
            self.output_text.value = "\n".join(generated_names)
            self.clear_result_button.disabled = False
            self.copy_button.visible = bool(generated_names)  # Show copy button only when there are results
            self.output_area.update()
            self.clear_result_button.update()

    def update_selected_gender(self, e: ControlEvent) -> None:
        """Updates the selected gender filter and clears unused input fields.

        Args:
            e (ControlEvent): The event triggered by the RadioGroup.
        """
        self.selected_gender_filter = e.control.value
        # Clear male input if not selected
        if self.selected_gender_filter != "male":
            self.male_count_input.value = ""
            self.male_count_input.update()
        # Clear female input if not selected
        if self.selected_gender_filter != "female":
            self.female_count_input.value = ""
            self.female_count_input.update()

    def copy_to_clipboard(self, e: ControlEvent) -> None:
        """Copy generated names to clipboard."""
        if self.output_text.value:
            self.page.set_clipboard(self.output_text.value)
            # Optionally show a snackbar to confirm copy
            self.page.show_snack_bar(ft.SnackBar(content=Text("Copied to clipboard!")))

    async def handle_save_list_click(self, e: ControlEvent) -> None:
        """Temporarily changes the icon to show save confirmation."""
        self.save_list_button.icon = icons.BOOKMARK_ADDED
        self.save_list_button.update()

        await asyncio.sleep(3)  # Use asyncio.sleep instead of page.sleep

        self.save_list_button.icon = icons.BOOKMARK_ADD_OUTLINED
        self.save_list_button.update()
