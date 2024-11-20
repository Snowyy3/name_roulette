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
from model.list_model import ListModel

from typing import Callable, Optional

logger = logging.getLogger(__name__)


class EditListView(UserControl):
    def __init__(self, page: Page, controller, list_data: dict | ListModel) -> None:
        super().__init__()
        self.page = page
        self.controller = controller
        # Ensure we handle both dict and ListModel inputs
        if isinstance(list_data, dict):
            self.list_model = ListModel(list_data)
        else:
            self.list_model = list_data
        self.original_model = ListModel(self.list_model.to_dict())

        # State Management
        self.filtered_items = self.list_model.items.copy()
        self.item_search_query = ""
        self.is_editing = False
        self.has_unsaved_changes = False
        self.persistent_item_search = ""  # Add persistent search state

        logger.info("Initializing EditListView")
        self._init_components()

        # Initialize and configure the items table first
        self.items_table = None  # Remove initial DataTable creation

        # Initialize lists view
        self.available_lists = ListView(
            controls=[],
            expand=True,
        )
        self._populate_available_lists()

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
            value=self.list_model.name,
            expand=True,
            on_change=self._handle_name_change,
            hint_text="Enter list name",
            helper_text="Name cannot be empty",
            # Remove error_text from here - it should only be set when validation fails
            on_submit=self._validate_name,
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

        self._init_items_table()
        return Container(
            content=Row(
                controls=[
                    self._build_left_column(),
                    ft.VerticalDivider(width=1, color=ft.colors.OUTLINE),
                    self._build_right_column(),
                ],
                expand=True,
            ),
            padding=20,
            expand=True,
        )

    def _init_items_table(self):
        """Initialize the items table"""
        self.items_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Gender")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=self._get_filtered_item_rows(),
        )

    def _build_left_column(self):
        """Build the left column containing list editing controls"""
        return Container(
            content=Column(
                controls=[
                    self._build_header_row(),
                    ft.Divider(height=1, color=ft.colors.OUTLINE),
                    self._build_search_row(),
                    Container(content=self.items_table, expand=True),
                ],
                expand=True,
            ),
            expand=6,
            margin=ft.margin.only(right=10),
        )

    def _build_header_row(self):
        """Build the header row with name field and actions"""
        return Row([
            self.list_name_field,
            self.use_list_button,
            IconButton(icon=ft.icons.SAVE, tooltip="Save changes", on_click=self._handle_save),
        ])

    def _build_search_row(self):
        """Build the search row with search field and add button"""
        return Row([
            self.item_search_field,
            IconButton(icon=ft.icons.ADD, tooltip="Add item", on_click=self._handle_add_item),
        ])

    def _build_right_column(self):
        """Build the right column containing available lists"""
        return Container(
            content=Column(
                controls=[
                    self._build_list_search_field(),
                    Container(
                        content=self.available_lists,
                        expand=True,
                        margin=ft.margin.only(top=10),
                    ),
                ],
                expand=True,
            ),
            expand=4,
            margin=ft.margin.only(left=10),
        )

    def _build_list_search_field(self):
        """Build the search field for available lists"""
        return TextField(
            prefix_icon=ft.icons.SEARCH,
            hint_text="Search available lists...",
            on_change=self._handle_list_search,
            expand=True,
        )

    def _get_filtered_item_rows(self):
        """Get filtered item rows for the table"""
        filtered = self.filtered_items
        if self.persistent_item_search:
            filtered = [item for item in self.filtered_items if self.persistent_item_search in item["name"].lower()]
        return [self._create_item_row(item) for item in filtered]

    def _create_available_lists_view(self):
        """Create the available lists view"""
        return self.available_lists

    def _populate_available_lists(self):
        """Populate the available lists view"""
        available_lists = self.controller.list_controller.get_all_lists()
        self.available_lists.controls = [
            ListTile(
                title=Text(lst.name),  # Use property access
                leading=Icon(ft.icons.LIST_ALT),
                on_click=lambda e, id=lst.id: self._handle_list_select(id),
            )
            for lst in available_lists
        ]

    def _handle_list_search(self, e):
        """Handle searching through available lists"""
        query = e.control.value.lower()
        all_lists = self.controller.list_controller.get_all_lists()
        filtered_lists = [lst for lst in all_lists if query in lst.name.lower()]  # Use property access

        self.available_lists.controls = [
            ListTile(
                title=Text(lst.name),  # Use property access
                leading=Icon(ft.icons.LIST_ALT),
                on_click=lambda e, id=lst.id: self._handle_list_select(id),  # Use property access
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
            self.list_model = selected_list  # It's already a ListModel, no need to convert
            self.original_model = ListModel(selected_list.to_dict())
            self.list_name_field.value = selected_list.name  # Use property access
            self.filtered_items = selected_list.items  # Reference items directly
            self.has_unsaved_changes = False
            self._update_items_table()
            self.list_name_field.update()

    def _create_item_row(self, item):
        """Create a row for the items table with optional fields"""
        return DataRow(
            cells=[
                DataCell(Text(item.get("name", ""))),  # Use get() for safety
                DataCell(Text(item.get("gender", ""))),  # Use get() for safety
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
        """Handle save operation with validation"""
        try:
            is_valid, error = self.controller.validate_list(self.list_model)
            if not is_valid:
                self.page.show_snack_bar(SnackBar(content=Text(error), bgcolor=ft.colors.ERROR))
                return False

            if self.controller.save_list(self.list_model):
                self.has_unsaved_changes = False
                self.original_model = ListModel(self.list_model.to_dict())
                self.page.show_snack_bar(
                    SnackBar(content=Text("Changes saved successfully!"), bgcolor=ft.colors.SUCCESS)
                )
                return True
            return False
        except Exception as e:
            self._handle_error("Error saving list", e)
            return False

    def _handle_use_list(self, target_view: View):
        """Handle using the list in different views"""
        if self.has_unsaved_changes:
            self._show_unsaved_changes_dialog(lambda: self._use_list_in_view(target_view))
        else:
            self._use_list_in_view(target_view)

    def _use_list_in_view(self, target_view: View):
        """Use the list in the specified view"""
        try:
            # Save current list state to controller
            self.controller.set_active_list(self.list_model)

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

    def show_confirmation_dialog(
        self,
        title: str,
        content: str,
        on_confirm: Callable,
        on_cancel: Optional[Callable] = None,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        is_destructive: bool = False,
    ):
        def handle_cancel(e):
            dialog.open = False
            self.page.update()
            if on_cancel:
                on_cancel()

        def handle_confirm(e):
            dialog.open = False
            self.page.update()
            on_confirm()

        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton(cancel_text, on_click=handle_cancel),
                ft.TextButton(
                    confirm_text,
                    on_click=handle_confirm,
                    style=ft.ButtonStyle(color=ft.colors.ERROR if is_destructive else ft.colors.PRIMARY),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_unsaved_changes_dialog(
        self, on_save: Callable, on_discard: Callable, on_cancel: Optional[Callable] = None
    ):
        def handle_save(e):
            if on_save():
                dialog.open = False
                self.page.update()

        def handle_discard(e):
            dialog.open = False
            self.page.update()
            on_discard()

        def handle_cancel(e):
            dialog.open = False
            self.page.update()
            if on_cancel:
                on_cancel()

        dialog = ft.AlertDialog(
            title=ft.Text("Unsaved Changes"),
            content=ft.Text("You have unsaved changes. What would you like to do?"),
            actions=[
                ft.TextButton("Cancel", on_click=handle_cancel),
                ft.TextButton("Discard", on_click=handle_discard),
                ft.TextButton(
                    "Save",
                    on_click=handle_save,
                    style=ft.ButtonStyle(color=ft.colors.PRIMARY),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _show_unsaved_changes_dialog(self, on_confirm):
        """Show dialog for unsaved changes"""
        self.show_unsaved_changes_dialog(lambda: self._handle_save(None), on_confirm)

    def _handle_add_item(self, e):
        """Handle adding a new item"""
        success, new_item, error = self.controller.add_item_to_list(self.list_model, "")
        if success:
            self.filtered_items.append(new_item)
            self._check_for_changes()
            self._update_items_table()
            self._handle_edit_item(new_item)
        else:
            self._handle_error("Error adding item", Exception(error))

    def _handle_edit_item(self, item):
        """Handle editing an item with validation"""
        try:
            name_field = TextField(
                label="Name",
                value=item.get("name", ""),  # Use get() for safety
                autofocus=True,
            )
            gender_field = TextField(
                label="Gender (optional)",
                value=item.get("gender", ""),  # Use get() for safety
            )

            def save_changes(e):
                success, error = self.controller.update_item_in_list(
                    self.list_model,
                    item.get("id", ""),  # Use get() for safety
                    name_field.value.strip(),
                    gender_field.value.strip() or None,
                )
                if success:
                    self._check_for_changes()
                    self._update_items_table()
                    self._close_dialog(e)
                else:
                    name_field.error_text = error
                    name_field.update()

            dialog = AlertDialog(
                title=Text("Edit Item"),
                content=Column([name_field, gender_field], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=self._close_dialog),
                    ft.TextButton("Save", on_click=save_changes),
                ],
            )
            self._show_dialog(dialog)

        except Exception as e:
            self._handle_error("Error editing item", e)

    def _create_edit_item_dialog(self, item):
        """Create the edit item dialog"""
        name_field = TextField(
            label="Name",
            value=item["name"],
            autofocus=True,
        )
        gender_field = TextField(
            label="Gender (optional)",
            value=item.get("gender", ""),
        )

        def save_changes(e):
            if self._validate_and_save_item(item, name_field, gender_field):
                self._close_dialog(e)

        return AlertDialog(
            title=Text("Edit Item"),
            content=Column([name_field, gender_field], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=self._close_dialog),
                ft.TextButton("Save", on_click=save_changes),
            ],
        )

    def _validate_and_save_item(self, item, name_field, gender_field):
        """Validate and save item changes"""
        name = name_field.value.strip()
        is_valid, error_msg = self._validate_item(name)

        if not is_valid:
            name_field.error_text = error_msg
            name_field.update()
            return False

        try:
            self._update_item(item, name, gender_field.value.strip())
            self._check_for_changes()
            self._update_items_table()
            return True
        except Exception as e:
            self._handle_error("Error saving item changes", e)
            return False

    def _update_item(self, item, name, gender):
        """Update item with new values"""
        item["name"] = name
        if gender:
            item["gender"] = gender
        elif "gender" in item:
            del item["gender"]

    def _handle_error(self, message: str, error: Exception):
        """Handle errors uniformly"""
        logger.error(f"{message}: {error}")
        self.page.show_snack_bar(SnackBar(content=Text(f"{message}!"), bgcolor=ft.colors.ERROR))

    def _show_dialog(self, dialog):
        """Show a dialog"""
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _close_dialog(self, e=None):
        """Close the current dialog"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _handle_delete_item(self, item):
        """Handle deleting an item"""

        def confirm_delete():
            success, error = self.controller.delete_item_from_list(self.list_model, item["id"])
            if success:
                self.filtered_items.remove(item)
                self._check_for_changes()
                self._update_items_table()
            else:
                self._handle_error("Error deleting item", Exception(error))

        self.show_confirmation_dialog(
            "Confirm Delete",
            f"Are you sure you want to delete '{item['name']}'?",
            confirm_delete,
            is_destructive=True,
        )

    def _handle_name_change(self, e):
        """Handle list name changes"""
        self.list_model.name = e.control.value
        self._check_for_changes()

    def _check_for_changes(self):
        """Check if current data differs from original data"""
        try:
            self.has_unsaved_changes = not self.list_model.equals(self.original_model)
            logger.debug(f"Unsaved changes: {self.has_unsaved_changes}")
        except Exception as e:
            logger.error(f"Error checking for changes: {e}")
            self.has_unsaved_changes = True  # Assume changes on error

    def _validate_name(self, e=None) -> bool:
        """Validate list name using controller"""
        name = self.list_name_field.value.strip()

        if not name:
            self.list_name_field.error_text = "Name cannot be empty"
            self.list_name_field.update()
            return False
        else:
            self.list_name_field.error_text = None  # Clear error when name is not empty
            self.list_name_field.update()
            return True
