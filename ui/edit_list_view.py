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
)
import logging

logger = logging.getLogger(__name__)


class EditListView(UserControl):
    def __init__(self, page: Page, controller, list_data: dict) -> None:
        super().__init__()
        self.page = page
        self.controller = controller
        self.list_data = list_data

        # State Management
        self.filtered_items = list_data.get("items", []).copy()
        self.item_search_query = ""
        self.is_editing = False
        self.has_unsaved_changes = False

        logger.info("Initializing EditListView")
        self._init_components()

    def _init_components(self):
        """Initialize components for List Details"""
        self.list_name_field = TextField(
            label="List Name",
            value=self.list_data["name"],
            expand=True,
            on_change=lambda e: self.mark_as_changed(),
        )
        self.item_search_field = TextField(
            prefix_icon=ft.icons.SEARCH,
            suffix_icon=ft.icons.CLEAR,
            hint_text="Search items...",
            on_change=self._handle_item_search,
            expand=True,
        )

    def build(self):
        """Build the edit list view"""
        logger.debug("Building EditListView")

        # Create items table
        self.items_table = DataTable(
            columns=[
                DataColumn(Text("Name")),
                DataColumn(Text("Actions")),
            ],
            rows=[self._create_item_row(item) for item in self.filtered_items],
        )

        return Container(
            content=Column([
                Row([
                    IconButton(icon=ft.icons.ARROW_BACK, tooltip="Back to lists", on_click=self._handle_back),
                ]),
                Row([
                    self.list_name_field,
                    IconButton(icon=ft.icons.PLAY_LESSON_OUTLINED, tooltip="Use list", on_click=self._handle_use_list),
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
            ]),
            expand=True,
            padding=20,
        )

    def _create_item_row(self, item):
        """Create a row for the items table"""
        return DataRow(
            cells=[
                DataCell(Text(item["name"])),
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

    def _handle_save(self, e):
        """Handle save button click"""
        try:
            self.list_data["name"] = self.list_name_field.value
            self.list_data["items"] = self.filtered_items

            if self.controller.save_list(self.list_data):
                self.has_unsaved_changes = False
                self.page.show_snack_bar(ft.SnackBar(content=Text("Changes saved successfully!")))
            else:
                self.page.show_snack_bar(ft.SnackBar(content=Text("Error saving changes!")))
        except Exception as e:
            logger.error(f"Error saving list: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error saving changes!")))

    def _handle_use_list(self, e):
        """Handle use list button click"""
        self.controller.use_list(self.list_data["id"])

    def _handle_item_search(self, e):
        """Handle item search"""
        self.item_search_query = e.control.value.lower()
        self._update_items_table()

    def _update_items_table(self):
        """Update the items table with filtered items"""
        filtered = self.filtered_items
        if self.item_search_query:
            filtered = [item for item in self.filtered_items if self.item_search_query in item["name"].lower()]

        self.items_table.rows = [self._create_item_row(item) for item in filtered]
        self.items_table.update()

    def mark_as_changed(self):
        """Mark that there are unsaved changes"""
        if not self.has_unsaved_changes:
            self.has_unsaved_changes = True
            logger.debug("Marked list as having unsaved changes")

    def _show_unsaved_changes_dialog(self, on_confirm):
        """Show dialog for unsaved changes"""

        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def confirm_action(e):
            close_dialog(e)
            on_confirm()

        dialog = AlertDialog(
            title=Text("Unsaved Changes"),
            content=Text("You have unsaved changes. Do you want to continue?"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Continue", on_click=confirm_action),
            ],
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
            self.mark_as_changed()
            self._update_items_table()
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error adding item!")))

    def _handle_edit_item(self, item):
        """Handle editing an item"""
        try:

            def close_dialog(e):
                dialog.open = False
                self.page.update()

            def save_changes(e):
                try:
                    item["name"] = name_field.value.strip()
                    self.mark_as_changed()
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

            dialog = AlertDialog(
                title=Text("Edit Item"),
                content=Column([name_field], tight=True),
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
                    self.mark_as_changed()
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
