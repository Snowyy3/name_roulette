import json
import uuid
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ListController:
    def __init__(self, auth_controller=None):
        self.auth = auth_controller
        self.selected_list: Optional[Dict] = None
        self.lists: List[Dict] = []
        logger.info("Initializing ListController")
        self._load_lists()

    def _get_current_username(self) -> str:
        """Get current username or 'guest' if not logged in"""
        if self.auth and self.auth.current_user:
            return self.auth.current_user["username"]
        return "guest"

    def _load_lists(self) -> None:
        """Load lists for current user from saved_lists.json"""
        try:
            with open("assets/saved_lists.json", "r") as file:
                data = json.load(file)

            username = self._get_current_username()
            if username == "guest":
                user_lists = data.get("guest", {}).get("lists", {})
            else:
                user_lists = data.get("users", {}).get(username, {}).get("lists", {})

            # Convert from dict to list format and ensure all required fields
            self.lists = []
            for list_id, list_data in user_lists.items():
                self.lists.append({
                    "id": list_id,
                    "name": list_data.get("name", "Untitled"),
                    "items": list_data.get("items", []),
                })

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
        with open("assets/saved_lists.json", "w") as file:
            json.dump(initial_data, file, indent=4)
        self.lists = []

    def save_list(self, list_data: Dict) -> bool:
        """Save changes to a list"""
        try:
            username = self._get_current_username()
            logger.info(f"Saving list for user {username}: {list_data['name']}")

            # Ensure list has an ID
            if "id" not in list_data:
                list_data["id"] = str(uuid.uuid4())

            # Update in-memory list
            list_index = next((i for i, lst in enumerate(self.lists) if lst["id"] == list_data["id"]), -1)
            if list_index >= 0:
                self.lists[list_index] = list_data
            else:
                self.lists.append(list_data)

            # Save to file
            with open("assets/saved_lists.json", "r+") as file:
                data = json.load(file)

                # Get correct section based on user type
                if username == "guest":
                    user_section = data.setdefault("guest", {"lists": {}})
                else:
                    user_section = data.setdefault("users", {}).setdefault(username, {"lists": {}})

                # Update list in file
                user_section["lists"][list_data["id"]] = {"name": list_data["name"], "items": list_data["items"]}

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            logger.info(f"Successfully saved list {list_data['id']}")
            return True

        except Exception as e:
            logger.error(f"Failed to save list: {e}", exc_info=True)
            return False

    def delete_list(self, list_id: str) -> bool:
        """Delete a list by ID"""
        try:
            username = self._get_current_username()
            logger.warning(f"Deleting list {list_id} for user {username}")

            # Remove from memory
            self.lists = [lst for lst in self.lists if lst["id"] != list_id]

            # Remove from file
            with open("assets/saved_lists.json", "r+") as file:
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

    def get_list(self, list_id: str) -> Optional[Dict]:
        """Get a list by ID"""
        return next((lst for lst in self.lists if lst["id"] == list_id), None)

    def get_all_lists(self) -> List[Dict]:
        """Get all lists"""
        return self.lists

    def set_active_list(self, list_data: Dict) -> None:
        """Set the currently selected list and notify dependent views"""
        self.selected_list = list_data
        # Signal views to update
        if hasattr(self, "name_generation_view"):
            self.name_generation_view.load_active_list()
        if hasattr(self, "group_former_view"):
            self.group_former_view.load_active_list()

    def set_selected_list(self, list_data: Dict) -> None:
        """Set the currently selected list"""
        self.selected_list = list_data

    def get_selected_list(self) -> Optional[Dict]:
        """Get the currently selected list"""
        return self.selected_list

    def handle_user_change(self):
        """Handle user change and reload lists"""
        self._load_lists()
