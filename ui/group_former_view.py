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
from model.group_former import GroupFormer


class GroupFormationView(UserControl):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.show_gender_column = False
        self.groupformer = GroupFormer()

        self.left_column_width = 500  # Initial size for the left column
        self.middle_column_min_width = 300  # Initial size for the middle column (set as the minimum)
        self.right_column_width = 550  # Initial size for the right column

        # Initialize input fields
        self.names_input = TextField(
            label="Name",
            multiline=True,
            min_lines=8,
            max_lines=20,
            expand=True,
            height=200,
            border=ft.InputBorder.OUTLINE,
        )

        self.gender_input = TextField(
            label="Gender",
            multiline=True,
            min_lines=10,
            max_lines=20,
            height=200,
            expand=True,
        )

        self.name_column = Column(
            [self.names_input],
            expand=2,
        )

        self.gender_column = Column(
            [self.gender_input],
            visible=self.show_gender_column,
            expand=1,
        )

        self.input_area = Row(
            [self.name_column, self.gender_column],
            spacing=10,
            expand=True,
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
        self.group_size_input = TextField(
            label="Max Group Size",
            width=150,
            on_change=self.update_group_size,
            border=ft.InputBorder.OUTLINE,
        )

        self.group_num_input = TextField(
            label="Number of Groups",
            width=150,
            on_change=self.update_group_num,
            border=ft.InputBorder.OUTLINE,
        )

        self.selected_gender_filter = "none"
        self.male_count_input = TextField(
            value="", width=40, height=35, text_align="center", content_padding=8, disabled=True
        )
        self.female_count_input = TextField(
            value="", width=40, height=35, text_align="center", content_padding=8, disabled=True
        )

        self.generate_button = ElevatedButton(
            text="Generate Groups",
            width=200,
            height=50,
            on_click=self.form_groups,
        )
        self.copy_button = IconButton(
            icon=icons.COPY_ALL_ROUNDED,
            icon_size=20,
            visible=True,
            tooltip="Copy to clipboard",
            on_click=self.copy_to_clipboard,
        )
        self.output_label = Text("Generated Groups:", weight=ft.FontWeight.BOLD)
        self.output_text = Text(
            "",
            style=ft.TextThemeStyle.HEADLINE_SMALL,
            weight=ft.FontWeight.BOLD,
        )
        self.input_area = self._build_input_area()
        self.output_area = self._build_output_area()
        self.filter_area = self._build_filter_area()

    def move_left_divider(self, e: ft.DragUpdateEvent):
        """Handle dragging for the left divider."""
        total_width = self.page.width or 960  # Default page width
        middle_width = total_width - self.left_column_width - self.right_column_width - 14  # Gap between dividers

        # Ensure the left divider respects the minimum width of the middle column
        if (
            e.delta_x > 0  # Dragging right
            and self.left_column_width < 700
            and middle_width - e.delta_x >= self.middle_column_min_width
        ) or (
            e.delta_x < 0  # Dragging left
            and self.left_column_width > 350
        ):
            self.left_column_width += e.delta_x
            self.input_area.width = self.left_column_width
            self.input_area.update()

            # Dynamically adjust middle column width
            middle_width -= e.delta_x
            self.filter_area.width = middle_width
            self.filter_area.update()

    def move_right_divider(self, e: ft.DragUpdateEvent):
        """Handle dragging for the right divider."""
        total_width = self.page.width or 960  # Default page width
        middle_width = total_width - self.left_column_width - self.right_column_width - 14  # Gap between dividers

        # Ensure the right divider respects the minimum width of the middle column
        if (
            e.delta_x < 0  # Dragging left
            and self.right_column_width < 700
            and middle_width + e.delta_x >= self.middle_column_min_width
        ) or (
            e.delta_x > 0  # Dragging right
            and self.right_column_width > 350
        ):
            self.right_column_width -= e.delta_x
            self.output_area.width = self.right_column_width
            self.output_area.update()

            # Dynamically adjust middle column width
            middle_width += e.delta_x
            self.filter_area.width = middle_width
            self.filter_area.update()

    def build(self) -> Row:
        return Row(
            [
                self.input_area,
                ft.GestureDetector(
                    content=ft.VerticalDivider(width=7, color=ft.colors.GREY, thickness=1),
                    drag_interval=10,
                    on_pan_update=self.move_left_divider,
                    on_hover=self.show_draggable_cursor,
                ),
                self.filter_area,
                ft.GestureDetector(
                    content=ft.VerticalDivider(width=7, color=ft.colors.GREY, thickness=1),
                    drag_interval=10,
                    on_pan_update=self.move_right_divider,
                    on_hover=self.show_draggable_cursor,
                ),
                self.output_area,
            ],
            spacing=0,
            expand=True,
            height=self.page.height if self.page else None,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _build_input_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Enter names (one per line)", weight=ft.FontWeight.BOLD),
                    Container(
                        content=self.input_area,
                        expand=True,
                    ),
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            alignment=ft.alignment.top_left,
            width=self.left_column_width,
        )

    def _build_divider(self) -> VerticalDivider:
        return VerticalDivider(width=7, color=ft.colors.GREY, thickness=1)

    def _build_filter_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Group Formation Settings:", weight=ft.FontWeight.BOLD),
                    Row(
                        controls=[
                            self.group_size_input,
                            self.group_num_input,
                        ],
                        spacing=10,
                    ),
                    Divider(height=1, color=ft.colors.GREY_400),
                    Text("Gender filler:", weight=ft.FontWeight.BOLD),
                    RadioGroup(
                        value=self.selected_gender_filter,
                        on_change=self.update_selected_gender,
                        content=Column(
                            [
                                Radio(value="none", label="None"),
                                Row(
                                    [
                                        Radio(value="male"),
                                        self.male_count_input,
                                        Text(" males"),
                                    ],
                                    spacing=8,
                                ),
                                Row(
                                    [
                                        Radio(value="female"),
                                        self.female_count_input,
                                        Text(" females"),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                    self.generate_button,
                    self.clear_result_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=20,
            alignment=ft.alignment.top_left,
        )

    def clear_result(self, e: ControlEvent) -> None:
        """Clear the generated result and disable the clear button."""
        self.output_text.value = ""
        self.output_text.update()
        self.output_label.value = "Generated name:"
        self.clear_result_button.disabled = True
        self.clear_result_button.update()
        self.output_area.update()
        self.clear_result_button.update()

    def copy_to_clipboard(self, e: ControlEvent) -> None:
        """Copy generated names to clipboard."""
        if self.output_text.value:
            self.page.set_clipboard(self.output_text.value)
            self.page.show_snack_bar(ft.SnackBar(content=Text("Copied to clipboard!")))

    def update_selected_gender(self, e: ControlEvent) -> None:
        self.selected_gender_filter = e.control.value

        if self.selected_gender_filter == "none":
            # Disable both male and female inputs when "None" is selected
            self.male_count_input.value = ""
            self.male_count_input.disabled = True
            self.male_count_input.update()

            self.female_count_input.value = ""
            self.female_count_input.disabled = True
            self.female_count_input.update()

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

        self.show_gender_column = self.selected_gender_filter != "none"
        if self.show_gender_column:
            self.gender_column.visible = True
            self.update()
        elif not self.show_gender_column:
            self.gender_column.visible = False
            self.update()

    def _build_output_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Row(
                        controls=[
                            self.output_label,
                            self.copy_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.output_text,
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=20,
            alignment=ft.alignment.top_left,
            width=self.right_column_width,
        )

    def update_group_size(self, e):
        try:
            # Lấy danh sách các tên
            names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
            total_names = len(names)

            # Kiểm tra đầu vào là số nguyên dương
            size = int(e.control.value)
            if size <= 0:
                e.control.error_text = "Must be positive"
            else:
                e.control.error_text = None

                # Tính toán số lượng nhóm dựa trên kích thước tối đa của nhóm
                num_groups = (total_names + size - 1) // size  # Làm tròn lên
                self.group_num_input.value = str(num_groups)

            # Cập nhật giao diện
            self.group_num_input.update()
            e.control.update()

        except ValueError:
            e.control.error_text = "Must be a number"
            e.control.update()

    def update_group_num(self, e):
        try:
            # Lấy danh sách các tên
            names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
            total_names = len(names)

            # Kiểm tra đầu vào là số nguyên dương
            num = int(e.control.value)
            if num <= 0:
                e.control.error_text = "Must be positive"
            else:
                e.control.error_text = None

                # Tính toán kích thước tối đa của nhóm dựa trên số lượng nhóm
                max_size = (total_names + num - 1) // num
                self.group_size_input.value = str(max_size)

            # Cập nhật giao diện
            self.group_size_input.update()
            e.control.update()

        except ValueError:
            e.control.error_text = "Must be a number"
            e.control.update()

    def form_groups(self, e):
        try:
            group_size = int(self.group_size_input.value or 0)
            group_num = int(self.group_num_input.value or 0)

        except ValueError:
            return

        if self.selected_gender_filter == "none":
            names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
            if not names:
                return

            generated_groups = self.controller.form_groups(names, group_size, group_num)

        else:
            # return list[tuple[name, gender]
            names = self.groupformer.get_cleaned_names(self.names_input.value, self.gender_input.value)
            try:
                male_count = int(self.male_count_input.value) if self.selected_gender_filter == "male" else 0
            except ValueError:
                male_count = 0

            try:
                female_count = int(self.female_count_input.value) if self.selected_gender_filter == "female" else 0
            except ValueError:
                female_count = 0

            # form group
            generated_groups = self.groupformer.generate_names_with_gender(
                names, male_count=male_count, female_count=female_count, group_size=group_size, num_groups=group_num
            )

        # Format output
        output = []
        for i, group in enumerate(generated_groups, 1):
            output.append(f"Group {i}:")
            output.extend(f"  • {name}" for name in group)
            output.append("")  # Empty line between groups

            self.output_text.value = "\n".join(output).strip()
            self.clear_result_button.disabled = False
            self.clear_result_button.update()
            self.output_text.update()
            self.output_area.update()

    def show_draggable_cursor(self, e: ft.HoverEvent) -> None:
        """Show draggable cursor when hovering over the divider."""
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()
