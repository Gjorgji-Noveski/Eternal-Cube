import random
from pygame import draw


class Platform:
    _RED = (255, 0, 0)
    _GREEN = (0, 255, 0)
    _COLORS = (_RED, _GREEN)

    def __init__(self, surface, yPos, xPos=None):
        color = random.choice(self._COLORS)
        width = 250
        if xPos is not None:
            platform = draw.rect(surface, color, (xPos, yPos, width, 25))
        else:
            platform = draw.rect(surface, color, (800, yPos, width, 25))
        self.color = color
        self.rect = platform
