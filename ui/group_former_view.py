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
        self.manual_group = "none"
        self.manually_assigned_names = []
        self.existing_groups = None

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
        self.error_message = ft.Text(
            value="", 
            color="red", 
            size=12,  
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
        self.output_text = Container(
            content=Column(
                controls=[],
                spacing=5,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )
        self.output_area = self._build_output_area()

    def build(self) -> Row:
        return Row(
            [
                self._build_input_area(),
                self._build_divider(),
                self._build_filter_area(),
                self._build_divider(),
                self.output_area,
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
                        content=self.input_area,
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
                    Row(
                        controls=[
                            self.group_size_input,
                            self.group_num_input,
                        ],
                        spacing=10,
                    ),
                    Divider(height=1, color=ft.colors.GREY_400),
                    # Text("Gender filler:", weight=ft.FontWeight.BOLD),
                    RadioGroup(
                        value=self.selected_gender_filter,
                        on_change=self.update_selected_gender,
                        content=Column(
                            [
                                Text("Gender filler:", weight=ft.FontWeight.BOLD),
                                self.error_message,
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
                    Text("Manually Assign:", weight=ft.FontWeight.BOLD),
                    RadioGroup(
                        value=self.manual_group,  # = 'none'
                        on_change=self.update_selected_manual_group,
                        content=Column([
                            Row([
                                # Text('Manually Assign:',weight=ft.FontWeight.BOLD),
                                Radio(value="none", label="None"),
                                Radio(value="manual", label="Manual"),
                            ])
                        ]),
                    ),
                    self.generate_button,
                    self.clear_result_button,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )

    def clear_result(self, e: ControlEvent) -> None:
        """Clear the generated result and disable the clear button."""
        self.output_text.content.controls.clear()
        self.manually_assigned_names = []
        self.existing_groups = None

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

    def update_selected_manual_group(self, e: ControlEvent) -> None:
        self.manual_group = e.control.value  # Lưu trạng thái mới

        for group_box in self.output_text.content.controls:
            group_box.disabled = self.manual_group == "none"  # Vô hiệu hóa nếu chọn "none"
            group_box.update()

        self.output_text.update()

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

    # STRATING
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
                self.create_empty_group_boxes(num_groups)

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
                self.create_empty_group_boxes(num)

            # Cập nhật giao diện
            self.group_size_input.update()
            e.control.update()

        except ValueError:
            e.control.error_text = "Must be a number"
            e.control.update()

    def create_empty_group_boxes(self, num_groups):
        self.output_text.content.controls.clear()  # Xóa các ô cũ

        for i in range(1, num_groups + 1):
            group_box = TextField(
                label=f"Group {i}",
                value="",  # Không có nội dung
                multiline=True,
                width=200,
                height=100,
                text_align=ft.TextAlign.LEFT,
                border=ft.border.all(1, ft.colors.GREY_300),
                disabled=(self.manual_group == "none"),  # Không cho phép chỉnh sửa
            )
            self.output_text.content.controls.append(group_box)

        self.output_text.update()
        self.output_area.update()

    def form_groups(self, e):
        # số lượng group và group size
        try:
            group_size = int(self.group_size_input.value or 0)
            group_num = int(self.group_num_input.value or 0)

        except ValueError:
            return

        # clean names
        if self.selected_gender_filter == "none":
            # Không lọc giới tính
            names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
        else:
            # Lọc giới tính: trả về danh sách tuple (name, gender)
            names = self.groupformer.get_cleaned_names(self.names_input.value, self.gender_input.value)

        total_names = len(names)
        if not names:
            return

        # xử lí số lượng giới tính
        male_count = 0
        female_count = 0
        if self.selected_gender_filter == "male":
            try:
                male_count = int(self.male_count_input.value) if self.selected_gender_filter == "male" else 0
            except ValueError:
                male_count = 0
        elif self.selected_gender_filter == "female":
            try:
                female_count = int(self.female_count_input.value) if self.selected_gender_filter == "female" else 0
            except ValueError:
                female_count = 0

    # check thông báo không đủ nam/nữ:
        if self.selected_gender_filter != "none":
            total_male = len([name for name, gender in names if gender == "male"])
            total_female = len([name for name, gender in names if gender == "female"])

            if total_male < male_count * group_num:
                self.error_message.value = (
                    f"Not enough males! Required: {male_count * group_num}, Available: {total_male}"
                )
                self.error_message.update()
            
            if total_female < female_count * group_num:
                self.error_message.value = (
                    f"Not enough females! Required: {female_count * group_num}, Available: {total_female}"
                )
                self.error_message.update()
            else:
                self.error_message.value = ""
        # Check thông báo nếu đủ giới tính
        self.error_message.update()

        # chia nhóm không có manual
        if self.selected_gender_filter == "none" and self.manual_group == "none":
            generated_groups = self.controller.form_groups(names, group_size, group_num)

        elif self.selected_gender_filter != "none" and self.manual_group == "none":
            generated_groups = self.groupformer.generate_names_with_gender(
                names, male_count=male_count, female_count=female_count, group_size=group_size, num_groups=group_num
            )

        # chia nhóm có manual
        elif self.manual_group != "none":
            # no gender
            if self.existing_groups is None and self.selected_gender_filter == "none":
                # print('is none')
                group_size = (total_names + group_num - 1) // group_num
                self.existing_groups = [[] for _ in range(group_num)]

                manually_assigned = []
                k = 0
                for group_box in self.output_text.content.controls:
                    # if not group_box.disabled:  # Nếu ô không bị disable, lấy tên nhập tay
                    group_members = [n.strip() for n in group_box.value.splitlines() if n.strip()]
                    self.existing_groups[k].extend(group_members)
                    manually_assigned.extend(group_members)
                    k += 1

                self.manually_assigned = manually_assigned

            remaining_names = []

            if self.selected_gender_filter == "none":
                remaining_names = [name for name in names if name not in self.manually_assigned]
                generated_groups = self.groupformer.manual_group_without_gender(
                    remaining_names=remaining_names,
                    existing_group=self.existing_groups,
                    group_size=group_size,
                    num_groups=group_num,
                )

            # with gender
            if self.existing_groups is None and self.selected_gender_filter != "none":
                group_size = (total_names + group_num - 1) // group_num
                self.existing_groups = [[] for _ in range(group_num)]

                manually_assigned = []
                k = 0

                for group_box in self.output_text.content.controls:
                    # if not group_box.disabled:  # Nếu ô không bị disable, lấy tên nhập tay
                    group_memberss = [n.strip() for n in group_box.value.splitlines() if n.strip()]
                    group_members = [
                        (name, gender) for name, gender in names if name in group_memberss
                    ]  # list các tuple(assigned_name, gender)
                    self.existing_groups[k].extend(group_members)
                    manually_assigned.extend(group_memberss)
                    k += 1
                self.manually_assigned = manually_assigned  # các tên đã được điền

            elif self.selected_gender_filter != "none":
                remaining_names = [(name, gender) for name, gender in names if name not in self.manually_assigned]
                generated_groups = []
                generated_groups = self.groupformer.manual_group_with_gender(
                    remaining_names=remaining_names,
                    existing_group=self.existing_groups,
                    male_count=male_count,
                    female_count=female_count,
                    group_size=group_size,
                    num_groups=group_num,
                )

        # STARTING
        # Format output
        self.output_text.content.controls.clear()
        self.output_area.update()
        self.output_text.update()
        for i, group in enumerate(generated_groups, 1):
            group_text = "\n".join([f"{name}" for name in group])  # Create the text for the group

            # Use a TextField to display the group information
            group_box = TextField(
                label=f"Group {i}",
                value=f"{group_text}",  # Group name and members
                multiline=True,  # Allow multiple lines
                width=200,  # Adjust width of the TextField
                height=100,  # Adjust height of the TextField
                text_align=ft.TextAlign.LEFT,  # Align text to the left
                border=ft.border.all(1, ft.colors.GREY_300),  # Optional: Add border for styling
            )
            self.output_text.content.controls.append(group_box)

        self.output_area.update()
        self.output_text.update()
        self.clear_result_button.disabled = False
        self.clear_result_button.update()
