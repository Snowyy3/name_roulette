from model.name_generator import NameGenerator


class MainController:
    def __init__(self, page):
        self.page = page
        self.name_generator = NameGenerator()
    def generate_name(self, names: list[str], num_names: int = 1) -> str | list[str]:
        return self.name_generator.get_random_names(names, num_names)
