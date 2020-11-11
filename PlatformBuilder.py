import random
from pygame import draw


class Platform:

    def __init__(self, surface,color, yPos, xPos=None):

        width = 250
        if xPos is not None:
            platform = draw.rect(surface, color, (xPos, yPos, width, 25))
        else:
            platform = draw.rect(surface, color, (800, yPos, width, 25))
        self.color = color
        self.rect = platform
