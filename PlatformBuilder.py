from pygame import draw


class Platform:

    def __init__(self, surface,color, yPos):

        width = 250
        platform = draw.rect(surface, color, (800, yPos, width, 25))
        self.color = color
        self.rect = platform
