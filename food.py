import random
from enum import Enum, auto
from colors import Colors

class FoodType(Enum):
    STANDARD = auto()
    UNLIMITED_GROWTH = auto()

    @staticmethod
    def list():
        return list(map(lambda c: c, FoodType))

    @staticmethod
    def random_type():
        all_types = FoodType.list()
        random_index = random.randint(0, len(all_types)-1)
        return all_types[random_index]


class Food:
    def __init__(self, position, type, growth):
        self.position = position
        self.type = type
        self.growth = growth
        self.type_colors = {FoodType.STANDARD:Colors.BRIGHT_RED,
                            FoodType.UNLIMITED_GROWTH:Colors.BRIGHT_GREEN}

    def get_type(self):
        return self.type
    
    def get_position(self):
        return self.position

    def get_growth(self):
        return self.growth

    def get_color(self):
        return self.type_colors[self.type]