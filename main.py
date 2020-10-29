import sys
import gameConstants as const
from collections import deque
import pygame as pyg
from PlatformBuilder import Platform

pyg.init()
screen = pyg.display.set_mode((800, 600))
platform_spawn_area = pyg.Surface((1600, 600))
player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), (50, const.WINDOW_HEIGHT // 2 - 25, 50, 50))
platforms = deque([], 10)
SPAWN_NEW_PLATFORMS = pyg.USEREVENT
pyg.time.set_timer(SPAWN_NEW_PLATFORMS, 2000)
clock = pyg.time.Clock()
goingUP = False
goingDOWN = False


def createPlatforms():
    if len(platforms) == 0:
        platformBottom = Platform(platform_spawn_area, player.bottomleft[1] + player.height)
        platformTop = Platform(platform_spawn_area, player.topleft[1] - player.height * 2)
        platforms.append(platformBottom)
        platforms.append(platformTop)
    if platforms[-1].rect.right < 800:
        platformBottom = Platform(platform_spawn_area, player.bottomleft[1] + player.height)
        platformTop = Platform(platform_spawn_area, player.topleft[1] - player.height * 2)
        platforms.append(platformBottom)
        platforms.append(platformTop)


def movePlatforms():
    for platform in platforms:
        platform.rect.move_ip(-5, 0)


def drawPlatforms():
    for platform in platforms:
        pyg.draw.rect(platform_spawn_area, platform.color, platform.rect)


def movingUp():
    global goingUP
    next_platform = None
    for platform in platforms:#OVDE GI IMA I GORNATA I DOLNATA PLATFORMA
        if platform.rect.y < player.y:
            next_platform = platform
            break
    if next_platform is not None:
        while next_platform.rect.y < player.y:
            next_platform.rect.move_ip(0,5)


# TODO: PREJAKA IDEJA, namesto da odish na platformata, vlezi vo nea, kako vo tunel, zelen crven
def movingDown():
    pass


while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        if event.type == SPAWN_NEW_PLATFORMS:
            createPlatforms()
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_UP:
                goingUP = True
            if event.key == pyg.K_DOWN:
                goingDOWN = True
    platform_spawn_area.fill((0, 0, 0))

    movePlatforms()
    if goingUP:
        movingUp()
    if goingDOWN:
        movingDown()
    drawPlatforms()
    player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), player)
    screen.blit(platform_spawn_area, (0, 0))

    pyg.display.update()
    clock.tick(60)
pyg.quit()
