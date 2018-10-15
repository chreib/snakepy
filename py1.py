import sys, pygame, random

class Direction:
    UP = [0, -1]
    DOWN = [0, 1]
    RIGHT = [1, 0]
    LEFT = [-1, 0]

    def are_opposite(dir1, dir2):
        return dir1[0] == -dir2[0] or dir1[1] == -dir2[1]


KEY2DIR1 = {pygame.K_UP : Direction.UP,
           pygame.K_DOWN : Direction.DOWN,
           pygame.K_LEFT : Direction.LEFT,
           pygame.K_RIGHT : Direction.RIGHT}

KEY2DIR2 = {pygame.K_w : Direction.UP,
           pygame.K_s : Direction.DOWN,
           pygame.K_a : Direction.LEFT,
           pygame.K_d : Direction.RIGHT}

def zirkular(v, upper_value):
    if v < 0:
        return upper_value
    elif v > upper_value:
        return 0
    else:
        return v

class Wurm:
    # positions: von links oben nach unten, rechts 
    def __init__(self,color,startposition,size_felder):
        self.COLOR = color
        self.direction = Direction.RIGHT
        self.positions = [startposition]
        self.more = 3
        self.size_felder = size_felder
        self.is_alive = True
    
    def set_direction(self,direction):
        if not Direction.are_opposite (self.direction, direction):
            self.direction = direction

    def move(self):
        if not self.is_alive:
            return

        # Liste positions beginnt beim Kopf
        new_x = zirkular(self.positions[0][0] + self.direction[0], self.size_felder[0])
        new_y = zirkular(self.positions[0][1] + self.direction[1], self.size_felder[1])

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

def calc_scaling(size, size_felder):
    return (int(size[0] / size_felder[0]), int(size[1] / size_felder[1]))

def draw_rect(screen, size, size_felder, field, color):
    sx, sy = calc_scaling(size, size_felder)
    rect = pygame.Rect(field[0]*sx, field[1]*sy, sx, sy)
    pygame.draw.rect(screen, color, rect)
    return


def draw_wurm(screen, size, size_felder, wurm):
    for position in wurm.get_positions():
        draw_rect(screen, size, size_felder, position, wurm.get_color())
    return

def draw_food(screen, size, size_felder, food):
    draw_rect(screen, size, size_felder, food, (250, 40, 40))
    return

def random_field(size_felder):
    return [random.randint(0, size_felder[0]), random.randint(0, size_felder[1])]

def calc_new_food_position(size_felder, wuermer):
    all_wurm_positions = []
    for wurm in wuermer: all_wurm_positions += wurm.get_positions()
    new_position = random_field(size_felder)
    while new_position in all_wurm_positions:
        new_position = random_field(size_felder)
    return new_position

def new_wuermer():
    wurm1 = Wurm((100,200,100), [10,10], size_felder)
    wurm2 = Wurm((200,100,100), [30,30], size_felder)
    return ([wurm1, wurm2], [KEY2DIR1, KEY2DIR2])

pygame.init()

# Martin Beamer: (1920, 1080)
infoObject = pygame.display.Info()
size = infoObject.current_w, infoObject.current_h

# with open('test.txt', 'w') as f:
#     f.write(str(size))

size_felder = 100,50
black = 0, 0, 0

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()

mainloop = True

wuermer, wuermer_keys_map = new_wuermer()

food = [size_felder[0]/2, size_felder[1]/2]
growth_factor = 1

while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            elif event.key == pygame.K_F5:
                wuermer, wuermer_keys_map = new_wuermer()
            else:
                for wurm, keys_map in zip(wuermer, wuermer_keys_map):
                    if event.key in keys_map.keys():
                        wurm.set_direction(keys_map[event.key])

    screen.fill(black)

    for wurm in wuermer:
        draw_wurm(screen, size, size_felder, wurm)
        draw_food(screen, size, size_felder, food)
        wurm.move()
        if wurm.collides_with ([food]):
            wurm.grow(growth_factor)
            growth_factor += 1
            food = calc_new_food_position (size_felder, wuermer)

        for other_wurm in wuermer:
            if other_wurm != wurm and wurm.collides_with(other_wurm.get_positions()):
                wurm.die()

    # screen.blit(ball, ballrect)
    pygame.display.flip()
    pygame.time.wait(50)