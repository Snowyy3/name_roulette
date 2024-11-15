import random as rd


class GroupFormer:
    def __init__(self):
        pass

    def group_formation(self, names: list[str], group_size: int = None, num_groups: int = None):
        """
        Divides a list of names into groups based on either group size or the number of groups.

        Args:
            names (list[str]): A list of names to be divided into groups.
            group_size (int, optional): The desired number of people per group. Defaults to None.
            num_groups (int, optional): The desired number of groups. Defaults to None.

        Raises:
            ValueError: If neither 'group_size' nor 'num_groups' is provided.
            TypeError: If 'group_size' or 'num_groups' is not an integer.
            ValueError: If 'group_size' or 'num_groups' is negative or zero.

        Returns:
            list[list[str]]: A list of groups.
        """
        if not names:
            return []

        if group_size is None and num_groups is None:
            raise ValueError("Either 'group_size' or 'num_groups' must be provided.")

        # Validate input types
        if group_size is not None and not isinstance(group_size, int):
            raise TypeError("'group_size' must be an integer.")
        if num_groups is not None and not isinstance(num_groups, int):
            raise TypeError("'num_groups' must be an integer.")

        # Validate input values
        if group_size is not None and group_size <= 0:
            raise ValueError("'group_size' must be a positive integer.")
        if num_groups is not None and num_groups <= 0:
            raise ValueError("'num_groups' must be a positive integer.")

        rd.shuffle(names)  # Shuffle names to randomize grouping

        # Điều chỉnh lại số lượng nhóm và kích thước nhóm
        if num_groups is None:
            # Tính số lượng nhóm khi chỉ định 'group_size'
            num_groups = (len(names) + group_size - 1) // group_size  # Làm tròn lên
        else:
            # Tính kích thước nhóm khi chỉ định 'num_groups'
            group_size = (len(names) + num_groups - 1) // num_groups  # Làm tròn lên

        # Khởi tạo các nhóm
        groups = [[] for _ in range(num_groups)]

        # Phân bổ các thành viên vào nhóm
        index = 0
        for name in names:
            groups[index].append(name)
            index = (index + 1) % num_groups

        # Điều chỉnh nếu có nhóm nào vượt quá `Max Group Size`
        for i in range(num_groups):
            while len(groups[i]) > group_size:
                for j in range(num_groups):
                    if len(groups[j]) < group_size:
                        groups[j].append(groups[i].pop())
                        break

        # Lọc các nhóm rỗng nếu có
        groups = [g for g in groups if g]

        return groups

    def handle_uneven_groups(
        self, groups: list[list[str]], remaining_members: list[str], distribute_randomly: bool = True
    ) -> list[list[str]]:
        """
        Handles uneven group sizes by either creating a separate remainder list or distributing remaining members randomly.

        Args:
            groups (list[list[str]]): The list of groups created by 'group_formation'.
            remaining_members (list[str]): The list of remaining members.
            distribute_randomly (bool, optional): If True, remaining members are distributed randomly among the groups.
                                                If False, remaining members are returned as a separate list. Defaults to True.

        Returns:
            list[list[str]]: The list of groups after handling uneven group sizes.
        """
        if distribute_randomly:
            for member in remaining_members:
                rd.choice(groups).append(member)
        else:
            groups.append(remaining_members)

        return groups

    def get_cleaned_names(self, names_text: str, genders_text: str) -> list[tuple[str, str]]:
        """Clean and parse the input names and genders text with corresponding lines.

        Args:
            names_text (str): Raw input text containing names, one per line.
            genders_text (str): Raw input text containing genders, one per line.

        Returns:
            list[tuple[str, str]]: List of tuples where each tuple is (name, gender).
        """
        names = names_text.strip().splitlines()
        genders = genders_text.strip().splitlines()

        # Combine names and genders based on line-by-line pairing
        cleaned_names = []
        for name, gender in zip(names, genders):
            name = name.strip()
            gender = gender.strip().lower()
            if name and gender in {"male", "female"}:
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
    
    def generate_names_with_gender(self, names: list[tuple[str, str]], male_count: int, female_count: int,group_size: int = None, num_groups: int = None) -> list[str]:
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

        if not names:
            return []
        
        
        if group_size is None and num_groups is None:
            raise ValueError("Either 'group_size' or 'num_groups' must be provided.")

        # Validate input types
        if group_size is not None and not isinstance(group_size, int):
            raise TypeError("'group_size' must be an integer.")
        if num_groups is not None and not isinstance(num_groups, int):
            raise TypeError("'num_groups' must be an integer.")
    
        # Validate input values
        if group_size is not None and group_size <= 0:
            raise ValueError("'group_size' must be a positive integer.")
        if num_groups is not None and num_groups <= 0:
            raise ValueError("'num_groups' must be a positive integer.")
        

        # Separate names by gender
        rd.shuffle(names)
        gendered_names = self.separate_by_gender(names)
        males, females = gendered_names["male"], gendered_names["female"]


        # Adjust `num_groups` and `group_size` based on input
        if num_groups is None:
            num_groups = (len(names) + group_size - 1) // group_size  # Round up if only `group_size` is provided
        else:
            group_size = (len(names) + num_groups - 1) // num_groups  # Round up if only `num_groups` is provided


        # Initialize groups
        groups = [[] for _ in range(num_groups)]
        for i in range(num_groups):
            # Select males and females for this group
            group_males = rd.sample(males, male_count)
            group_females = rd.sample(females, female_count)
            
            # Add selected names to the group and remove them from the pools
            groups[i].extend(group_males + group_females)
            males = [m for m in males if m not in group_males]
            females = [f for f in females if f not in group_females]

        # Assign remaining names while respecting `max_group_size`
        remaining_names = males + females
        index = 0
        for name in remaining_names:
            if len(groups[index]) < group_size:
                groups[index].append(name)
            else:
                # Find a group with space if the current group is full
                for j in range(num_groups):
                    if len(groups[j]) < group_size:
                        groups[j].append(name)
                        break
            index = (index + 1) % num_groups

        # Filter out any empty groups
        groups = [g for g in groups if g]
        
        return groups
    def manual_assignment(self, groups: list[list[str]], assignments: dict[int, list[str]]) -> list[list[str]]:
        """
        Manually assigns specific members to specific groups.

        Args:
            groups (list[list[str]]): The list of groups created by 'group_formation'.
            assignments (dict[int, list[str]]): A dictionary where keys are group indices (starting from 1) and
                                                values are lists of names to be assigned to that group.

        Returns:
            list[list[str]]: The list of groups after manual assignment.
        """
        for i, names in assignments.items():
            group_index = i - 1
            if group_index < 0 or group_index >= len(groups):
                raise ValueError(f"Invalid group index: {i}. Group indices must be between 1 and {len(groups)}.")
            if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
                raise TypeError("Values in 'assignments' must be lists of strings.")

            groups[group_index].extend(names)

        return groups
