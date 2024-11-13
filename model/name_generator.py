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
        names = names_text.strip().splitlines()
        genders = genders_text.strip().splitlines() if genders_text else [""] * len(names)

        # Combine names and genders based on line-by-line pairing
        cleaned_names = []
        for name, gender in zip(names, genders):
            name = name.strip()
            gender = gender.strip().lower()
            if name:
                cleaned_names.append((name, gender))

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

    def generate_names_with_fixed_gender(self, names: list[tuple[str, str]], male_count: int, female_count: int, total_count: int) -> list[str]:
        """Generate names with specified counts of males and/or females within a total count.

        Args:
            names (list[tuple[str, str]]): Pool of names with gender information.
            male_count (int): Exact number of male names to select.
            female_count (int): Exact number of female names to select.
            total_count (int): Total number of names to select.

        Returns:
            list[str]: List of randomly selected names meeting the gender and total requirements,
                       or an empty list if constraints cannot be met.
        """
        # Separate names by gender
        gendered_names = self.separate_by_gender(names)

        # Check if there are enough names to meet the gender constraints
        if male_count > len(gendered_names["male"]) or female_count > len(gendered_names["female"]):
            return []  # Not enough names to satisfy the gender requirements

        selected_names = []
        remaining_pool = []

        # First, select the specified number of names from the chosen gender
        if male_count > 0:
            rd.shuffle(gendered_names["male"])  # Randomize the male list
            selected_males = gendered_names["male"][:male_count]
            selected_names.extend(selected_males)
            remaining_pool = gendered_names["female"]  # Opposite gender pool for remaining count
        elif female_count > 0:
            rd.shuffle(gendered_names["female"])  # Randomize the female list
            selected_females = gendered_names["female"][:female_count]
            selected_names.extend(selected_females)
            remaining_pool = gendered_names["male"]  # Opposite gender pool for remaining count

        # Calculate the number of names needed to reach total_count
        remaining_count = total_count - len(selected_names)

        # Randomize the opposite gender pool and pick remaining names
        rd.shuffle(remaining_pool)
        if remaining_count > len(remaining_pool):
            return []  # Not enough names left in the opposite gender to satisfy the total count requirement

        selected_names.extend(remaining_pool[:remaining_count])

        return selected_names

    def process_name_generation(self, names_text: str, genders_text: str, selected_num: str, custom_value: str = "", male_count: int = 0, female_count: int = 0) -> list[str]:
        """Processes the name generation request with gender-specific selection within a total count.

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
        # Determine the total number of names to select
        total_count = self.get_num_names(selected_num, custom_value)

        # If no gender constraint is applied, generate names without gender
        if male_count == 0 and female_count == 0:
            return self.generate_random_names_without_gender(names_text, total_count)

        # Otherwise, parse names with genders and apply gender constraints
        names = self.get_cleaned_names(names_text, genders_text)
        return self.generate_names_with_fixed_gender(names, male_count, female_count, total_count)

    def get_num_names(self, selected_num: str, custom_value: str = "") -> int:
        """Convert the selected number option to an integer value."""
        try:
            if selected_num == "custom":
                value = custom_value.strip()
                return int(value) if value else 0
            return int(selected_num)
        except ValueError:
            return 0
