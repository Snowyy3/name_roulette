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
    # Audio,
    ControlEvent,
    IconButton,
    icons,
)
from . import group_former_ui_helper as ui_helper
import asyncio
import logging

logger = logging.getLogger(__name__)


class GroupFormationView(UserControl):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._initialize_state()
        self._initialize_ui_components()

    def _initialize_state(self):
        """Initialize state variables"""
        self.show_gender_column = False
        self.manual_group = "none"
        self.manually_assigned_names = []
        self.existing_groups = None
        self.remaining_names = []
        self.current_list = None
        self.remaining_counts = None
        self.last_updated = None
        self.selected_gender_filter = "none"

        # Column widths
        self.left_column_width = 500
        self.middle_column_min_width = 300
        self.right_column_width = 550

    def _initialize_ui_components(self):
        """Initialize all UI components"""
        # Audio components
        # self.randomize_sound = Audio(src="randomize.mp3", autoplay=False)
        # self.clear_sound = Audio(src="clear.mp3", autoplay=False)

        # Setup individual components first
        self._setup_input_fields()
        self._setup_buttons()
        self._setup_columns()

        # Create main areas
        self.input_area = self._build_input_row()  # Changed from _build_input_area()
        self.filter_area = self._build_filter_area()
        self.output_area = self._build_output_area()

    def _setup_input_fields(self):
        """Initialize input field components"""
        self.names_input = TextField(
            label="Name",
            multiline=True,
            min_lines=8,
            max_lines=20,
            expand=True,
            height=200,
            border=ft.InputBorder.OUTLINE,
            on_change=self._handle_input_change,
        )

        self.gender_input = TextField(
            label="Gender",
            multiline=True,
            min_lines=10,
            max_lines=20,
            height=200,
            expand=True,
        )

        self.error_message = ft.Text(
            value="",
            color="red",
            size=12,
        )
        self.error_message_manual = ft.Text(
            value="",
            color="red",
            size=12,
        )
        self.error_message_manual = ft.Text(
            value="",
            color="red",
            size=12,
        )

    def _setup_buttons(self):
        """Initialize button components"""
        # Copy button
        self.copy_button = IconButton(
            icon=icons.COPY_ALL_ROUNDED,
            icon_size=20,
            visible=True,
            tooltip="Copy to clipboard",
            on_click=self.copy_to_clipboard,
        )

        self.save_list_button = IconButton(
            icon=icons.BOOKMARK_ADD_OUTLINED,
            icon_size=20,
            tooltip="Save as list",
            on_click=self.handle_save_list_click,
        )

        self.generate_button = ElevatedButton(
            text="Generate Groups",
            width=200,
            height=50,
            on_click=self.handle_randomize_click,
        )

        self.clear_result_button = ElevatedButton(
            content=Row(
                [ft.Icon(icons.CLEAR_ROUNDED), Text("Clear Result")],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            on_click=self.clear_result,
            width=200,
            disabled=True,
            height=50,
        )

    def _setup_columns(self):
        """Setup column layouts"""
        # Base columns
        self.name_column = Column([self.names_input], expand=2)
        self.gender_column = Column([self.gender_input], visible=self.show_gender_column, expand=1)

        # Input area row (will be replaced by _build_input_area later)
        self.input_row = Row([self.name_column, self.gender_column], spacing=10, expand=True)

        # Output container setup
        self.output_text = Container(
            content=Column(controls=[], spacing=20, expand=True, scroll=ft.ScrollMode.AUTO),
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )

        self.output_label = Row(
            [Text("Generated Groups:", weight=ft.FontWeight.BOLD), self.copy_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # Initialize input fields that filter_area will need
        self.group_size_input = TextField(
            label="Max Group Size",
            width=150,
            on_change=self.update_group_size,
            label_style=ft.TextStyle(size=14),
            border=ft.InputBorder.OUTLINE,
        )

        self.group_num_input = TextField(
            label="Number of Groups",
            width=150,
            on_change=self.update_group_num,
            label_style=ft.TextStyle(size=14),
            border=ft.InputBorder.OUTLINE,
        )

        # Gender count inputs
        self.male_count_input = TextField(
            value="", width=40, height=35, text_align="center", content_padding=8, disabled=True
        )

        self.female_count_input = TextField(
            value="", width=40, height=35, text_align="center", content_padding=8, disabled=True
        )

    def _handle_input_change(self, e):
        """Handle changes in the input fields"""
        try:
            new_size, new_num = self.controller.handle_input_change(
                names=self.names_input.value,
                group_size=self.group_size_input.value,
                group_num=self.group_num_input.value,
            )

            if new_size is not None:
                self.group_size_input.value = str(new_size)
                self.group_size_input.update()

            if new_num is not None:
                self.group_num_input.value = str(new_num)
                self.group_num_input.update()

        except Exception as e:
            logger.error(f"Error handling input change: {e}")

    def form_groups(self):
        """Delegate group formation to controller"""
        try:
            # Get basic parameters
            names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
            if not names:
                return

            group_size = int(self.group_size_input.value or 0)
            group_num = int(self.group_num_input.value or 0)

            # Handle gender-specific parameters
            male_count = 0
            female_count = 0
            if self.selected_gender_filter in ["male", "female"]:
                if self.selected_gender_filter == "male":
                    try:
                        male_count = int(self.male_count_input.value)
                    except ValueError:
                        male_count = 0
                else:
                    try:
                        female_count = int(self.female_count_input.value)
                    except ValueError:
                        female_count = 0

                # Get names with gender information
                names = self.controller.group_formation.group_former.get_cleaned_names(
                    self.names_input.value, self.gender_input.value
                )

            # Delegate to controller with all parameters
            ans = self.controller.form_groups(
                names,
                existing_groups=self.existing_groups,
                group_size=group_size,
                remaining_names=self.remaining_names,
                group_num=group_num,
                gender_filter=self.selected_gender_filter,
                male_count=male_count,
                female_count=female_count,
                manual_group=self.manual_group,
                output_text=self.output_text.content.controls,
            )
            if self.manual_group != "none":
                generated_groups = ans["generated_groups"]
                self.existing_groups = ans["existing_groups"]
                self.remaining_names = ans["remaining_names"]

                self._update_output_display(generated_groups)
            else:
                self._update_output_display(ans)

        except Exception as e:
            logger.error(f"Error forming groups: {e}")
            self.error_message.value = str(e)
            self.error_message.update()

    def _update_output_display(self, groups):
        """Update the output display with formed groups"""
        self.output_text.content.controls.clear()

        for i, group in enumerate(groups, 1):
            group_text = "\n".join([f"• {name}" for name in group])
            group_box = TextField(
                label=f"Group {i}",
                value=group_text,
                multiline=True,
                width=300,
                text_align=ft.TextAlign.LEFT,
                border=ft.border.all(1, ft.colors.GREY_300),
                on_change=self._handle_manual_input,
            )
            self.output_text.content.controls.append(group_box)

        self._update_ui_state()

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
                # self.randomize_sound,
                # self.clear_sound,
            ],
            spacing=0,
            expand=True,
            height=self.page.height if self.page else None,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _build_input_area(self) -> Container:
        return ui_helper.build_input_area(self)

    def _build_divider(self) -> VerticalDivider:
        return VerticalDivider(width=7, color=ft.colors.GREY, thickness=1)

    def _build_filter_area(self) -> Container:
        return ui_helper.build_filter_area(self)

    def handle_name_input(self, e):
        print("e")
        # Lấy giá trị từ tất cả các TextField trong output_text
        used_names = []
        for text_field in self.output_text.content.controls:
            if isinstance(text_field, ft.TextField):
                text_value = text_field.value.strip()
                if text_value:
                    used_names.extend(text_value.splitlines())

        # Tạo danh sách còn lại dựa trên các tên ban đầu
        name_only = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
        counts = self.groupformer.counting_name(names_only=name_only)

        # Trừ các tên đã sử dụng
        for name in used_names:
            if name in counts.keys():
                counts[name] -= 1

        # Lưu trạng thái cập nhật vào remaining_counts
        self.remaining_counts = counts

        # Kiểm tra tên vừa nhập
        input_name = e.control.value.strip()
        if input_name:
            if input_name in self.remaining_counts and self.remaining_counts[input_name] > 0:
                print("a")
                # Hợp lệ, giảm số lần còn lại
                self.remaining_counts[input_name] -= 1
                self.error_message_manual = None
            else:
                print("b")
                # Tên không hợp lệ
                self.error_message_manual.value = f"Name '{input_name}' is already used up!"
                e.control.value = ""  # Xóa giá trị không hợp lệ

        # Cập nhật TextField cho giao diện hiện tại
        for text_field in self.output_text.content.controls:
            if isinstance(text_field, ft.TextField):
                text_field.update()
                self.output_text.update()
                self.output_area.update()

        # Cập nhật TextField hiện tại
        e.control.update()
        self.output_text.update()
        self.output_area.update()

    def clear_result(self, e: ControlEvent) -> None:
        """Clear the generated result and disable the clear button."""
        self.output_text.content.controls.clear()
        self.manually_assigned_names = []
        self.existing_groups = None
        self.remaining_names = []
        self.create_empty_group_boxes(int(self.group_num_input.value))

        self.output_text.update()
        self.output_label.value = "Generated name:"
        self.clear_result_button.disabled = True
        self.clear_result_button.update()
        self.output_area.update()
        self.clear_result_button.update()
        # self.clear_sound.play()

    async def handle_save_list_click(self, e: ControlEvent) -> None:
        """Temporarily changes the icon to show save confirmation. Kind of like animating :)) fun, y'know"""
        self.save_list_button.icon = icons.BOOKMARK_ADDED
        self.save_list_button.update()
        await asyncio.sleep(3)
        self.save_list_button.icon = icons.BOOKMARK_ADD_OUTLINED
        self.save_list_button.update()

    def handle_randomize_click(self, e: ControlEvent) -> None:
        """Handles the randomize button click and plays a sound effect."""
        # self.randomize_sound.play()  # Play the sound effect
        self.form_groups()  # Removed 'e' parameter

    def copy_to_clipboard(self, e: ControlEvent) -> None:
        """Copy generated names to clipboard."""
        if self.output_text.content.controls:  # Kiểm tra nếu có nhóm trong output_text
            # Duyệt qua các controls trong output_text để lấy nội dung
            all_text = "\n\n".join([
                f"{control.label}:\n{control.value}"  # Thêm tiêu đề nhóm (label) và nội dung
                for control in self.output_text.content.controls
                if isinstance(control, ft.TextField)
            ])
            # Sao chép toàn bộ nội dung vào clipboard
            self.page.set_clipboard(all_text)
            # Hiển thị thông báo
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Copied to clipboard!")))

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
        return ui_helper.build_output_area(self)

    def addition_update_group_size_group_num(self, e):
        names = [n.strip() for n in self.names_input.value.splitlines() if n.strip()]
        total_names = len(names)

        if self.last_updated == "group_num":
            try:
                num = int(self.group_num_input.value)
                max_size = (total_names + num - 1) // num
                self.group_size_input.value = str(max_size)
                self.group_size_input.update()
            except ValueError:
                pass

        elif self.last_updated == "group_size":
            try:
                size = int(self.group_size_input.value)
                num_groups = (total_names + size - 1) // size
                self.group_num_input.value = str(num_groups)
                self.group_num_input.update()
            except ValueError:
                pass

    def update_group_size(self, e):
        self.last_updated = "group_size"
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
        self.last_updated = "group_num"
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

    def create_empty_group_boxes(self, num_groups: int) -> None:
        self.output_text.content.controls.clear()

        for i in range(1, num_groups + 1):
            group_box = ui_helper.create_group_box(i, self.manual_group == "none")
            self.output_text.content.controls.append(group_box)

        self.output_text.update()
        self.output_area.update()

    def show_draggable_cursor(self, e: ft.HoverEvent) -> None:
        """Show draggable cursor when hovering over the divider."""
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    def load_active_list(self):
        """Load and display the active list"""
        try:
            logger.info("Loading active list in GroupFormationView")
            self.current_list = self.controller.list_controller.get_selected_list()
            if self.current_list:
                self._populate_list_data()
                self.update()
        except Exception as e:
            logger.error(f"Error loading active list: {e}")

    def _populate_list_data(self):
        """Populate the view with active list data"""
        if not self.current_list:
            return

        try:
            # Get items from ListModel
            items = self.current_list.items

            # Format the names and genders
            names = [item.get("name", "") for item in items]
            genders = [item.get("gender", "") for item in items]

            # Update the input fields
            self.names_input.value = "\n".join(names)
            self.gender_input.value = "\n".join(genders)

            # Update the UI
            self.names_input.update()
            self.gender_input.update()

        except Exception as e:
            logger.error(f"Error populating list data: {e}")

    def _update_ui_state(self):
        """Update UI state after group formation"""
        self.output_area.update()
        self.output_text.update()
        self.clear_result_button.disabled = False
        self.clear_result_button.update()

    def _build_input_row(self) -> Container:
        """Build the initial input row before ui_helper builds the complete area"""
        return Container(
            content=self.input_row,  # Use the input_row we created in _setup_columns
            expand=True,
            padding=20,
            alignment=ft.alignment.top_left,
        )

    def _handle_manual_input(self, e):
        """Handle changes in the manual group input textfields."""
        try:
            # Get all current groups from the output text fields
            current_groups = []
            for text_field in self.output_text.content.controls:
                if isinstance(text_field, ft.TextField):
                    # Split the text into lines and clean them
                    names = [name.strip() for name in text_field.value.split("\n") if name.strip()]
                    current_groups.append(names)

            # Store the current groups for later use
            self.existing_groups = current_groups

            # Update the error message if needed
            self.error_message.value = ""
            self.error_message.update()

        except Exception as e:
            self.error_message.value = str(e)
            self.error_message.update()
            logger.error(f"Error handling manual input: {e}")
