import random as rd


class NameGenerator:
    """A class to handle name generation and validation logic.

    This class provides functionality for validating inputs, cleaning name lists,
    and generating random unique names from a given list.

    Attributes:
        selected_num (str): The currently selected number of names to generate.
    """

    def __init__(self):
        """Initialize the NameGenerator with default selection of '1'."""
        self.selected_num = "1"

    def validate_input(self, names: list[str], selected_num: str, custom_value: str = "") -> bool:
        """Validate if the current configuration allows for name generation.

        Args:
            names (list[str]): List of names to validate.
            selected_num (str): The selected number option ('1', '2', '3', or 'custom').
            custom_value (str, optional): Custom number input when selected_num is 'custom'.
                Defaults to empty string.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        # Check for empty name list
        if not names:
            return False

        # Get the number of names to generate
        num_names = self.get_num_names(selected_num, custom_value)

        # Validate based on selection type
        if selected_num == "custom":
            return num_names > 0 and num_names <= len(names)
        return int(selected_num) <= len(names)

    def get_num_names(self, selected_num: str, custom_value: str = "") -> int:
        """Convert the selected number option to an integer value.

        Args:
            selected_num (str): The selected number option ('1', '2', '3', or 'custom').
            custom_value (str, optional): Custom number input when selected_num is 'custom'.
                Defaults to empty string.

        Returns:
            int: The number of names to generate. Returns 0 if invalid.
        """
        try:
            if selected_num == "custom":
                value = custom_value.strip()
                return int(value) if value else 0
            return int(selected_num)
        except ValueError:
            return 0

    def get_cleaned_names(self, input_text: str) -> list[str]:
        """Clean and validate the input names text.

        Processes raw input text by splitting into lines, removing whitespace,
        and filtering out empty lines.

        Args:
            input_text (str): Raw input text containing names, one per line.

        Returns:
            list[str]: List of cleaned, non-empty names.
        """
        return [name.strip() for name in input_text.splitlines() if name.strip()]

    def generate_names(self, names: list[str], num_names: int) -> list[str]:
        """Generate random unique names from the input list.

        Args:
            names (list[str]): Pool of names to select from.
            num_names (int): Number of unique names to generate.

        Returns:
            list[str]: List of randomly selected unique names. Returns empty list
                if inputs are invalid.
        """
        # Validate inputs before generation
        if not names or num_names <= 0 or num_names > len(names):
            return []
        # Use random.sample to get unique selections
        return rd.sample(names, num_names)

    def process_name_generation(self, input_text: str, selected_num: str, custom_value: str = "") -> list[str]:
        """Processes the name generation request in one go.

        Args:
            input_text (str): Raw input text containing names
            selected_num (str): Selected number option
            custom_value (str): Custom number input value

        Returns:
            list[str]: Generated names list
        """
        names = self.get_cleaned_names(input_text)
        num_names = self.get_num_names(selected_num, custom_value)
        return self.generate_names(names, num_names)
