import flet as ft
from flet import (
    UserControl,
    Row,
    Column,
    Row,
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
    Dropdown
)


class GroupFormationView(UserControl):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Initialize input fields
        self.names_input = TextField(
            multiline=True,
            min_lines=8,
            max_lines=20,
            expand=True,
            border=ft.InputBorder.OUTLINE,
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

        self.gender_filter = Radio(value="none")
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

        self.generate_button = ElevatedButton(
            text="Generate Groups",
            
            width=200,
            height=50,
            on_click=self.form_groups,
        )

        self.output_label = Text("Generated Groups:", weight=ft.FontWeight.BOLD)
        self.output_text = Text(
            "",
            style=ft.TextThemeStyle.HEADLINE_SMALL,
            weight=ft.FontWeight.BOLD,
        )

    def build(self) -> Row:
        return Row(
            [
                self._build_input_area(),
                self._build_divider(),
                self._build_filter_area(),
                self._build_divider(),
                self._build_output_area(),
            ],
            spacing=0,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _build_input_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Enter names (one per line)", weight=ft.FontWeight.BOLD),
                    Container(
                        content=self.names_input,
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
        return VerticalDivider(width=7, color=ft.colors.GREY, thickness=1)

    def _build_filter_area(self) -> Container:
        return Container(
            content=Column(
                [
                    Text("Group Formation Settings:", weight=ft.FontWeight.BOLD),
                    self.group_size_input,
                    self.group_num_input,
                    Divider(height=1, color=ft.colors.GREY_400),
                    Text("Gender filler:", weight=ft.FontWeight.BOLD),
                    RadioGroup(
                        value=self.gender_filter,
                        on_change=self.update_selected_gender,
                        content=Column(
                            [
                                Radio(value="none", label="None"),
                                Row(
                                    [
                                        Radio(value="male", label="Fix "),
                                        self.male_count_input,
                                        Text(" males"),
                                    ],
                                    spacing=8,
                                ),
                                Row(
                                    [
                                        Radio(value="female", label="Fix "),
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
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )
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
    def _build_output_area(self) -> Container:
        return Container(
            content=Column(
                [
                    self.output_label,
                    self.output_text,
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
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
        names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
        try:
            group_size = int(self.group_size_input.value or 0)
            group_num = int(self.group_num_input.value or 0)

            if not names:
                return

            generated_groups = self.controller.form_groups(names, group_size, group_num)

            # Format output
            output = []
            for i, group in enumerate(generated_groups, 1):
                output.append(f"Group {i}:")
                output.extend(f"  • {name}" for name in group)
                output.append("")  # Empty line between groups

            self.output_text.value = "\n".join(output).strip()
            self.output_text.update()
            self.output_area.update()
            


        except ValueError:
            return
