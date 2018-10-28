import random, pygame
from worm import Worm
from food import FoodType, Food
from direction import Direction
from colors import Colors

KEY2DIR1 = {pygame.K_UP : Direction.UP,
           pygame.K_DOWN : Direction.DOWN,
           pygame.K_LEFT : Direction.LEFT,
           pygame.K_RIGHT : Direction.RIGHT}

KEY2DIR2 = {pygame.K_w : Direction.UP,
           pygame.K_s : Direction.DOWN,
           pygame.K_a : Direction.LEFT,
           pygame.K_d : Direction.RIGHT}

KEY2DIR3 = {pygame.K_t : Direction.UP,
           pygame.K_f : Direction.LEFT,
           pygame.K_g : Direction.DOWN,
           pygame.K_h : Direction.RIGHT}

KEY2DIR4 = {pygame.K_i : Direction.UP,
           pygame.K_j : Direction.LEFT,
           pygame.K_k : Direction.DOWN,
           pygame.K_l : Direction.RIGHT}

class Arena:
    def __init__(self, size_fields):
        self.worms = []
        self.dead_worms = []
        self.worm_colors = Colors.list()
        self.key_list = [KEY2DIR1, KEY2DIR2, KEY2DIR3, KEY2DIR4]
        self.size_fields = size_fields
        self.food = []
        self.growth_factor = 1

    def init(self, n_worms):
        self.worms = []
        self.food = []
        self.create_food(FoodType.STANDARD)
        for i in range(n_worms):
            self.create_worm()

    def get_all_worms(self):
        return list(self.worms) + list(self.dead_worms)

    def get_all_food(self):
        return list(self.food)

    def create_worm(self):
        new_index = len(self.worms)
        self.worms += [Worm(self.worm_colors[new_index], self.calc_new_free_position(), self.size_fields)]
    
    def create_food(self, type):
        self.food += [Food(self.calc_new_free_position(),type,self.growth_factor)]

    def restart_worm(self,i_worm):
        self.worms[i_worm] = Worm(self.worm_colors[i_worm],self.calc_new_free_position(), self.size_fields)

    def calc_new_free_position(self):
        occupied_positions = []
        for worm in self.get_all_worms(): occupied_positions += worm.get_positions()
        for food in self.get_all_food(): occupied_positions += food.get_position()
        new_position = self.random_field()
        while new_position in occupied_positions:
            new_position = self.random_field()
        return new_position

    def random_field(self):
        return [random.randint(0, self.size_fields[0]), random.randint(0, self.size_fields[1])]

    def handle_keys(self,keys):
        for worm, keys_map in zip(self.worms, self.key_list[:len(self.worms)]):
            key_applied = False
            for key in keys:
                if key in keys_map.keys() and not key_applied:
                    worm.set_direction(keys_map[key])
                    key_applied = True


    def tick(self):
        for i_worm,worm in enumerate(self.worms):
            worm.move()
            for food in self.get_all_food():
                if worm.collides_with([food.get_position()]):
                    self.food.remove(food)
                    self.create_food(FoodType.random_type())
                    if food.get_type() == FoodType.STANDARD:
                        worm.grow(self.growth_factor)
                        self.growth_factor += 1
                        worm.set_speed(1)
                    elif food.get_type() == FoodType.UNLIMITED_GROWTH:
                        worm.set_speed(0.5)

            for other_worm in self.get_all_worms():
                if other_worm != worm and worm.collides_with(other_worm.get_positions()):
                    worm.die()
                    self.dead_worms += [worm]
                    self.restart_worm(i_worm)
