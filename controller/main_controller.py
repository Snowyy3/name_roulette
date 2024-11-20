import flet as ft
from model.user_authentication import UserAuthentication
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

        self.name_generation = NameGenerationController()
        self.group_formation = GroupFormationController()

        # Create a single UserAuthentication instance
        # Since if not, 2 instances = change password/forgot password are out of sync and won't work
        self.user_auth = UserAuthentication()

        # Initialize controllers with shared UserAuthentication instance
        self.auth = UserAuthenticationController(page, auth=self.user_auth)

        self.list_controller = ListController(self.auth)
        self.view = None  # Store reference to MainView

    def set_main_view(self, view):
        """Set reference to MainView for navigation"""
        self.view = view

    def navigate_to_manage_lists(self):
        """Navigate to manage lists view"""
        if self.view:
            self.view.handle_view_change(View.MANAGE_LISTS)

    def navigate_to_edit_list(self, list_data: dict):
        """Navigate to edit list view with selected list"""
        try:
            if self.view:
                # Set the selected list before navigation
                self.list_controller.set_selected_list(list_data)
                # Import here to avoid circular imports
                from ui.edit_list_view import EditListView

                # Create the edit view first
                edit_view = EditListView(self.page, self, list_data)
                # Then handle navigation
                self.view.handle_view_change(View.EDIT_LIST, edit_view)
        except Exception as e:
            logger.error(f"Error navigating to edit list: {e}")
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Error loading list for editing!")))

    def save_list(self, list_data: dict) -> bool:
        """Save list using list controller"""
        return self.list_controller.save_list(list_data)

    def delete_list(self, list_id: str) -> bool:
        """Delete list using list controller"""
        return self.list_controller.delete_list(list_id)

    def set_active_list(self, list_data: dict) -> None:
        """Set active list and update relevant views"""
        self.list_controller.set_active_list(list_data)

    def navigate_to_name_picker(self):
        """Navigate to name picker view with active list"""
        # Signal view change
        if hasattr(self, "view"):
            self.view.handle_view_change(View.NAME_PICKER)

    def navigate_to_group_former(self):
        """Navigate to group former view with active list"""
        if hasattr(self, "view"):
            self.view.handle_view_change(View.GROUP_FORMER)
