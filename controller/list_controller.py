import json
import logging
from typing import Dict, List, Optional
import uuid
from model.list_model import ListModel

logger = logging.getLogger(__name__)


class ListController:
    def __init__(self, auth_controller=None):
        self.auth = auth_controller
        self.selected_list: Optional[ListModel] = None
        self.lists: List[ListModel] = []
        logger.info("Initializing ListController")
        self._load_lists()

    def handle_user_change(self):
        """Refresh lists when user changes"""
        logger.info("Refreshing lists due to user change")
        self.selected_list = None  # Clear selected list
        self._load_lists()  # Reload lists for new user

    def _get_current_username(self) -> str:
        """Get current username or 'guest' if not logged in"""
        if self.auth and self.auth.current_user:
            return self.auth.current_user["username"]
        return "guest"

    def _load_lists(self) -> None:
        """Load lists for current user from saved_lists.json"""
        try:
            with open("data/saved_lists.json", "r") as file:
                data = json.load(file)

            username = self._get_current_username()
            self.lists = []

            user_lists = (
                data.get("users", {}).get(username, {}).get("lists", {})
                if username != "guest"
                else data.get("guest", {}).get("lists", {})
            )

            # Convert from dict to ListModel
            for list_id, list_data in user_lists.items():
                list_data["id"] = list_id
                self.lists.append(ListModel(list_data))

            logger.info(f"Loaded {len(self.lists)} lists for user {username}")

        except FileNotFoundError:
            logger.warning("saved_lists.json not found, creating new file")
            self._create_initial_file()
        except Exception as e:
            logger.error(f"Error loading lists: {e}")
            self.lists = []

    def _create_initial_file(self):
        """Create initial saved_lists.json structure"""
        initial_data = {"users": {}, "guest": {"lists": {}}}
        with open("data/saved_lists.json", "w") as file:
            json.dump(initial_data, file, indent=4)
        self.lists = []

    def save_list(self, list_data: Dict | ListModel) -> bool:
        """Save changes to a list"""
        try:
            username = self._get_current_username()

            # Convert to ListModel if necessary
            list_model = list_data if isinstance(list_data, ListModel) else ListModel(list_data)

            # Update in-memory list
            list_index = next((i for i, lst in enumerate(self.lists) if lst.id == list_model.id), -1)
            if list_index >= 0:
                self.lists[list_index] = list_model
            else:
                self.lists.append(list_model)

            # Save to file
            self._save_lists_to_file(username)

            logger.info(f"Successfully saved list {list_model.id}")
            return True

        except Exception as e:
            logger.error(f"Failed to save list: {e}", exc_info=True)
            return False

    def _save_lists_to_file(self, username: str) -> None:
        """Save all lists to file for given username"""
        try:
            with open("data/saved_lists.json", "r+") as file:
                data = json.load(file)
                
                # Get correct section based on user type
                if username == "guest":
                    user_section = data.setdefault("guest", {"lists": {}})
                else:
                    user_section = data.setdefault("users", {}).setdefault(username, {"lists": {}})

                # Convert all lists to dict format safely
                user_section["lists"] = {
                    lst.id: {
                        "name": lst.name,
                        "items": [
                            {
                                "id": item.get("id", str(uuid.uuid4())),
                                "name": item.get("name", ""),
                                **({"gender": item["gender"]} if item.get("gender") else {})
                            }
                            for item in lst.items
                        ]
                    }
                    for lst in self.lists
                }

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

        except Exception as e:
            logger.error(f"Error saving lists to file: {e}")
            raise

    def delete_list(self, list_id: str) -> bool:
        """Delete a list by ID"""
        try:
            username = self._get_current_username()
            logger.warning(f"Deleting list {list_id} for user {username}")

            # Remove from memory
            self.lists = [lst for lst in self.lists if lst.id != list_id]

            # Remove from file
            with open("data/saved_lists.json", "r+") as file:
                data = json.load(file)

                if username == "guest":
                    user_section = data.get("guest", {}).get("lists", {})
                else:
                    user_section = data.get("users", {}).get(username, {}).get("lists", {})

                if list_id in user_section:
                    del user_section[list_id]

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            logger.info(f"Successfully deleted list {list_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete list {list_id}: {e}", exc_info=True)
            return False

    def get_list(self, list_id: str) -> Optional[ListModel]:
        """Get a list by ID"""
        return next((lst for lst in self.lists if lst.id == list_id), None)

    def get_all_lists(self) -> List[ListModel]:
        """Get all lists"""
        return self.lists

    def set_active_list(self, list_data: Dict | ListModel) -> None:
        """Set the currently selected list and notify dependent views"""
        self.selected_list = list_data if isinstance(list_data, ListModel) else ListModel(list_data)
        self._notify_views()

    def _notify_views(self) -> None:
        """Notify dependent views of list changes"""
        for view_name in ["name_generation_view", "group_former_view"]:
            if hasattr(self, view_name):
                getattr(self, view_name).load_active_list()

    def set_selected_list(self, list_data: Dict | ListModel) -> None:
        """Set the currently selected list"""
        self.selected_list = list_data if isinstance(list_data, ListModel) else ListModel(list_data)

    def get_selected_list(self) -> Optional[ListModel]:
        """Get the currently selected list"""
        return self.selected_list

    def filter_lists(self, query: str) -> List[ListModel]:
        """Filter lists based on search query"""
        query = query.lower()
        return [lst for lst in self.lists if query in lst.name.lower()]

    def validate_list(self, list_model: ListModel) -> tuple[bool, str]:
        """Validate list data"""
        return list_model.validate()

    def validate_item(self, name: str) -> tuple[bool, str]:
        """Validate item data"""
        temp_model = ListModel()
        return temp_model.validate_item(name)

    def add_item_to_list(
        self, list_model: ListModel, name: str, gender: Optional[str] = None
    ) -> tuple[bool, Dict, str]:
        """Add item to list with validation"""
        try:
            is_valid, error = self.validate_item(name)
            if not is_valid:
                return False, {}, error

            new_item = list_model.add_item(name, gender)
            return True, new_item, ""
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            return False, {}, str(e)

    def update_item_in_list(
        self, list_model: ListModel, item_id: str, name: str, gender: Optional[str] = None
    ) -> tuple[bool, str]:
        """Update item in list with validation"""
        try:
            is_valid, error = self.validate_item(name)
            if not is_valid:
                return False, error

            if list_model.update_item(item_id, name, gender):
                return True, ""
            return False, "Item not found"
        except Exception as e:
            logger.error(f"Error updating item: {e}")
            return False, str(e)

    def delete_item_from_list(self, list_model: ListModel, item_id: str) -> tuple[bool, str]:
        """Delete item from list"""
        try:
            if list_model.delete_item(item_id):
                return True, ""
            return False, "Item not found"
        except Exception as e:
            logger.error(f"Error deleting item: {e}")
            return False, str(e)
