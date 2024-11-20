import random as rd


class NameGenerator:
    """A class to handle name generation and validation logic with gender-specific selection."""

    def __init__(self):
        """Initialize the NameGenerator."""
        self.selected_num = "1"

    def get_cleaned_names(self, names_text: str, genders_text: str) -> list[tuple[str, str]]:
        """Clean and parse the input names and genders text with corresponding lines.

        Args:
            names_text (str): Raw input text containing names, one per line.
            genders_text (str): Raw input text containing genders, one per line.

        Returns:
            list[tuple[str, str]]: List of tuples where each tuple is (name, gender).
        """
        # Map Vietnamese gender terms to English
        gender_map = {"nam": "male", "nữ": "female", "male": "male", "female": "female"}

        names = names_text.strip().splitlines()
        genders = genders_text.strip().splitlines()

        # Combine names and genders based on line-by-line pairing
        cleaned_names = []
        for name, gender in zip(names, genders):
            name = name.strip()
            normalized_gender = gender_map.get(gender.strip().lower(), None)  # Normalize gender
            if name and normalized_gender:
                cleaned_names.append((name, normalized_gender))

        return cleaned_names

    def separate_by_gender(self, names: list[tuple[str, str]]) -> dict[str, list[str]]:
        """Separate names by gender based on parsed tuples.

        Args:
            names (list[tuple[str, str]]): List of tuples containing names with gender.

        Returns:
            dict[str, list[str]]: Dictionary with keys 'male' and 'female', each holding a list of names.
        """
        males = [name for name, gender in names if gender == "male"]
        females = [name for name, gender in names if gender == "female"]
        return {"male": males, "female": females}

    def generate_random_names_without_gender(self, names_text: str, total_count: int) -> list[str]:
        """Generate a list of random names without gender constraints.

        Args:
            names_text (str): Raw input text containing names.
            total_count (int): Total number of names to select.

        Returns:
            list[str]: List of randomly selected names.
        """
        # Split names by line and clean them
        names = [name.strip() for name in names_text.strip().splitlines() if name.strip()]

        # Check if there are enough names to meet the total count
        if total_count > len(names):
            return []  # Not enough names to meet the request

        # Randomly sample the specified number of names
        return rd.sample(names, total_count)

    def generate_names_with_gender(
        self, names: list[tuple[str, str]], male_count: int, female_count: int, total_count: int
    ) -> list[str]:
        """Generate names with exact counts of male and female selections within a total count.

        Args:
            names (list[tuple[str, str]]): Pool of names with gender information.
            male_count (int): Exact number of male names to select.
            female_count (int): Exact number of female names to select.
            total_count (int): Total number of names to select.

        Returns:
            list[str]: List of randomly selected names meeting the exact gender and total requirements,
                    or an empty list if constraints cannot be met.
        """
        # Separate names by gender
        gendered_names = self.separate_by_gender(names)

        # Check if we have enough names for each gender and the total count constraint
        if male_count > len(gendered_names["male"]) or female_count > len(gendered_names["female"]):
            return []  # Not enough names to satisfy the exact counts

        # Select exactly the specified number of male and female names
        selected_males = rd.sample(gendered_names["male"], male_count)
        selected_females = rd.sample(gendered_names["female"], female_count)

        # Combine selected male and female names
        selected_names = selected_males + selected_females

        # Calculate remaining slots for the other gender
        remaining_count = total_count - len(selected_names)

        # Add additional names from the remaining gender pool to fill the total count
        if remaining_count > 0:
            remaining_gender = "female" if male_count > 0 else "male"  # Choose opposite gender
            remaining_pool = [name for name in gendered_names[remaining_gender] if name not in selected_names]

            # Ensure we don't select more names than are available in the pool
            if remaining_count > len(remaining_pool):
                return []  # Not enough names to meet the total request

            selected_names += rd.sample(remaining_pool, remaining_count)

        return selected_names

    def process_name_generation(
        self,
        names_text: str,
        genders_text: str,
        selected_num: str,
        custom_value: str = "",
        male_count: int = 0,
        female_count: int = 0,
    ) -> list[str]:
        """Processes the name generation request with exact gender-specific selection within a total count.

        Args:
            names_text (str): Raw input text containing names.
            genders_text (str): Raw input text containing genders.
            selected_num (str): Selected number option for total count.
            custom_value (str): Custom number input value.
            male_count (int): Exact number of male names.
            female_count (int): Exact number of female names.

        Returns:
            list[str]: Generated names list or an empty list if constraints cannot be met.
        """
        names = self.get_cleaned_names(names_text, genders_text)

        # Determine the total number of names to select
        total_count = self.get_num_names(selected_num, custom_value)

        # Generate names based on the exact male and female counts within the total count
        if male_count > 0 or female_count > 0:
            return self.generate_names_with_gender(names, male_count, female_count, total_count)
        else:
            return self.generate_random_names_without_gender(names_text, total_count)

    def get_num_names(self, selected_num: str, custom_value: str = "") -> int:
        """Convert the selected number option to an integer value."""
        try:
            if selected_num == "custom":
                value = custom_value.strip()
                return int(value) if value else 0
            return int(selected_num)
        except ValueError:
            return 0

    def validate_input(
        self,
        names: list[tuple[str, str]],
        selected_num: str,
        custom_value: str,
        male_count: str = "0",
        female_count: str = "0",
    ) -> bool:
        """Validate the input for name generation.

        Args:
            names: List of (name, gender) tuples
            selected_num: Selected number option ("1", "2", "3", or "custom")
            custom_value: Custom number input value
            male_count: Number of male names to select
            female_count: Number of female names to select

        Returns:
            bool: True if input is valid, False otherwise
        """
        # Validate total number of names to select
        try:
            total_count = self.get_num_names(selected_num, custom_value)
            if total_count <= 0:
                return False

            if not names:  # No names provided
                return False

            # If gender counts specified, validate them
            if male_count != "0" or female_count != "0":
                try:
                    male_count = int(male_count)
                    female_count = int(female_count)

                    # Get available names by gender
                    gendered_names = self.separate_by_gender(names)
                    available_males = len(gendered_names["male"])
                    available_females = len(gendered_names["female"])

                    # Check if we have enough names of each gender
                    if male_count > available_males or female_count > available_females:
                        return False

                    # Check if total gender counts don't exceed total requested
                    if male_count + female_count > total_count:
                        return False

                except ValueError:
                    return False
            else:
                # For non-gender specific validation, just check total available names
                available_names = len(names)
                if total_count > available_names:
                    return False

            return True

        except (ValueError, TypeError):
            return False
