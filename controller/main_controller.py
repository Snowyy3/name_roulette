from model.name_generator import NameGenerator
from controller.group_former_controller import GroupFormationController

class MainController:
    def __init__(self, page):
        self.page = page
        self.name_generator = NameGenerator()
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

