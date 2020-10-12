import pygame as pyg
import sys
import gameConstants as constants
from PlatformBuilder import Platform

clock = pyg.time.Clock()
pyg.init()
smaller_surface = pyg.Surface((1200, 600))

screen = pyg.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
player_cube = pyg.draw.rect(smaller_surface, (0, 0, 255), (50, constants.WINDOW_HEIGHT // 2 - 25, 50, 50))

# variables
gravity = 0.25
cube_movement = 0
SPAWN_PLATFORM_EVENT = pyg.USEREVENT
pyg.time.set_timer(SPAWN_PLATFORM_EVENT, 2000)
platform_list = []


def overlapping_platforms(platform_list):
    pass


def move_platforms():
    for platform in platform_list:
        platform.rect.centerx -= 2


def draw_platforms(surface):
    for platform in platform_list:
        pyg.draw.rect(surface, platform.color, platform.rect)
xot=50
while True:

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        if event.type == SPAWN_PLATFORM_EVENT:
            platform_top = Platform(smaller_surface, "UP")
            platform_bottom = Platform(smaller_surface, "DOWN")
            platform_list.append(platform_top)
            platform_list.append(platform_bottom)
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_DOWN:
                pass

    # KOGA KE "SKOKASH" ne go mrdash chovecheto tuku site platformi ke gi pridvizhish nadole

    smaller_surface.fill((0, 0, 0))
    move_platforms()
    draw_platforms(smaller_surface)

    pyg.draw.rect(smaller_surface, (0, 0, 255), (50, constants.WINDOW_HEIGHT // 2 - 25, 50, 50))
    pyg.draw.rect(smaller_surface, (0, 50, 210), (xot, constants.WINDOW_HEIGHT // 2 + 25, 300, 50))
    xot-=1
    screen.blit(smaller_surface, (0, 0))

    pyg.display.update()
    clock.tick(60)
