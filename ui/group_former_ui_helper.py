import flet as ft
from flet import (
    Row,
    Column,
    Container,
    Text,
    TextField,
    IconButton,
    icons,
    Radio,
    RadioGroup,
)


def build_input_area(view) -> Container:
    """Build the left input area containing name inputs"""
    return Container(
        content=Column(
            [
                Row(
                    [
                        Text("Enter names (one per line)", weight=ft.FontWeight.BOLD),
                        view.save_list_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                Container(
                    content=view.input_row,  # Changed from view.input_area to view.input_row
                    expand=True,
                ),
            ],
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        alignment=ft.alignment.top_left,
        width=view.left_column_width,
    )


def build_filter_area(view) -> Container:
    """Build the middle filter area containing group settings"""
    return Container(
        content=Column(
            [
                Text("Group Formation Settings:", weight=ft.FontWeight.BOLD),
                Row(
                    controls=[
                        view.group_size_input,
                        Text("OR", weight=ft.FontWeight.BOLD),
                        view.group_num_input,
                    ],
                    spacing=10,
                ),
                ft.Divider(height=1, color=ft.colors.GREY_400),
                RadioGroup(
                    value=view.selected_gender_filter,
                    on_change=view.update_selected_gender,
                    content=Column(
                        [
                            Text("Gender filler:", weight=ft.FontWeight.BOLD),
                            view.error_message,
                            Radio(value="none", label="None"),
                            Row(
                                [Radio(value="male"), view.male_count_input, Text(" males")],
                                spacing=8,
                            ),
                            Row(
                                [Radio(value="female"), view.female_count_input, Text(" females")],
                                spacing=8,
                            ),
                        ],
                        spacing=8,
                    ),
                ),
                Text("Manually Assign:", weight=ft.FontWeight.BOLD),
                RadioGroup(
                    value=view.manual_group,
                    on_change=view.update_selected_manual_group,
                    content=Column([
                        Row([
                            Radio(value="none", label="None"),
                            Radio(value="manual", label="Manual"),
                        ])
                    ]),
                ),
                view.generate_button,
                view.clear_result_button,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=20,
        alignment=ft.alignment.top_left,
    )


def build_output_area(view) -> Container:
    """Build the right output area displaying groups"""
    return Container(
        content=Column(
            [
                Row(
                    controls=[view.output_label],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                view.error_message_manual,
                Container(
                    content=Column(
                        controls=[view.output_text],
                        spacing=20,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                    height=500,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=20,
        alignment=ft.alignment.top_left,
        width=view.right_column_width,
    )


def create_group_box(group_num: int, is_disabled: bool = True) -> TextField:
    """Create a group text box for displaying or entering names"""
    return TextField(
        label=f"Group {group_num}",
        value="",
        multiline=True,
        width=200,
        height=100,
        text_align=ft.TextAlign.LEFT,
        border=ft.border.all(1, ft.colors.GREY_300),
        disabled=is_disabled,
    )


def format_group_text(group: list[str]) -> str:
    """Format a group's names into display text"""
    return "\n".join([f"• {name}" for name in group])
