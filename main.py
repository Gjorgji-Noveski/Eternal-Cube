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
gameActive = False
font = pyg.font.Font(pyg.font.get_default_font(), 80)


def createPlatforms():
    colors = random.sample(const.COLORS, 2)
    platformBottom = Platform(platform_spawn_area, colors[0], player.bottom + player.height * 1.6)
    platformTop = Platform(platform_spawn_area, colors[1], player.top - player.height * 1.6)
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
            if platforms[0].rect.bottom < player.top:
                platform.rect.move_ip(0, movingPlatformSpeed)
            else:
                platforms[0].rect.bottom = player.top + 1
                movingPlatformSpeed = 1
                movingPlatforms = None
                goingUP = False
                goingDOWN = False
        else:
            if platforms[1].rect.top > player.bottom:
                platform.rect.move_ip(0, movingPlatformSpeed)
            else:
                platforms[1].rect.top = player.bottom - 1
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


def homeScreen(mousePos, pressedButtons):
    global screen, font, gameActive
    gameTitleSurf = font.render("Eternal Cube", True, (150, 150, 150), const.BLACK)
    gameTitleRect = gameTitleSurf.get_rect()
    gameTitleRect.midbottom = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT / 3)
    startSurf = font.render("START", True, const.BLUE, const.BLACK)
    startSurfRect = startSurf.get_rect()
    startSurfRect.center = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT - const.WINDOW_HEIGHT / 3)
    # creating hover animation on Start button
    if startSurfRect.collidepoint(mousePos):
        startSurf = font.render("START", True, const.BLUE, (150, 150, 150))
        # starting the game when left clicking
        if pressedButtons[0]:
            gameActive = True
    screen.blits(((gameTitleSurf, gameTitleRect, None), (startSurf, startSurfRect, None)))


def detectCollision():
    for platform in platforms:
        if platform.rect.colliderect(player) and platform.color == const.RED:
            return False
    return True


while True:

    # TODO: PREJAKA IDEJA, namesto da odish na platformata, vlezi vo nea, kako vo tunel, zelen crven
    # TODO: ne se oslonuvaj kreiranje na platformi vremenski na odredeni intervali, deka ako korisnikot ima mal fps
    #  ke bidat nabutani tuku kreiraj koga vishe ednata platforma ke bide vo odredena lokacija na ekranot

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

    homeScreen(pyg.mouse.get_pos(), pyg.mouse.get_pressed())
    if gameActive:
        platform_spawn_area.fill((0, 0, 0))
        movePlatforms()
        if goingUP:
            findClosestPlatform(direction='UP')
        if goingDOWN:
            findClosestPlatform(direction='DOWN')
        gameActive = detectCollision()
        drawPlatforms()
        player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), player)
        screen.blit(platform_spawn_area, (0, 0))

    pyg.display.update()
    clock.tick(60)

pyg.quit()
