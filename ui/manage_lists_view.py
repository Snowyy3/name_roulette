import flet as ft
from flet import UserControl, Page, Container, Column, Row, Text, TextField, GridView, IconButton, AlertDialog
import logging

# Configure logging
logging.basicConfig(
    filename="logs/app.log", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ManageListsView(UserControl):
    def __init__(self, page: Page, controller) -> None:
        super().__init__()
        self.page = page
        self.controller = controller

        # State Management
        self.lists_data = []  # Store all lists
        self.filtered_lists = []  # Store filtered lists based on search
        self.search_query = ""  # Current search query

        logger.info("Initializing ManageListsView")
        logger.debug("Initializing UI components")
        self._init_components()
        self._load_lists()

    def _init_components(self):
        """Initialize components for List Overview"""
        self.search_field = TextField(
            prefix_icon=ft.icons.SEARCH,
            suffix_icon=ft.icons.CLEAR,
            hint_text="Search lists...",
            on_change=self._handle_search,
            expand=True,
        )

    def build(self):
        """Build the view"""
        logger.debug("Building ManageListsView")

        self.grid_view = GridView(
            expand=True,
            runs_count=3,
            max_extent=350,
            child_aspect_ratio=3.0,
            spacing=10,
            run_spacing=10,
            controls=[self._create_list_item(list_data) for list_data in self.filtered_lists],
        )

        return Column(
            controls=[
                Container(content=Row([self.search_field]), padding=10),
                ft.Divider(height=1, color=ft.colors.OUTLINE),
                Container(
                    content=self.grid_view,
                    padding=10,
                    expand=True,
                ),
            ],
            expand=True,
        )

    def _create_list_item(self, list_data: dict):
        """Create a single list item"""
        try:
            return Container(
                content=Row([
                    Text(list_data["name"], expand=True),
                    IconButton(
                        icon=ft.icons.MODE_EDIT_OUTLINED,
                        tooltip="Edit list",
                        on_click=lambda e, id=list_data["id"]: self._handle_edit_list(id),
                    ),
                    IconButton(
                        icon=ft.icons.DELETE_OUTLINED,
                        tooltip="Delete list",
                        on_click=lambda e, id=list_data["id"]: self._handle_delete_list(id),
                    ),
                ]),
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=8,
                padding=10,
            )
        except Exception as e:
            logger.error(f"Error creating list item: {e}")
            return Container()

    # Event Handlers
    def _handle_search(self, e):
        """Handle search field changes and filter lists"""
        logger.debug(f"Search field changed: {e.control.value}")
        self.search_query = e.control.value
        self.filter_lists(self.search_query)
        self._update_list_grid()

    def _handle_edit_list(self, list_id: str):
        """Handle edit list button click"""
        logger.info(f"Attempting to edit list {list_id}")
        try:
            selected_list = next((lst for lst in self.lists_data if lst["id"] == list_id), None)
            if selected_list:
                # Navigate to EditListView (implementation will be handled by controller)
                self.controller.navigate_to_edit_list(selected_list)
            else:
                logger.warning(f"List {list_id} not found")
                self.page.show_snack_bar(ft.SnackBar(content=Text("List not found!")))
        except Exception as e:
            logger.error(f"Error editing list: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error loading list for editing!")))

    def _handle_delete_list(self, list_id: str):
        """Handle delete list button click"""
        logger.warning(f"Attempting to delete list {list_id}")

        def close_dialog(e):
            logger.debug("Closing delete confirmation dialog")
            dialog.open = False
            self.page.update()

        def confirm_delete(e):
            if self.controller.delete_list(list_id):
                self.lists_data = self.controller.list_controller.get_all_lists()
                self.filter_lists(self.search_query)
                self._update_list_grid()
                self.page.show_snack_bar(ft.SnackBar(content=Text("List deleted successfully!")))
            else:
                self.page.show_snack_bar(ft.SnackBar(content=Text("Error deleting list!")))
            close_dialog(e)

        try:
            list_name = next(lst["name"] for lst in self.lists_data if lst["id"] == list_id)
            dialog = AlertDialog(
                title=Text("Confirm Delete"),
                content=Text(f"Are you sure you want to delete '{list_name}'?"),
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
            self.page.show_snack_bar(ft.SnackBar(content=Text("Error showing delete dialog!")))

    def _load_lists(self):
        """Load lists from controller"""
        self.lists_data = self.controller.list_controller.get_all_lists()
        self.filtered_lists = self.lists_data.copy()
        logger.info(f"Loaded {len(self.lists_data)} lists")

    def filter_lists(self, query: str):
        """Filter lists based on search query"""
        try:
            if not query:
                self.filtered_lists = self.lists_data.copy()
            else:
                query = query.lower()
                self.filtered_lists = [lst for lst in self.lists_data if query in lst["name"].lower()]
            logger.debug(f"Filtered lists to {len(self.filtered_lists)} results")
        except Exception as e:
            logger.error(f"Error filtering lists: {e}")
            self.filtered_lists = []

    def _update_list_grid(self):
        """Update the grid view with filtered lists"""
        try:
            self.grid_view.controls = [self._create_list_item(lst) for lst in self.filtered_lists]
            self.grid_view.update()
            logger.debug(f"Updated grid with {len(self.filtered_lists)} items")
        except Exception as e:
            logger.error(f"Error updating grid: {e}")
