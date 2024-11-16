from model.group_former import GroupFormer


class GroupFormationController:
    def __init__(self):
        self.group_former = GroupFormer()

    def form_groups(self, names: list[str], group_size: int = None, num_groups: int = None) -> list[list[str]]:
        """
        Forms groups based on the provided names and grouping parameters.

        Args:
            names (list[str]): The list of names to be grouped.
            group_size (int, optional): The desired number of people per group.
            num_groups (int, optional): The desired number of groups.

        Returns:
            list[list[str]]: A list of grouped names.
        """
        try:
            return self.group_former.group_formation(names, group_size=group_size, num_groups=num_groups)
        except (ValueError, TypeError) as e:
            print(f"Error forming groups: {e}")
            return []

    def distribute_remaining(
        self, groups: list[list[str]], remaining_members: list[str], distribute_randomly: bool = True
    ) -> list[list[str]]:
        """
        Handles any remaining members by either distributing them across groups or adding as a separate group.

        Args:
            groups (list[list[str]]): The list of groups formed.
            remaining_members (list[str]): Members not initially assigned to groups.
            distribute_randomly (bool): If True, distributes remaining members randomly among existing groups.

        Returns:
            list[list[str]]: Groups after handling remaining members.
        """
        return self.group_former.handle_uneven_groups(
            groups, remaining_members, distribute_randomly=distribute_randomly
        )

    def manual_assign(self, groups: list[list[str]], assignments: dict[int, list[str]]) -> list[list[str]]:
        """
        Manually assigns specified members to specified groups.

        Args:
            groups (list[list[str]]): The current list of groups.
            assignments (dict[int, list[str]]): A dictionary where keys are group indices (starting from 1) and
                                                values are lists of names to be assigned to that group.

        Returns:
            list[list[str]]: The updated groups after manual assignment.
        """
        try:
            return self.group_former.manual_assignment(groups, assignments)
        except (ValueError, TypeError) as e:
            print(f"Error in manual assignment: {e}")
            return []


