from model.name_generator import NameGenerator


class NameGenerationController:
    def __init__(self):
        self.name_generator = NameGenerator()

    def generate_name(self, num_names: int) -> list[str]:
        # Example list of names
        names = ["Alice", "Bob", "Charlie", "David", "Eve"]
        return self.name_generator.get_random_names(names, num_names)
