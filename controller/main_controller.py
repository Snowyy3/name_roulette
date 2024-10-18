from model.name_generator import NameGenerator

class MainController:
    def __init__(self, page):
        self.page = page
        self.name_generator = NameGenerator()

    def generate_random_names(self, names, gender_filter):
        return self.name_generator.generate_random_names(names, gender_filter)
