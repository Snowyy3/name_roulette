import random as rd
import copy

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
    
    def generate_names_with_gender(self, names: list[tuple[str, str]], male_count: int, female_count: int, group_size: int = None, num_groups: int = None) -> list[str]:
        """Tạo danh sách nhóm với số lượng nam và nữ chính xác trong tổng số đã cho.

        Args:
            names (list[tuple[str, str]]): Danh sách tên kèm giới tính.
            male_count (int): Số lượng nam cần chọn.
            female_count (int): Số lượng nữ cần chọn.
            group_size (int, optional): Kích thước nhóm (số lượng người trong mỗi nhóm).
            num_groups (int, optional): Số nhóm cần chia.

        Returns:
            list[str]: Danh sách các nhóm đã được chia, hoặc danh sách rỗng nếu không thể tạo nhóm theo yêu cầu.
        """

        if not names:
            return []

        if group_size is None and num_groups is None:
            raise ValueError("Phải cung cấp ít nhất 'group_size' hoặc 'num_groups'.")

        # Kiểm tra số lượng nam và nữ có đủ cho mỗi nhóm không
        gendered_names = self.separate_by_gender(names)
        males, females = gendered_names["male"], gendered_names["female"]

        # Kiểm tra nếu đủ số lượng nam hoặc nữ để chia nhóm # Phải sửa lại đoạn này
        if len(males) < num_groups and len(females) < num_groups:
            raise ValueError("Not enough males or females to form a group as required.")

        groups = [[] for _ in range(num_groups)]
        
        # Chắc chắn mỗi nhóm có ít nhất một nam nếu có đủ nam
        if len(males) >= num_groups:
            for i in range(num_groups):
                group_males = rd.sample(males, 1)
                groups[i].append(group_males[0])
                males.remove(group_males[0])

        # Chắc chắn mỗi nhóm có ít nhất một nữ nếu có đủ nữ
        if len(females) >= num_groups:
            for i in range(num_groups):
                group_females = rd.sample(females, 1)
                groups[i].append(group_females[0])
                females.remove(group_females[0])

        # Phân bổ các tên còn lại vào nhóm
        remaining_names = females + males
        rd.shuffle(remaining_names)
        index = 0
        for name in remaining_names:
            groups[index].append(name)
            index = (index + 1) % num_groups

        # Lọc bỏ nhóm trống
        groups = [g for g in groups if g]

        return groups

    def manual_group_without_gender(self, remaining_names: list[str], existing_group: list[list[str]], group_size: int, num_groups: int) -> list[list[str]]:
        rd.shuffle(remaining_names)
        existing_groups = copy.deepcopy(existing_group)
        # Xác định số thành viên ban đầu của từng nhóm
        group_sizes = [len(group) for group in existing_groups]

        # Phân bổ tên vào nhóm
        while remaining_names:
            # Xác định số thành viên nhỏ nhất hiện tại
            min_size = min(group_sizes)

            # Phân bổ các tên cho các nhóm có số thành viên = min_size
            for i, group in enumerate(existing_groups):
                if len(group) == min_size and remaining_names:
                    group.append(remaining_names.pop(0))  # Thêm tên vào nhóm
                    group_sizes[i] += 1  # Cập nhật kích thước nhóm

        return existing_groups
    
    def check_groups_gender(self, existing_groups, male_count, female_count, error_text):
        for i, group in enumerate(existing_groups):
            male_in_group = sum(1 for name, gender in group if gender == 'male')
            female_in_group = sum(1 for name, gender in group if gender == 'female')
            
            # Kiểm tra nếu nhóm không đủ số nam hoặc nữ theo yêu cầu
            if male_in_group < male_count:
                error_text += f"\nNhóm {i+1} chưa đủ {male_count} nam."
            if female_in_group < female_count:
                error_text += f"\nNhóm {i+1} chưa đủ {female_count} nữ."
        
        return error_text
    def manual_group_with_gender (self, remaining_names: list[tuple[str, str]], existing_group: list[list[tuple[str, str]]],  male_count: int, female_count: int, group_size: int, num_groups: int) -> list[list[str]]:
        # Phân loại remaining_names theo giới tính
        males = [name for name, gender in remaining_names if gender.lower() == "male"]
        females = [name for name, gender in remaining_names if gender.lower() == "female"]

        # Copy existing_group để tránh thay đổi input
        groups = [group[:] for group in existing_group]

        # Tạo hàm tính số lượng nam và nữ trong một nhóm
        def count_gender(group):
            group_males = len([name for name, gender in group if gender.lower() == "male"])
            group_females = len([name for name, gender in group if gender.lower() == "female"])
            return group_males, group_females


        # Ưu tiên chia nữ trước
        if male_count == 0: 
            while females:
                # Sắp xếp nhóm dựa trên số nữ hiện tại (nhóm rỗng sẽ được ưu tiên)
                groups.sort(key=lambda g: count_gender(g)[1])  # Sắp xếp nhóm theo số lượng nữ
                for group in groups:
                    if len(group) < group_size and count_gender(group)[1] < female_count:
                        group.append((females.pop(0), 'female'))  # Thêm 1 nữ vào nhóm
                        break

        # Sau đó chia nam
        if female_count == 0:
            while males:
                # Sắp xếp nhóm dựa trên số nam hiện tại (nhóm rỗng sẽ được ưu tiên)
                groups.sort(key=lambda g: count_gender(g)[0])  # Sắp xếp nhóm theo số lượng nam
                for group in groups:
                    if len(group) < group_size and count_gender(group)[0] < male_count:
                        group.append((males.pop(0), 'male'))  # Thêm 1 nam vào nhóm
                        break

        # Chia đều remaining_names (nếu còn) vào các nhóm theo phương pháp round-robin
        remaining_members = females + males
        rd.shuffle(remaining_members)
        for member in remaining_members:
            for group in groups:
                if len(group) < group_size:
                    group.append((member, 'female' if member in females else 'male'))
                    break

        # Trả về danh sách các nhóm với chỉ tên
        return [[name for name, gender in group] for group in groups]

