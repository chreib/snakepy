import sys

class Direction:
    UP = [0, -1]
    DOWN = [0, 1]
    RIGHT = [1, 0]
    LEFT = [-1, 0]

    def are_opposite(dir1, dir2):
        return dir1[0] == -dir2[0] or dir1[1] == -dir2[1]

