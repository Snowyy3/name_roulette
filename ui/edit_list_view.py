import flet as ft
from flet import (
    UserControl,
    Page,
    Container,
    Column,
    Row,
    Text,
    TextField,
    IconButton,
    AlertDialog,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    PopupMenuButton,
    PopupMenuItem,
    SnackBar,
    ListTile,
    ListView,
    Icon,
)
from ui.views import View
import logging

logger = logging.getLogger(__name__)


class EditListView(UserControl):
    def __init__(self, page: Page, controller, list_data: dict) -> None:
        super().__init__()
        self.page = page
        self.controller = controller
        self.list_data = list_data
        self.original_data = dict(list_data)  # Store original data for comparison

        # State Management
        self.filtered_items = list_data.get("items", []).copy()
        self.item_search_query = ""
        self.is_editing = False
        self.has_unsaved_changes = False
        self.persistent_item_search = ""  # Add persistent search state

        # Initialize items table
        self.items_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Gender")),  # Optional column for gender
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[],  # Will be populated later
        )

        # Initialize lists view
        self.available_lists = ListView(
            controls=[],
            expand=True,
        )
        self._populate_available_lists()

        logger.info("Initializing EditListView")
        self._init_components()

        self.use_list_button = PopupMenuButton(
            content=IconButton(
                icon=ft.icons.PLAY_LESSON_OUTLINED,
                tooltip="Use list",
            ),
            items=[
                PopupMenuItem(
                    text="Use in Name Picker",
                    on_click=lambda e: self._handle_use_list(View.NAME_PICKER),
                ),
                PopupMenuItem(
                    text="Use in Group Former",
                    on_click=lambda e: self._handle_use_list(View.GROUP_FORMER),
                ),
            ],
        )

    def _init_components(self):
        """Initialize components for List Details"""
        self.list_name_field = TextField(
            label="List Name",
            value=self.list_data["name"],
            expand=True,
            on_change=self._handle_name_change,  # Update change handler
        )
        self.item_search_field = TextField(
            prefix_icon=ft.icons.SEARCH,
            suffix_icon=ft.icons.CLEAR,
            hint_text="Search items...",
            value=self.persistent_item_search,  # Set initial value from persistent state
            on_change=self._handle_item_search,
            on_submit=self._handle_item_search,  # Add submit handler
            expand=True,
        )

    def build(self):
        """Build the edit list view"""
        logger.debug("Building EditListView")

        # Left Column: Edit current list
        left_column = Column(
            controls=[
                Row([
                    self.list_name_field,
                    self.use_list_button,
                    IconButton(icon=ft.icons.SAVE, tooltip="Save changes", on_click=self._handle_save),
                ]),
                ft.Divider(height=1, color=ft.colors.OUTLINE),
                Row([
                    self.item_search_field,
                    IconButton(icon=ft.icons.ADD, tooltip="Add item", on_click=self._handle_add_item),
                ]),
                Container(
                    content=self.items_table,
                    expand=True,
                ),
            ],
            expand=True,
        )

        # Right Column: Available lists
        available_lists = self._create_available_lists_view()
        right_column = Column(
            controls=[
                TextField(
                    prefix_icon=ft.icons.SEARCH,
                    hint_text="Search available lists...",
                    on_change=self._handle_list_search,
                    expand=True,
                ),
                Container(
                    content=available_lists,
                    expand=True,
                    margin=ft.margin.only(top=10),
                ),
            ],
            expand=True,
        )

        # Main layout with two columns
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=left_column,
                        expand=6,  # Takes 60% of space
                        margin=ft.margin.only(right=10),
                    ),
                    ft.VerticalDivider(width=1, color=ft.colors.OUTLINE),
                    Container(
                        content=right_column,
                        expand=4,  # Takes 40% of space
                        margin=ft.margin.only(left=10),
                    ),
                ],
                expand=True,
            ),
            padding=20,
            expand=True,
        )

    def _create_available_lists_view(self):
        """Create the available lists view"""
        return self.available_lists

    def _populate_available_lists(self):
        """Populate the available lists view"""
        self.available_lists.controls = [
            ListTile(
                title=Text(lst["name"]),
                leading=Icon(ft.icons.LIST_ALT),
                on_click=lambda e, id=lst["id"]: self._handle_list_select(id),
            )
            for lst in self.controller.list_controller.get_all_lists()
        ]

    def _handle_list_search(self, e):
        """Handle searching through available lists"""
        query = e.control.value.lower()
        all_lists = self.controller.list_controller.get_all_lists()
        filtered_lists = [lst for lst in all_lists if query in lst["name"].lower()]

        self.available_lists.controls = [
            ListTile(
                title=Text(lst["name"]),
                leading=Icon(ft.icons.LIST_ALT),
                on_click=lambda e, id=lst["id"]: self._handle_list_select(id),
            )
            for lst in filtered_lists
        ]
        self.available_lists.update()

    def _handle_list_select(self, list_id: str):
        """Handle selection of a list from the right column"""
        if self.has_unsaved_changes:
            self._show_unsaved_changes_dialog(lambda: self._load_selected_list(list_id))
        else:
            self._load_selected_list(list_id)

    def _load_selected_list(self, list_id: str):
        """Load the selected list data"""
        selected_list = self.controller.list_controller.get_list(list_id)
        if selected_list:
            self.list_data = dict(selected_list)
            self.original_data = dict(selected_list)
            self.list_name_field.value = selected_list["name"]
            self.filtered_items = selected_list.get("items", []).copy()
            self.has_unsaved_changes = False
            self._update_items_table()
            self.list_name_field.update()

    def _create_item_row(self, item):
        """Create a row for the items table with optional fields"""
        return DataRow(
            cells=[
                DataCell(Text(item["name"])),
                # Only show gender if it exists
                DataCell(Text(item.get("gender", ""))) if "gender" in item else DataCell(Text("")),
                DataCell(
                    Row([
                        IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Edit item",
                            on_click=lambda e, i=item: self._handle_edit_item(i),
                        ),
                        IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Delete item",
                            on_click=lambda e, i=item: self._handle_delete_item(i),
                        ),
                    ])
                ),
            ]
        )

    def _handle_back(self, e):
        """Handle back button click"""
        if self.has_unsaved_changes:
            self._show_unsaved_changes_dialog(lambda: self.controller.navigate_to_manage_lists())
        else:
            self.controller.navigate_to_manage_lists()

    def _handle_save(self, e) -> bool:
        """Handle save operation and return success status"""
        try:
            self.list_data["name"] = self.list_name_field.value
            self.list_data["items"] = self.filtered_items

            if self.controller.save_list(self.list_data):
                self.has_unsaved_changes = False
                self.original_data = dict(self.list_data)
                self.page.show_snack_bar(ft.SnackBar(content=Text("Changes saved successfully!")))
                return True
            else:
                self.page.show_snack_bar(ft.SnackBar(content=Text("Error saving changes!")))
                return False
        except Exception as e:
            logger.error(f"Error saving list: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error saving changes!")))
            return False

    def _handle_use_list(self, target_view: View):
        """Handle using the list in different views"""
        try:
            if self.has_unsaved_changes:
                self._show_unsaved_changes_dialog(lambda: self._use_list_in_view(target_view))
            else:
                self._use_list_in_view(target_view)
        except Exception as e:
            logger.error(f"Error using list: {e}")
            self.page.show_snack_bar(SnackBar(content=Text("Error using list!"), bgcolor="#ef4444"))

    def _use_list_in_view(self, target_view: View):
        """Use the list in the specified view"""
        try:
            # Save current list state to controller
            self.controller.set_active_list(self.list_data)

            # Navigate to target view using controller
            if target_view == View.NAME_PICKER:
                self.controller.navigate_to_name_picker()
            elif target_view == View.GROUP_FORMER:
                self.controller.navigate_to_group_former()

            self.page.show_snack_bar(
                SnackBar(
                    content=Text(f"List loaded in {target_view.name.replace('_', ' ').title()}"),
                    bgcolor="#10b981",
                )
            )
        except Exception as e:
            logger.error(f"Error setting active list: {e}")
            self.page.show_snack_bar(SnackBar(content=Text("Error loading list!"), bgcolor="#ef4444"))

    def _handle_item_search(self, e):
        """Handle item search"""
        self.persistent_item_search = e.control.value.lower()  # Update persistent state
        self._update_items_table()

    # Add method to clear search
    def clear_item_search(self):
        """Clear search field and reset filters"""
        self.item_search_field.value = ""
        self.persistent_item_search = ""
        self._update_items_table()
        self.item_search_field.update()

    def _update_items_table(self):
        """Update the items table with filtered items"""
        filtered = self.filtered_items
        if self.persistent_item_search:  # Use persistent search state
            filtered = [item for item in self.filtered_items if self.persistent_item_search in item["name"].lower()]

        self.items_table.rows = [self._create_item_row(item) for item in filtered]
        self.items_table.update()

    def mark_as_changed(self):
        """Mark that there are unsaved changes"""
        if not self.has_unsaved_changes:
            self.has_unsaved_changes = True
            logger.debug("Marked list as having unsaved changes")

    def _show_unsaved_changes_dialog(self, on_confirm):
        """Show enhanced dialog for unsaved changes with save option"""

        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def discard_changes(e):
            close_dialog(e)
            on_confirm()

        def save_and_continue(e):
            if self._handle_save():
                close_dialog(e)
                on_confirm()

        dialog = AlertDialog(
            title=Text("Unsaved Changes"),
            content=Text("You have unsaved changes. What would you like to do?"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Discard", on_click=discard_changes),
                ft.TextButton(
                    "Save",
                    on_click=save_and_continue,
                    style=ft.ButtonStyle(color=ft.colors.PRIMARY),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _handle_add_item(self, e):
        """Handle adding a new item"""
        try:
            new_item = {
                "name": "",  # Empty name for editing
                "id": str(len(self.filtered_items) + 1),  # Simple ID generation
            }
            self.filtered_items.append(new_item)
            self._check_for_changes()
            self._update_items_table()
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error adding item!")))

    def _handle_edit_item(self, item):
        """Handle editing an item with optional fields"""
        try:

            def close_dialog(e):
                dialog.open = False
                self.page.update()

            def save_changes(e):
                try:
                    item["name"] = name_field.value.strip()
                    if gender_field.value.strip():  # Only save gender if provided
                        item["gender"] = gender_field.value.strip()
                    self._check_for_changes()  # Check for changes after edit
                    self._update_items_table()
                    close_dialog(e)
                except Exception as e:
                    logger.error(f"Error saving item changes: {e}")
                    self.page.show_snack_bar(ft.SnackBar(content=Text("Error saving changes!")))

            name_field = TextField(
                label="Name",
                value=item["name"],
                autofocus=True,
            )

            gender_field = TextField(
                label="Gender (optional)",
                value=item.get("gender", ""),
            )

            dialog = AlertDialog(
                title=Text("Edit Item"),
                content=Column([name_field, gender_field], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dialog),
                    ft.TextButton("Save", on_click=save_changes),
                ],
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        except Exception as e:
            logger.error(f"Error showing edit dialog: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error editing item!")))

    def _handle_delete_item(self, item):
        """Handle deleting an item"""
        try:

            def close_dialog(e):
                dialog.open = False
                self.page.update()

            def confirm_delete(e):
                try:
                    self.filtered_items.remove(item)
                    self._check_for_changes()  # Check for changes after delete
                    self._update_items_table()
                    close_dialog(e)
                except Exception as e:
                    logger.error(f"Error deleting item: {e}")
                    self.page.show_snack_bar(ft.SnackBar(content=Text("Error deleting item!")))

            dialog = AlertDialog(
                title=Text("Confirm Delete"),
                content=Text(f"Are you sure you want to delete '{item['name']}'?"),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dialog),
                    ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.colors.ERROR)),
                ],
            )

            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        except Exception as e:
            logger.error(f"Error showing delete dialog: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error deleting item!")))

    def _handle_name_change(self, e):
        """Handle list name changes"""
        self.list_data["name"] = e.control.value
        self._check_for_changes()

    def _check_for_changes(self):
        """Check if current data differs from original data"""
        try:
            current_state = {"name": self.list_data["name"], "items": self.filtered_items}
            original_state = {"name": self.original_data["name"], "items": self.original_data["items"]}
            self.has_unsaved_changes = (
                current_state["name"] != original_state["name"]
                or len(current_state["items"]) != len(original_state["items"])
                or any(i1 != i2 for i1, i2 in zip(current_state["items"], original_state["items"]))
            )
            logger.debug(f"Unsaved changes: {self.has_unsaved_changes}")
        except Exception as e:
            logger.error(f"Error checking for changes: {e}")
