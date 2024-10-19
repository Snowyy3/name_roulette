import random as rd


class NameGenerator:
    def get_random_names(self, names: list[str]) -> str | list[str]:
        # No filtering for now
        randomized_name = rd.choices(names, k=1)
        return randomized_name
