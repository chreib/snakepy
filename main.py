import sys, pygame, random, ctypes
from direction import Direction
from colors import Colors
from food import Food
from worm import Worm
from arena import Arena


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
    draw_rect(screen, size, size_fields, food.get_position(), food.get_color())
    return

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
tick_time = 50

arena = Arena(size_fields)
arena.init(4)

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
            elif event.key == pygame.K_KP_PLUS:
                tick_time = int(tick_time*0.5)
            elif event.key == pygame.K_KP_MINUS:
                tick_time = int(tick_time*2)
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
    pygame.time.wait(tick_time)