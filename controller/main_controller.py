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

        # Create a single UserAuthentication instance
        self.user_auth = UserAuthentication()

        # Initialize controllers in correct order with proper references
        self.auth = UserAuthenticationController(page, auth=self.user_auth)
        self.list_controller = ListController(self.auth)

        # Update NameGenerationController initialization with list_controller
        self.name_generation = NameGenerationController(list_controller=self.list_controller)
        self.group_formation = GroupFormationController()

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

    def handle_name_generation(
        self,
        names_text: str,
        genders_text: str,
        selected_num: str,
        custom_value: str,
        selected_gender_filter: str,
        male_count: str = "0",
        female_count: str = "0",
    ) -> list[str]:
        """Handle name generation at app level."""
        try:
            return self.name_generation.generate_names(
                names_text, genders_text, selected_num, custom_value, selected_gender_filter, male_count, female_count
            )
        except Exception as e:
            logger.error(f"Error generating names: {e}", exc_info=True)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Error generating names!")))
            return []

    def validate_input(
        self,
        names_text: str,
        selected_num: str,
        custom_value: str,
        selected_gender_filter: str = "none",
        male_count: str = "0",
        female_count: str = "0",
    ) -> bool:
        """Validate name generation input at app level."""
        try:
            return self.name_generation.validate_input(
                names_text, selected_num, custom_value, selected_gender_filter, male_count, female_count
            )
        except Exception as e:
            logger.error(f"Error validating input: {e}", exc_info=True)
            return False

    def handle_list_update(self, list_data: ListModel) -> None:
        """Handle list updates and notify relevant controllers."""
        try:
            # Update list controller
            self.list_controller.update_list(list_data)

            # Notify name generation controller if needed
            if hasattr(self.name_generation, "on_list_update"):
                self.name_generation.on_list_update(list_data)

            logger.info(f"List updated successfully: {list_data.name}")
        except Exception as e:
            logger.error(f"Error updating list: {e}", exc_info=True)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Error updating list!")))

    def update_selected_num(self, selected_num: str, custom_value: str) -> tuple[bool, str]:
        """Delegate to name generation controller."""
        return self.name_generation.update_selected_num(selected_num, custom_value)

    def update_gender_filter(self, filter_type: str) -> dict[str, bool]:
        """Delegate to name generation controller."""
        return self.name_generation.update_gender_filter(filter_type)

    def format_output_label(self, names: list[str]) -> str:
        """Delegate to name generation controller."""
        return self.name_generation.format_output_label(names)

    def handle_clipboard_copy(self, text: str) -> bool:
        """Delegate to name generation controller."""
        return self.name_generation.handle_clipboard_copy(text)

    def handle_input_change(self, names: str, group_size: str, group_num: str) -> tuple[int, int] | tuple[None, None]:
        """Delegate input change handling to group formation controller"""
        try:
            return self.group_formation.handle_input_change(names, group_size, group_num)
        except Exception as e:
            logger.error(f"Error handling input change: {e}")
            return None, None

    def form_groups(self, names: list[str], **kwargs) -> list[list[str]]:
        """Delegate group formation to group formation controller."""
        try:
            return self.group_formation.form_groups(names, **kwargs)
        except Exception as e:
            logger.error(f"Error forming groups: {e}", exc_info=True)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Error forming groups!")))
            return []
