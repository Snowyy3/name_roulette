import flet as ft
from flet import (
    UserControl,
    Column,
    Row,
    Container,
    TextField,
    ElevatedButton,
    Dropdown,
    Text,
    Divider,
)


class GroupFormationView(UserControl):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.show_gender_column = False  # Track visibility of gender column
        self.group_size = None  # Default group size
        self.group_num = 1 

    def build(self) -> Column:
        """Builds the group formation view layout."""

        # Name input area (multiline like TextArea) to allow multiple names
        self.name_input = TextField(
            label="Enter Names (one per line)",
            multiline=True,
            min_lines=10,
            max_lines=20,
            expand=True,
            height=200,
        )

        self.gender_input = TextField(
            label="Gender",
            multiline=True,
            min_lines=10,
            max_lines=20,
            expand=True,
            height=200,
        )

        # Gender dropdown in constraint fields
        self.gender_filter_dropdown = Dropdown(
            label="Gender Filter",
            options=[
                ft.dropdown.Option(text="None", data="None"),
                ft.dropdown.Option(text="Male", data="Male"),
                ft.dropdown.Option(text="Female", data="Female"),
            ],
            value="None",
            on_change=self.toggle_gender_column,
            width=150,
        )

        # Group size input field in constraint fields
        self.group_size_input = TextField(
            label="Group Size",
            value=str(self.group_size),
            width=150,
            on_change=self.update_group_size,
        )

        self.group_num_input = TextField(
            label="Number of Group",
            value=str(self.group_num),
            width=150,
            on_change=self.update_group_num,
        )

        # Button to form groups based on inputs
        self.form_groups_button = ElevatedButton(
            text="Generate Groups",
            on_click=self.form_groups,
            width=200,
        )

        # Output area for displaying generated groups
        self.output_area = TextField(
            label="Generated Group(s):",
            enable_suggestions=False,
            expand=True,
            height=200,
            multiline= True,
        )

        # Layout for the input fields with optional gender column
        self.name_column = Column(
            [self.name_input],
            expand=2,
        )
        self.gender_column = Column(
            [self.gender_input],
            visible=self.show_gender_column,
            expand=1,
        )

        input_area = Row(
            [self.name_column, self.gender_column],
            spacing=10,
            expand=True,
        )

        # Right constraint area with gender filter, group size input, and generation button
        constraint_area = Column(
            [
                Text("Number of names to pick:"),
                self.gender_filter_dropdown,
                self.group_size_input,
                self.group_num_input,
                self.form_groups_button,
            ],
            alignment="start",
            spacing=20,
        )

        # Arrange main layout like the provided example image
        return Column(
            [
                Row(
                    [
                        Container(content=input_area, expand=True, padding=10),
                        Divider(height=1, color=ft.colors.OUTLINE),
                        Container(content=constraint_area, padding=10),
                    ],
                    alignment="start",
                    expand=True,
                ),
                self.output_area,
            ],
            alignment="start",
            expand=True,
            spacing=25,
        )

    def toggle_gender_column(self, event):
        """Toggles visibility of the gender column based on dropdown selection."""
        self.show_gender_column = event.control.value != "None"
        self.gender_column.visible = self.show_gender_column
        self.update()

    def update_group_size(self, event):
        """Updates the group size from the input field."""
        try:
            self.group_size = int(event.control.value)
        except ValueError:
            self.group_size_input.error_text = "Please enter a valid number."
            self.group_size_input.update()
        else:
            self.group_size_input.error_text = None
            self.group_size_input.update()

    def update_group_num(self, event):
        """Updates the group size from the input field."""
        try:
            self.group_num = int(event.control.value)
        except ValueError:
            self.group_num_input.error_text = "Please enter a valid number."
            self.group_num_input.update()
        else:
            self.group_num_input.error_text = None
            self.group_num_input.update()

    def form_groups(self, event):
        """Handles the group formation based on the inputs."""
        names = self.name_input.value.splitlines()  
        gender_filter = self.gender_filter_dropdown.value if self.show_gender_column else None
        group_size = self.group_size
        group_num = self.group_num

        # Placeholder for group formation logic
        #generated_groups = names 
        generated_groups = self.controller.form_groups(names,group_size,group_num)# This is output (list variable)
        
        # # Format the groups output
        formatted_output = ""
        for i, group in enumerate(generated_groups, start=1):
            formatted_output += f"Group {i}:\n"
            formatted_output += "\n".join([f" - {member}" for member in group]) + "\n\n"

        # Set and update the output area
        self.output_area.value = formatted_output.strip()  # Remove any trailing whitespace
        self.output_area.update()

        # self.output_area.value = generated_groups
        # self.output_area.update()

