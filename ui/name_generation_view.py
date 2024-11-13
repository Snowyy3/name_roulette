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
import asyncio


class NameGenerationView(UserControl):
    """A view component for the name generation interface."""

    def __init__(self, controller) -> None:
        """Initialize the name generation view."""
        super().__init__()
        self.controller = controller
        self.name_generator = NameGenerator()
        
        self.num_names_input = TextField(
            value="",
            width=40,
            height=35,
            text_align="center",
            content_padding=8,
            disabled=True,  # Initially disabled for the custom option
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
        self.names_input = TextField(
            label="Name",
            multiline=True,
            min_lines=8,
            max_lines=20,
            expand=2,
            on_change=self.validate_input,
            border=ft.InputBorder.OUTLINE,
        )
        self.gender_input = TextField(
            label="Gender",
            multiline=True,
            min_lines=8,
            max_lines=20,
            expand=1,
            on_change=self.validate_input,
            border=ft.InputBorder.OUTLINE,
            visible=False,
        )
        self.output_label = Text("Generated name:", weight=ft.FontWeight.BOLD)
        self.output_text = Text(
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
            disabled=True,  # Initially disabled
        )
        self.female_count_input = TextField(
            value="",
            width=40,
            height=35,
            text_align="center",
            content_padding=8,
            disabled=True,  # Initially disabled
        )
        self.copy_button = IconButton(
            icon=icons.COPY_ALL_ROUNDED,
            icon_size=20,
            visible=False,
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
            height=self.page.height if self.page else None,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _build_input_area(self) -> Container:
        """Builds the input area for entering names and genders."""
        name_gender_row = Row(
            controls=[self.names_input, self.gender_input],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

        return Container(
            content=Column(
                [
                    Text("Input:", weight=ft.FontWeight.BOLD),
                    Row(
                        [
                            self.save_list_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    Container(
                        content=name_gender_row,
                        expand=True,
                    ),
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )

    def _build_divider(self) -> VerticalDivider:
        """Builds a vertical divider between input and output areas."""
        return VerticalDivider(width=7, color=ft.colors.GREY, thickness=1)

    def _build_filter_area(self) -> Container:
        """Builds the filter area with number selection for males and females."""
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
                                    spacing=8,
                                ),
                            ],
                            spacing=32,
                        ),
                    ),
                    Divider(height=1, color=ft.colors.GREY_400),
                    Text("Gender filter:", weight=ft.FontWeight.BOLD),
                    RadioGroup(
                        value=self.selected_gender_filter,
                        on_change=self.update_selected_gender,
                        content=Column(
                            [
                                Radio(value="none", label="None"),
                                Row(
                                    [
                                        Radio(value="male", label=""),
                                        self.male_count_input,
                                        Text(" males"),
                                    ],
                                    spacing=8,
                                ),
                                Row(
                                    [
                                        Radio(value="female", label=""),
                                        self.female_count_input,
                                        Text(" females"),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                    self.randomize_button,
                    self.clear_result_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )

    def _build_output_area(self) -> Container:
        """Builds the output area to display the generated names."""
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
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )

    def update_selected_num(self, e: ControlEvent) -> None:
        """Updates the selected number of names to pick and enables/disables custom input box."""
        self.selected_num = e.control.value

        # Enable custom input only when "custom" is selected
        if self.selected_num == "custom":
            self.num_names_input.disabled = False
        else:
            self.num_names_input.disabled = True
            self.num_names_input.value = ""  # Clear the custom input if it's disabled

        # Update the UI
        self.num_names_input.update()
        self.validate_input()


    def validate_input(self, e: ControlEvent = None) -> None:
        """UI event handler for input validation."""
        names = self.name_generator.get_cleaned_names(self.names_input.value or "")

        # Check if gender filter is set to "None" and validate accordingly
        if self.selected_gender_filter == "none":
            is_valid = self.name_generator.validate_input(names, self.selected_num, self.num_names_input.value)
        else:
            is_valid = self.name_generator.validate_input(
                names, self.selected_num, self.num_names_input.value,
                male_count=self.male_count_input.value or "0",
                female_count=self.female_count_input.value or "0"
            )

        self.randomize_button.disabled = not is_valid
        self.randomize_button.update()

    def generate_random_name(self, e: ControlEvent) -> None:
        """UI event handler for name generation, ignoring gender if 'None' is selected."""
        total_count = self.name_generator.get_num_names(self.selected_num, self.num_names_input.value)

        if self.selected_gender_filter == "none":
            generated_names = self.name_generator.generate_random_names_without_gender(
                names_text=self.names_input.value or "",
                total_count=total_count
            )
        else:
            try:
                male_count = int(self.male_count_input.value) if self.selected_gender_filter == "male" else 0
            except ValueError:
                male_count = 0

            try:
                female_count = int(self.female_count_input.value) if self.selected_gender_filter == "female" else 0
            except ValueError:
                female_count = 0

            generated_names = self.name_generator.process_name_generation(
                names_text=self.names_input.value or "",
                genders_text=self.gender_input.value or "",
                selected_num=self.selected_num,
                custom_value=self.num_names_input.value,
                male_count=male_count,
                female_count=female_count
            )

        if not generated_names:
            self.output_text.value = "Unable to generate names. Please make sure there are enough names to meet your selected counts."
            self.output_area.update()
            return

        self._update_output_area(generated_names)

    def clear_result(self, e: ControlEvent) -> None:
        """Clear the generated result and disable the clear button."""
        self.output_text.value = ""
        self.output_label.value = "Generated name:"
        self.clear_result_button.disabled = True
        self.copy_button.visible = False
        self.output_area.update()
        self.clear_result_button.update()

    def _update_output_area(self, generated_names: list[str]) -> None:
        """Update the output area with generated names."""
        if self.output_area and self.output_area.content:
            self.output_label.value = "Generated names:" if len(generated_names) > 1 else "Generated name:"
            self.output_text.value = "\n".join(generated_names)
            self.clear_result_button.disabled = False
            self.copy_button.visible = bool(generated_names)
            self.output_area.update()
            self.clear_result_button.update()

    def update_selected_gender(self, e: ControlEvent) -> None:
        """Updates the selected gender filter and enables/disables inputs based on selection."""
        self.selected_gender_filter = e.control.value
        if self.selected_gender_filter == "none":
            # Disable both male and female inputs when "None" is selected
            self.male_count_input.value = ""
            self.male_count_input.disabled = True
            self.male_count_input.update()

            self.female_count_input.value = ""
            self.female_count_input.disabled = True
            self.female_count_input.update()

            # Hide gender input box as it's not required
            self.gender_input.visible = False
            self.gender_input.update()

        elif self.selected_gender_filter == "male":
            # Enable male input and disable female input
            self.male_count_input.disabled = False
            self.female_count_input.value = ""
            self.female_count_input.disabled = True
            self.gender_input.visible = True
            self.male_count_input.update()
            self.female_count_input.update()
            self.gender_input.update()

        elif self.selected_gender_filter == "female":
            # Enable female input and disable male input
            self.female_count_input.disabled = False
            self.male_count_input.value = ""
            self.male_count_input.disabled = True
            self.gender_input.visible = True
            self.male_count_input.update()
            self.female_count_input.update()
            self.gender_input.update()

    def copy_to_clipboard(self, e: ControlEvent) -> None:
        """Copy generated names to clipboard."""
        if self.output_text.value:
            self.page.set_clipboard(self.output_text.value)
            self.page.show_snack_bar(ft.SnackBar(content=Text("Copied to clipboard!")))

    async def handle_save_list_click(self, e: ControlEvent) -> None:
        """Temporarily changes the icon to show save confirmation."""
        self.save_list_button.icon = icons.BOOKMARK_ADDED
        self.save_list_button.update()
        await asyncio.sleep(3)
        self.save_list_button.icon = icons.BOOKMARK_ADD_OUTLINED
        self.save_list_button.update()
