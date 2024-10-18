import random

class NameGenerator:
    def generate_random_names(self, names, gender_filter):
        # For now, we'll ignore the gender filter and just shuffle the names
        shuffled_names = names.copy()
        random.shuffle(shuffled_names)
        return shuffled_names
