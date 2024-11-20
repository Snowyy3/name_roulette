from typing import Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class ListModel:
    def __init__(self, list_data: Optional[Dict] = None):
        if list_data is None:
            list_data = {}
        self.id: str = list_data.get("id", str(uuid.uuid4()))
        self.name: str = list_data.get("name", "Untitled")
        self.items: List[Dict] = list_data.get("items", [])

    def to_dict(self) -> Dict:
        """Convert model to dictionary format"""
        return {"id": self.id, "name": self.name, "items": self.items}

    def from_dict(self, data: Dict) -> None:
        """Update model from dictionary data"""
        self.id = data.get("id", self.id)
        self.name = data.get("name", self.name)
        self.items = data.get("items", self.items)

    # Item management methods
    def add_item(self, name: str, gender: Optional[str] = None) -> Dict:
        """Add a new item to the list"""
        item = {
            "id": str(uuid.uuid4()),
            "name": name.strip() if name else "",
        }
        if gender and gender.strip():
            item["gender"] = gender.strip()
        self.items.append(item)
        return item

    def update_item(self, item_id: str, name: str, gender: Optional[str] = None) -> bool:
        """Update an existing item with validation"""
        for item in self.items:
            if item.get("id") == item_id:  # Use get() for safety
                item["name"] = name.strip() if name else ""
                if gender and gender.strip():
                    item["gender"] = gender.strip()
                elif "gender" in item:
                    del item["gender"]
                return True
        return False

    def delete_item(self, item_id: str) -> bool:
        """Delete an item from the list"""
        initial_length = len(self.items)
        self.items = [item for item in self.items if item["id"] != item_id]
        return len(self.items) < initial_length

    def filter_items(self, query: str) -> List[Dict]:
        """Filter items based on search query"""
        query = query.lower()
        return [item for item in self.items if query in item["name"].lower()]

    def equals(self, other: "ListModel") -> bool:
        """Compare this list with another list"""
        return (
            self.name == other.name
            and len(self.items) == len(other.items)
            and all(i1 == i2 for i1, i2 in zip(self.items, other.items))
        )

    def validate_name(self, name: str) -> tuple[bool, str]:
        """Validate list name"""
        name = name.strip()
        if not name:
            return False, "Name cannot be empty"
        if len(name) > 200:
            return False, "Name is too long (max 200 characters)"
        return True, ""

    def validate_item(self, name: str) -> tuple[bool, str]:
        """Validate item data"""
        name = name.strip()
        if not name:
            return False, "Name cannot be empty"
        if len(name) > 100:
            return False, "Name is too long (max 100 characters)"
        return True, ""

    def validate(self) -> tuple[bool, str]:
        """Validate entire list"""
        is_valid, error = self.validate_name(self.name)
        if not is_valid:
            return False, error

        for item in self.items:
            is_valid, error = self.validate_item(item["name"])
            if not is_valid:
                return False, f"Item '{item['name']}': {error}"

        return True, ""
