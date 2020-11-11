import sys
import gameConstants as const
from collections import deque
import pygame as pyg
from PlatformBuilder import Platform
import random
pyg.init()
# Surfaces
screen = pyg.display.set_mode((800, 600))
platform_spawn_area = pyg.Surface((1600, 600))
player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), (50, const.WINDOW_HEIGHT // 2 - 25, 50, 50))

# Variables
platforms = deque([], 10)
SPAWN_NEW_PLATFORMS = pyg.USEREVENT
pyg.time.set_timer(SPAWN_NEW_PLATFORMS, 1500)
clock = pyg.time.Clock()
goingUP = False
goingDOWN = False
movingPlatforms = None
movingPlatformSpeed = 1
gameActive = True


def createPlatforms():
    colors = random.sample(const.COLORS,2)
    if len(platforms) == 0:
        platformBottom = Platform(platform_spawn_area, colors[0],player.bottomleft[1] + player.height)
        platformTop = Platform(platform_spawn_area, colors[1],player.topleft[1] - player.height * 2)
        platforms.append(platformTop)
        platforms.append(platformBottom)
    if platforms[-1].rect.right < 800:
        platformBottom = Platform(platform_spawn_area,colors[0], player.bottomleft[1] + player.height)
        platformTop = Platform(platform_spawn_area, colors[1],player.topleft[1] - player.height * 2 )
        platforms.append(platformTop)
        platforms.append(platformBottom)


def movePlatforms():
    for platform in platforms:
        platform.rect.move_ip(-5, 0)


def drawPlatforms():
    for platform in platforms:
        pyg.draw.rect(platform_spawn_area, platform.color, platform.rect)


def movePlatform(platforms, direction):
    global movingPlatformSpeed
    global movingPlatforms
    global goingUP
    global goingDOWN
    if direction == 'DOWN':
        movingPlatformSpeed -= 1
    else:
        movingPlatformSpeed += 1
    for platform in platforms:

        if direction == 'UP':
            if platforms[0].rect.y < player.bottom:
                platform.rect.move_ip(0, movingPlatformSpeed)
            else:
                platforms[0].rect.y = player.bottom
                movingPlatformSpeed = 1
                movingPlatforms = None
                goingUP = False
                goingDOWN = False
        else:
            if platforms[1].rect.y > player.bottom:
                platform.rect.move_ip(0, movingPlatformSpeed)
            else:
                platforms[1].rect.y = player.bottom
                movingPlatformSpeed = 1
                movingPlatforms = None
                goingUP = False
                goingDOWN = False


# Looking for the bottom platform
def findClosestPlatform(direction):
    global goingUP
    global movingPlatforms
    if movingPlatforms is not None:
        movePlatform(movingPlatforms, direction)
    else:
        for idx, platform in enumerate(platforms):  # OVDE GI IMA I GORNATA I DOLNATA PLATFORMA
            if platform.rect.x > player.right:
                movingPlatforms = [platform, platforms[idx + 1]]
                break


def detectCollision():
    for platform in platforms:
        if platform.rect.colliderect(player):
            return False
    return True

def checkIfOnCorrectPlatform():
    global gameActive
    for platform in platforms:
        if platform.rect.left < player.right < platform.rect.right and player.bottom == platform.rect.top:
            if platform.color == const.RED:
                gameActive = False
#TODO: PREJAKA IDEJA, namesto da odish na platformata, vlezi vo nea, kako vo tunel, zelen crven
while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        if event.type == SPAWN_NEW_PLATFORMS:
            createPlatforms()
        if event.type == pyg.KEYDOWN:
            # Remember, we are moving the platforms not the player, goingUP will bring the platforms down,
            # and vice versa
            if event.key == pyg.K_UP:
                goingUP = True
            if event.key == pyg.K_DOWN:
                goingDOWN = True
            if event.key == pyg.K_r and gameActive == False:
                platforms.clear()
                gameActive = True

    if gameActive:
        platform_spawn_area.fill((0, 0, 0))
        movePlatforms()
        if goingUP:
            findClosestPlatform(direction='UP')
        if goingDOWN:
            findClosestPlatform(direction='DOWN')
        gameActive = detectCollision()
        checkIfOnCorrectPlatform()
        drawPlatforms()
        player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), player)
        screen.blit(platform_spawn_area, (0, 0))

        pyg.display.update()
        clock.tick(60)
pyg.quit()