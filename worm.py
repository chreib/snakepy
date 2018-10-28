from direction import Direction

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
        self.speed = 1
        self.tick_sum = 0
    
    def set_direction(self,direction):
        if not Direction.are_opposite (self.direction, direction):
            self.direction = direction

    def set_speed(self, new_speed):
        self.speed = new_speed

    def move(self):
        if not self.is_alive:
            return

        self.tick_sum += self.speed
        while self.tick_sum >= 1:
            self.tick_sum -= 1
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
