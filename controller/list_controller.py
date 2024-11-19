import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ListController:
    def __init__(self):
        logger.info("Initializing ListController")
        self.selected_list: Optional[Dict] = None
        self.lists: List[Dict] = []
        self._load_lists()

    def _load_lists(self) -> None:
        """Load lists from saved_lists.json"""
        try:
            with open("data/saved_lists.json", "r") as file:
                data = json.load(file)
            user1_data = next((user for user in data["users"] if user["user_id"] == "user1"), None)
            if user1_data:
                self.lists = [
                    {"id": lst["list_id"], "name": lst["list_name"], "items": lst["members"]}
                    for lst in user1_data["lists"]
                ]
                logger.info(f"Successfully loaded {len(self.lists)} lists")
            else:
                logger.warning("User1 not found in saved_lists.json")
                self.lists = []
        except Exception as e:
            logger.error(f"Error loading lists: {e}")
            self.lists = []

    def save_list(self, list_data: Dict) -> bool:
        """Save changes to a list"""
        try:
            logger.info(f"Saving list: {list_data['id']} ({list_data['name']})")
            # Update list in memory
            list_index = next((i for i, lst in enumerate(self.lists) if lst["id"] == list_data["id"]), -1)
            if list_index >= 0:
                self.lists[list_index] = list_data
            else:
                self.lists.append(list_data)

            # Save to file
            with open("data/saved_lists.json", "r+") as file:
                data = json.load(file)
                user1_data = next(user for user in data["users"] if user["user_id"] == "user1")
                user1_lists = user1_data["lists"]

                # Update or add list
                list_index = next((i for i, lst in enumerate(user1_lists) if lst["list_id"] == list_data["id"]), -1)
                list_to_save = {
                    "list_id": list_data["id"],
                    "list_name": list_data["name"],
                    "members": list_data["items"],
                }

                if list_index >= 0:
                    user1_lists[list_index] = list_to_save
                else:
                    user1_lists.append(list_to_save)

                # Save back to file
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            logger.info(f"Successfully saved list {list_data['id']}")
            return True
        except Exception as e:
            logger.error(f"Failed to save list {list_data.get('id', 'unknown')}: {str(e)}", exc_info=True)
            return False

    def delete_list(self, list_id: str) -> bool:
        """Delete a list by ID"""
        try:
            logger.warning(f"Deleting list: {list_id}")
            # Remove from memory
            self.lists = [lst for lst in self.lists if lst["id"] != list_id]

            # Remove from file
            with open("data/saved_lists.json", "r+") as file:
                data = json.load(file)
                user1_data = next(user for user in data["users"] if user["user_id"] == "user1")
                user1_data["lists"] = [lst for lst in user1_data["lists"] if lst["list_id"] != list_id]

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

            logger.info(f"Successfully deleted list {list_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete list {list_id}: {str(e)}", exc_info=True)
            return False

    def get_list(self, list_id: str) -> Optional[Dict]:
        """Get a list by ID"""
        return next((lst for lst in self.lists if lst["id"] == list_id), None)

    def get_all_lists(self) -> List[Dict]:
        """Get all lists"""
        return self.lists

    def set_selected_list(self, list_data: Dict) -> None:
        """Set the currently selected list"""
        self.selected_list = list_data

    def get_selected_list(self) -> Optional[Dict]:
        """Get the currently selected list"""
        return self.selected_list
