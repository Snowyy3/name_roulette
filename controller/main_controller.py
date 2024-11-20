import flet as ft
from model.user_authentication import UserAuthentication
from model.list_model import ListModel
from controller.user_authentication_controller import UserAuthenticationController
from controller.name_generation_controller import NameGenerationController
from controller.group_former_controller import GroupFormationController
from controller.list_controller import ListController
from ui.views import View
import logging

logger = logging.getLogger(__name__)


class MainController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = None

        self.name_generation = NameGenerationController()
        self.group_formation = GroupFormationController()

        # Create a single UserAuthentication instance
        self.user_auth = UserAuthentication()

        # Initialize controllers in correct order with proper references
        self.auth = UserAuthenticationController(page, auth=self.user_auth)
        self.list_controller = ListController(self.auth)
        self.auth.set_list_controller(self.list_controller)

    def set_main_view(self, view):
        """Set reference to MainView for navigation"""
        self.view = view

    def navigate_to_manage_lists(self):
        """Navigate to manage lists view"""
        if self.view:
            # Import here to avoid circular imports
            from ui.manage_lists_view import ManageListsView

            # Create fresh instance of ManageListsView
            manage_lists_view = ManageListsView(self.page, self)
            self.view.handle_view_change(View.MANAGE_LISTS, manage_lists_view)

    def navigate_to_edit_list(self, list_data: ListModel | dict):
        """Navigate to edit list view"""
        try:
            logger.debug(f"Navigating to edit list with data type: {type(list_data)}")
            # Ensure we have a ListModel
            if isinstance(list_data, dict):
                list_model = ListModel(list_data)
            else:
                list_model = list_data

            logger.debug(f"List model created with name: {list_model.name}")

            if self.view:
                # Set the selected list before navigation
                self.list_controller.set_selected_list(list_model)

                from ui.edit_list_view import EditListView

                edit_view = EditListView(self.page, self, list_model)
                self.view.handle_view_change(View.EDIT_LIST, edit_view)

        except Exception as e:
            logger.error(f"Error navigating to edit list: {e}", exc_info=True)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Error loading list for editing!")))

    def save_list(self, list_data: dict) -> bool:
        """Save list using list controller"""
        return self.list_controller.save_list(list_data)

    def delete_list(self, list_id: str) -> bool:
        """Delete list using list controller"""
        return self.list_controller.delete_list(list_id)

    def set_active_list(self, list_data: ListModel | dict):
        """Set active list and update relevant views"""
        self.list_controller.set_active_list(list_data)

    def navigate_to_name_picker(self):
        """Navigate to name picker view"""
        logger.info("Navigating to name picker")
        if hasattr(self, "view"):
            self.view.navigate_to_name_picker()
        else:
            logger.error("No view found in controller")

    def navigate_to_group_former(self):
        """Navigate to group former view"""
        logger.info("Navigating to group former")
        if hasattr(self, "view"):
            self.view.navigate_to_group_former()
        else:
            logger.error("No view found in controller")
