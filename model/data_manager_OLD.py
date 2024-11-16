import json
import os
from datetime import datetime
from .user_authentication import UserAuthentication


class DataManager:
    def __init__(self, file_path=r"name_roulette/data/user.json"):
        """
        Initialize the DataManager with a file path for storing data.
        """
        self.file_path = file_path
        self.user_auth = UserAuthentication()

        # Ensure self.data is always initialized
        self.data = self.load_data()

    def load_data(self):
        """
        Load data from the JSON file.
        """
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} not found. Creating a new file.")
            return {}  # Return an empty dict if file doesn't exist

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file {self.file_path}. Creating a new file.")
            return {}  # Return an empty dict on JSON errors
        except IOError as e:
            print(f"Error reading file {self.file_path}: {e}")
            return {}  # Return an empty dict on IO errors

    def save_data(self):
        """
        Save the current data to the JSON file.
        """
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def create_list(self, list_name, records, required_fields=["name"], optional_fields=[]):
        """
        Create a new list of records with validation.
        """
        self._validate_records(records, required_fields, optional_fields)
        self.data[list_name] = records
        self.save_data()

    def save_group_formation(self, group_name: str, groups: list[list[str]]):
        """
        Save the group formation results to the user.json file.

        Args:
            group_name (str): Name of the group formation event.
            groups (list[list[str]]): The group formation results from GroupFormer.
        """
        if "group_formations" not in self.data:
            self.data["group_formations"] = {}

        # Count existing results to determine the next 'Result #'
        current_result_count = len(self.data["group_formations"])
        result_key = f"Result #{current_result_count + 1}"

        # Save the new group formation with the new result key
        self.data["group_formations"][result_key] = groups
        self.save_data()

        print(f"Group formation saved successfully as '{result_key}'!")

    def edit_list(self, list_name, new_records, required_fields=["name"], optional_fields=[]):
        """
        Edit an existing list of records.
        """
        if list_name not in self.data:
            raise KeyError(f"List '{list_name}' does not exist.")

        self._validate_records(new_records, required_fields, optional_fields)
        self.data[list_name] = new_records
        self.save_data()

    def delete_list(self, list_name):
        """
        Delete a list from the data.
        """
        if list_name in self.data:
            del self.data[list_name]
            self.save_data()

    def _validate_records(self, records, required_fields, optional_fields):
        """
        Validate that records contain required fields and proper formats.
        """
        if not isinstance(records, list):
            raise ValueError("Records should be a list of dictionaries.")

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each record must be a dictionary.")

            # Check for required fields
            for field in required_fields:
                if field not in record or not record[field]:
                    raise ValueError(f"'{field}' is a required field and must be present in each record.")

            # Validate birthday format
            if "birthday" in record:
                try:
                    datetime.strptime(record["birthday"], "%d/%m/%Y")
                except ValueError:
                    raise ValueError("Birthday must be in 'DD/MM/YYYY' format.")

            # Validate GPA (as float between 0 and 4.0)
            if "gpa" in record and not (0 <= float(record["gpa"]) <= 4.0):
                raise ValueError("GPA must be between 0 and 4.0.")

    # Example usage of UserAuthentication
    def register_user(self, username, display_name, password):
        """
        Register a new user.
        """
        try:
            self.user_auth.add_user(username, display_name, password)
            print("User registered successfully.")
        except ValueError as e:
            print(e)

    def authenticate_user(self, username, password):
        """
        Authenticate a user.
        """
        if self.user_auth.verify_password(username, password):
            print("Authentication successful.")
            return True
        else:
            print("Authentication failed.")
            return False


if __name__ == "__main__":
    data_manager = DataManager()

    # Example group formation result
    groups = [["Alice", "Bob"], ["Charlie", "David"]]

    # Save the group formation result
    data_manager.save_group_formation(" ", groups)
