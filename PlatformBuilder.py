import random
from pygame import draw


class Platform:
    _RED = (255, 0, 0)
    _GREEN = (0, 255, 0)
    _COLORS = (_RED, _GREEN)

    def __init__(self,surface,position):
        color = random.choice(self._COLORS)
        width = 150
        if position=="UP":
            Y = 100
        else:
            Y = 200
        platform = draw.rect(surface, color, (800, Y, width, 20))
        self.color = color
        self.rect = platform

