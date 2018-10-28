import sys, pygame, random, ctypes
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

def circular(v, upper_value):
    if v < 0:
        return upper_value
    elif v > upper_value:
        return 0
    else:
        return v

class Worm:
    # positions: von links oben nach unten, rechts 
    def __init__(self,color,start_position,size_fields):
        self.COLOR = color
        self.direction = Direction.RIGHT
        self.positions = [start_position]
        self.more = 3
        self.size_fields = size_fields
        self.is_alive = True
    
    def set_direction(self,direction):
        if not Direction.are_opposite (self.direction, direction):
            self.direction = direction

    def move(self):
        if not self.is_alive:
            return

        # Liste positions beginnt beim Kopf
        new_x = circular(self.positions[0][0] + self.direction[0], self.size_fields[0])
        new_y = circular(self.positions[0][1] + self.direction[1], self.size_fields[1])

        new_position = [new_x, new_y]
        if self.more > 0:
            self.more -= 1
            self.positions = [new_position] + self.positions
        else:
            self.positions = [new_position] + self.positions[:-1]

        if new_position in self.positions[1:]:
            self.die()

    def collides_with(self, other_positions):
        return self.positions[0] in other_positions

    def grow(self,size):
        self.more += size

    def get_positions(self):
        return self.positions[:]

    def get_color(self):
        if self.is_alive:
            return self.COLOR
        else:
            return (100, 100, 100)

    def die(self):
        self.is_alive = False

def calc_scaling(size, size_fields):
    return (int(size[0] / size_fields[0]), int(size[1] / size_fields[1]))

def draw_rect(screen, size, size_fields, field, color):
    sx, sy = calc_scaling(size, size_fields)
    rect = pygame.Rect(field[0]*sx, field[1]*sy, sx, sy)
    pygame.draw.rect(screen, color, rect)
    return

def draw_worm(screen, size, size_fields, worm):
    for position in worm.get_positions():
        draw_rect(screen, size, size_fields, position, worm.get_color())
    return

def draw_food(screen, size, size_fields, food):
    draw_rect(screen, size, size_fields, food, (250, 40, 40))
    return

def random_field(size_fields):
    return [random.randint(0, size_fields[0]), random.randint(0, size_fields[1])]



def calc_new_free_position_old(size_fields, worms):
    all_worm_positions = []
    for worm in worms: all_worm_positions += worm.get_positions()
    new_position = random_field(size_fields)
    while new_position in all_worm_positions:
        new_position = random_field(size_fields)
    return new_position

def new_worms():
    worm1 = Worm((100,200,100), [10,10], size_fields)
    worm2 = Worm((200,100,100), [30,30], size_fields)
    return ([worm1, worm2], [KEY2DIR1, KEY2DIR2])

class Arena:
    def __init__(self, size_fields):
        self.worms = []
        self.dead_worms = []
        self.worm_colors = Colors.list()
        self.key_list = [KEY2DIR1, KEY2DIR2]
        self.size_fields = size_fields
        self.food = self.calc_new_free_position()
        self.growth_factor = 1

    def init(self, n_worms):
        self.worms = []
        for i in range(n_worms):
            self.create_worm()

    def get_all_worms(self):
        return list(self.worms) + list(self.dead_worms)

    def get_all_food(self):
        return [self.food]

    def create_worm(self):
        new_index = len(self.worms)
        self.worms += [Worm(self.worm_colors[new_index], self.calc_new_free_position(), self.size_fields)]

    def calc_new_free_position(self):
        occupied_positions = []
        for worm in self.worms: occupied_positions += worm.get_positions()
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
        for worm in self.worms:
            worm.move()
            if worm.collides_with([self.food]):
                worm.grow(self.growth_factor)
                self.growth_factor += 1
                self.food = self.calc_new_free_position()

            for other_worm in self.worms:
                if other_worm != worm and worm.collides_with(other_worm.get_positions()):
                    worm.die()


pygame.init()

# Martin Beamer: (1920, 1080)
infoObject = pygame.display.Info()
ctypes.windll.user32.SetProcessDPIAware()
size = int(infoObject.current_w*0.8), int(infoObject.current_h*0.8)

# with open('test.txt', 'w') as f:
#     f.write(str(size))

size_fields = 100,50
black = 0, 0, 0

screen = pygame.display.set_mode((size[0], size[1]), pygame.NOFRAME)

# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()

mainloop = True

arena = Arena(size_fields)
arena.init(2)

while mainloop:
    key_list = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_F5:
                arena.init(2)
            else:
                key_list += [event.key]
    
    arena.handle_keys(key_list)
                
    screen.fill(black)

    arena.tick()

    for food in arena.get_all_food():
        draw_food(screen, size, size_fields, food)
    for worm in arena.get_all_worms():
        draw_worm(screen, size, size_fields, worm)

    pygame.display.flip()
    pygame.time.wait(50)