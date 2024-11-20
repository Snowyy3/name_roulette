from model.group_former import GroupFormer
import logging

logger = logging.getLogger(__name__)


class GroupFormationController:
    def __init__(self):
        self.group_former = GroupFormer()

    def handle_input_change(self, names: str, group_size: str, group_num: str) -> None:
        """Handle input changes and update view accordingly"""
        try:
            names_list = [n.strip() for n in names.splitlines() if n.strip()]
            size = int(group_size) if group_size else None
            num = int(group_num) if group_num else None

            if self.group_former.validate_input(names_list, size, num):
                new_size, new_num = self.group_former.calculate_group_parameters(len(names_list), size, num)
                return new_size, new_num
        except ValueError as e:
            logger.error(f"Input validation error: {e}")
            return None, None

    def form_groups(self, names: list[str], **kwargs) -> list[list[str]]:
        """Coordinate group formation between view and model."""
        try:
            if kwargs.get("gender_filter") != "none":
                return self._form_groups_with_gender(names, **kwargs)
            elif kwargs.get("manual_group") != "none":
                return self._form_groups_with_manual(names, **kwargs)
            else:
                return self.group_former.group_formation(
                    names, group_size=kwargs.get("group_size"), num_groups=kwargs.get("group_num")
                )
        except Exception as e:
            logger.error(f"Error forming groups: {e}")
            return []

    def _form_groups_with_gender(self, names: list[str], **kwargs) -> list[list[str]]:
        """Handle gender-based group formation"""
        try:
            # Ensure we have valid integer values
            male_count = int(kwargs.get("male_count", 0))
            female_count = int(kwargs.get("female_count", 0))
            group_size = int(kwargs.get("group_size")) if kwargs.get("group_size") else None
            num_groups = int(kwargs.get("num_groups")) if kwargs.get("num_groups") else None

            # Validate that we have at least one of group_size or num_groups
            if group_size is None and num_groups is None:
                raise ValueError("Either group_size or num_groups must be provided")

            # Call model method with validated parameters
            return self.group_former.generate_names_with_gender(
                names,
                male_count=male_count,
                female_count=female_count,
                group_size=group_size,
                num_groups=num_groups,
            )
        except Exception as e:
            logger.error(f"Error in gender-based group formation: {e}")
            raise ValueError(f"Failed to form gender-based groups: {str(e)}")

    def _form_groups_with_manual(self, names: list[str], **kwargs) -> list[list[str]]:
        """Handle manual group formation"""
        try:
            # Ensure we have valid lists
            if names is None:
                names = []

            existing_groups = kwargs.get("existing_groups")
            if existing_groups is None:
                existing_groups = []

            # Validate numeric parameters
            group_size = kwargs.get("group_size")
            if not isinstance(group_size, int) or group_size <= 0:
                raise ValueError("Invalid group size")

            num_groups = kwargs.get("group_num")
            if not isinstance(num_groups, int) or num_groups <= 0:
                raise ValueError("Invalid number of groups")

            logger.debug(f"Manual group formation with {len(names)} names into {num_groups} groups")

            return self.group_former.manual_group_without_gender(
                remaining_names=names,
                existing_group=existing_groups,
                group_size=group_size,
                num_groups=num_groups,
            )
        except Exception as e:
            logger.error(f"Error in manual group formation: {e}")
            # Return empty list instead of None to prevent iteration errors
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
