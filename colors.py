import sys

class Colors:
    GREEN = (100, 200, 100)
    RED = (200, 100, 100)
    BLUE = (100, 100, 200)
    YELLOW = (200, 200, 100)
    PURPLE = (200, 100, 200)
    CYAN = (100, 200, 200)

    def list():
        return list([Colors.GREEN, Colors.RED, Colors.BLUE,
                     Colors.YELLOW, Colors.PURPLE, Colors.CYAN])