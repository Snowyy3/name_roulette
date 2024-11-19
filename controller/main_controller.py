import flet as ft
from model.user_authentication import UserAuthentication
from controller.user_authentication_controller import UserAuthenticationController
from controller.name_generation_controller import NameGenerationController
from controller.group_former_controller import GroupFormationController


class MainController:
    def __init__(self, page: ft.Page):
        self.page = page

        # Create a single UserAuthentication instance
        # Since if not, 2 instances = change password/forgot password are out of sync and won't work
        self.user_auth = UserAuthentication()

        # Initialize controllers with shared UserAuthentication instance
        self.auth = UserAuthenticationController(page, auth=self.user_auth)
        self.name_generation = NameGenerationController()
        self.group_formation = GroupFormationController()

    def generate_name(self, names: list[str], num_names: int = 1) -> list[str]:
        return self.name_generator.get_random_names(names, num_names)

    def form_groups(self, names: list[str], group_size: int = None, num_groups: int = None) -> list[list[str]]:
        """Forms groups based on user input.

        Args:
            names (list[str]): The list of names to be grouped.
            group_size (int): The desired number of people per group.
            num_groups (int): The desired number of groups.

        Returns:
            list[list[str]]: A list of grouped names.
        """
        return self.group_formation.form_groups(names, group_size, num_groups)
