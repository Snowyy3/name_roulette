import random as rd


class NameGenerator:
    def get_random_names(self, names: list[str], num_names: int) -> list[str]:
        return rd.sample(names, k=num_names)
