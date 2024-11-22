import random as rd
import copy


class GroupFormer:
    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        """Reset internal state"""
        self.current_groups = []
        self.remaining_names = []

    def validate_input(self, names: list[str], group_size: int = None, num_groups: int = None) -> bool:
        """Validate input parameters"""
        if not names:
            return False

        if group_size is not None and (not isinstance(group_size, int) or group_size <= 0):
            return False

        if num_groups is not None and (not isinstance(num_groups, int) or num_groups <= 0):
            return False

        return True

    def calculate_group_parameters(
        self, total_names: int, group_size: int = None, num_groups: int = None
    ) -> tuple[int, int]:
        """Calculate optimal group size and number of groups"""
        if group_size is None and num_groups is None:
            # Default to roughly square root for both if neither is specified
            num_groups = max(1, int(total_names**0.5))
            group_size = (total_names + num_groups - 1) // num_groups
        elif group_size is not None:
            num_groups = max(1, (total_names + group_size - 1) // group_size)
        else:  # num_groups is not None
            group_size = max(1, (total_names + num_groups - 1) // num_groups)

        return group_size, num_groups

    def group_formation(self, names: list[str], group_size: int = None, num_groups: int = None):
        """
        Divides a list of names into groups based on either group size or the number of groups.
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

        # Cập nhật lại group_size và num_groups dựa trên số lượng tên
        group_size, num_groups = self.update_group_size_on_name_addition(names, group_size, num_groups)

        # Adjust group count and size
        if num_groups is None:
            # Calculate number of groups when only 'group_size' is provided
            num_groups = (len(names) + group_size - 1) // group_size  # Round up
        else:
            # Calculate group size when only 'num_groups' is provided
            group_size = (len(names) + num_groups - 1) // num_groups  # Round up

        # Initialize groups
        groups = [[] for _ in range(num_groups)]

        # Distribute names to groups
        index = 0
        for name in names:
            groups[index].append(name)
            index = (index + 1) % num_groups

        # Adjust if there are any groups exceeding `group_size`
        for i in range(num_groups):
            while len(groups[i]) > group_size:
                for j in range(num_groups):
                    if len(groups[j]) < group_size:
                        groups[j].append(groups[i].pop())
                        break

        # Filter out empty groups
        groups = [g for g in groups if g]
        return groups
        #return {'generated_groups': groups, 'exisiting_groups': None, 'remaining_names': None}

    def update_group_size_on_name_addition(self, names: list[str], group_size: int, num_groups: int):
        """Automatically updates group size based on the number of names and the number of groups."""
        if num_groups is not None:
            # Update group size based on num_groups
            group_size = (len(names) + num_groups - 1) // num_groups
        # elif group_size is not None:
        #     # Update num_groups based on group size
        #     num_groups = (len(names) + group_size - 1) // group_size

        return group_size, num_groups

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
            if name and gender in {"male", "female", "nam", "nữ"}:
                if gender == "nam":
                    gender = "male"
                elif gender == "nữ":
                    gender = "female"
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

    def generate_names_with_gender(self,names: list[tuple[str, str]],male_count: int,female_count: int,group_size: int = None,num_groups: int = None,) -> list[list[str]]:
        """Generate gender-balanced groups with fallback for insufficient members."""
        if not names:
            return []

        # Ensure we have either group_size or num_groups
        if group_size is None and num_groups is None:
            # Default to group size based on total count and gender requirements
            total_per_group = max(male_count + female_count, 1)
            group_size = total_per_group
            num_groups = (len(names) + group_size - 1) // group_size
        elif num_groups is None:
            num_groups = (len(names) + group_size - 1) // group_size
        elif group_size is None:
            group_size = (len(names) + num_groups - 1) // num_groups

        # Separate by gender
        gendered_names = self.separate_by_gender(names)
        males, females = gendered_names["male"], gendered_names["female"]

        # Initialize groups
        groups = [[] for _ in range(num_groups)]

        # Handle insufficient males or females with warnings
        if male_count > 0 and len(males) < male_count * num_groups:
            print(f"Not enough males to meet requirement of {male_count} per group. Proceeding with available males.")
        if female_count > 0 and len(females) < female_count * num_groups:
            print(f"Not enough females to meet requirement of {female_count} per group. Proceeding with available females.")

        # Distribute required males first
        if male_count > 0:
            for i in range(num_groups):
                if males:  # Only distribute if there are remaining males
                    group_males = rd.sample(males, min(male_count, len(males)))
                    groups[i].extend((name, "male") for name in group_males)
                    for name in group_males:
                        males.remove(name)

        # Then distribute required females
        if female_count > 0:
            for i in range(num_groups):
                if females:  # Only distribute if there are remaining females
                    group_females = rd.sample(females, min(female_count, len(females)))
                    groups[i].extend((name, "female") for name in group_females)
                    for name in group_females:
                        females.remove(name)

        # Distribute remaining members evenly (any gender)
        remaining = [(name, "male") for name in males] + [(name, "female") for name in females]
        rd.shuffle(remaining)

        # Add remaining members to groups
        i = 0
        while remaining and any(len(group) < group_size for group in groups):
            if len(groups[i]) < group_size:
                groups[i].append(remaining.pop())
            i = (i + 1) % num_groups

        # Ensure no group is empty
        for group in groups:
            if not group and remaining:
                group.append(remaining.pop())

        # Format groups to return only names
        return [[name for name, _ in group] for group in groups if group]


    def counting_name(self, names_only: list[str]) -> dict[str, int]:
        """
        Count occurrences of each name in the input list.

        Args:
            names_only (list[str]): List of names to count

        Returns:
            dict[str, int]: Dictionary mapping names to their occurrence count
        """
        names_count = {}
        for name in names_only:
            names_count[name] = names_count.get(name, 0) + 1
        return names_count

    def manual_group_without_gender(
        self, remaining_names: list[str], existing_group: list[list[str]], group_size: int, num_groups: int
    ) -> list[list[str]]:
        """Handle manual group formation with validation and edge cases"""
        # Validate inputs

        # Create copy and proceed with distribution
        rd.shuffle(remaining_names)
        existing_groups = copy.deepcopy(existing_group)

        # Get current group sizes
        group_sizes = [len(group) for group in existing_groups]

        # Distribute remaining names
        for name in remaining_names:
            # Find group with minimum size that hasn't reached max size
            valid_groups = [i for i, size in enumerate(group_sizes) if size < group_size]
            if not valid_groups:
                break

            # Add to smallest valid group
            min_group_idx = min(valid_groups, key=lambda i: group_sizes[i])
            existing_groups[min_group_idx].append(name)
            group_sizes[min_group_idx] += 1

        return existing_groups

    def check_groups_gender(self, existing_groups, male_count, female_count, error_text):
        for i, group in enumerate(existing_groups):
            male_in_group = sum(1 for name, gender in group if gender == "male")
            female_in_group = sum(1 for name, gender in group if gender == "female")

            # Kiểm tra nếu nhóm không đủ số nam hoặc nữ theo yêu cầu
            if male_in_group < male_count:
                error_text += f"\nNhóm {i + 1} chưa đủ {male_count} nam."
            if female_in_group < female_count:
                error_text += f"\nNhóm {i + 1} chưa đủ {female_count} nữ."

        return error_text

    def get_groups_remainging_names(self, names,output_text, group_num, remaining_names ):
        existing_groups = [[] for _ in range(group_num)]
        manually_assigned = []
        k = 0
        for group_box in output_text:
            group_memberss = [n.strip() for n in group_box.value.splitlines() if n.strip()]
            group_members = [
                        (name, gender) for name, gender in names if name in group_memberss
                    ]  
            # list các tuple(assigned_name, gender)
            existing_groups[k].extend(group_members)
            manually_assigned.extend(group_memberss)
            k += 1
        remaining_names = [(name, gender) for name, gender in names]
        for tup in remaining_names[:]:
            if tup[0] in manually_assigned:
                remaining_names.remove(tup)

        return {'existing_groups': existing_groups, 'remaining_names': remaining_names}

    def manual_group_with_gender(
        self,
        remaining_names: list[tuple[str, str]],
        existing_group: list[list[tuple[str, str]]],
        male_count: int,
        female_count: int,
        group_size: int,
    ) -> list[list[str]]:
        # Phân loại remaining_names theo giới tính

        males = [name for name, gender in remaining_names if gender == "male"]
        rd.shuffle(males)
        females = [name for name, gender in remaining_names if gender == "female"]
        rd.shuffle(females)
        
        # Chuyển đổi các nhóm hiện có để dễ xử lý
        groups = [list(group) for group in existing_group]
        
        # Hàm kiểm tra số lượng nam và nữ trong nhóm
        def count_gender(group):
            male_in_group = sum(1 for _, gender in group if gender == "male")
            female_in_group = sum(1 for _, gender in group if gender == "female")
            return male_in_group, female_in_group
        
        # Đảm bảo từng nhóm thỏa mãn số lượng tối thiểu
        for group in groups:
            male_in_group, female_in_group = count_gender(group)
            
            # Đảm bảo số lượng nam
            while male_in_group < male_count and males:
                group.append((males.pop(), "male"))
                male_in_group += 1
            
            # Đảm bảo số lượng nữ
            while female_in_group < female_count and females:
                group.append((females.pop(), "female"))
                female_in_group += 1

        # Phân bổ các phần tử còn lại vào các nhóm còn thiếu chỗ
        for group in groups:
            while len(group) < group_size and (males or females):
                if males:
                    group.append((males.pop(), "male"))
                elif females:
                    group.append((females.pop(), "female"))

        # Nếu vẫn còn phần tử chưa phân bổ, tạo nhóm mới
        while males or females:
            new_group = []
            while len(new_group) < group_size and (males or females):
                if males:
                    new_group.append((males.pop(), "male"))
                elif females:
                    new_group.append((females.pop(), "female"))
            groups.append(new_group)

        # Định dạng lại các nhóm để chỉ trả về tên
        result = [[name for name, _ in group] for group in groups]
        
        return result