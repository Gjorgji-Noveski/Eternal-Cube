import sys
import gameConstants as const
from collections import deque
import pygame as pyg
from PlatformBuilder import Platform
import random

pyg.init()

# Surfaces
screen = pyg.display.set_mode((800, 600))
platform_spawn_area = pyg.Surface((1600, 600)).convert()
player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), (50, const.WINDOW_HEIGHT // 2 - 25, 50, 50))

# Events ( USER event IDs should be between 24 and 32 )
SPAWN_NEW_PLATFORMS = 24
UPDATE_SCORE = 25

# Variables
platforms = deque([], 10)
pyg.time.set_timer(SPAWN_NEW_PLATFORMS, 1500)
pyg.time.set_timer(UPDATE_SCORE, 1000)
clock = pyg.time.Clock()
goingUP = False
goingDOWN = False
closestPlatforms = None
platformSpeed = 1
gameActive = False
homeScreenFont = pyg.font.Font(pyg.font.get_default_font(), 80)
scoreFont = pyg.font.Font(pyg.font.get_default_font(), 35)
highScore = 0
score = 0


def updateScore():
    global score
    score += 1


def reinitializeVariables():
    global platforms, goingUP, goingDOWN, closestPlatforms, platformSpeed, gameActive, score
    platforms.clear()
    goingUP = False
    goingDOWN = False
    closestPlatforms = None
    platformSpeed = 1
    score = 0


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


def moveClosestPlatforms(platforms, direction):
    global platformSpeed
    global closestPlatforms
    global goingUP
    global goingDOWN
    if direction == 'DOWN':
        platformSpeed -= 1
    else:
        platformSpeed += 1
    for platform in platforms:

        if direction == 'UP':
            if platforms[0].rect.bottom < player.top:
                platform.rect.move_ip(0, platformSpeed)
            else:
                platforms[0].rect.bottom = player.top + 1
                platformSpeed = 1
                closestPlatforms = None
                goingUP = False
                goingDOWN = False
        else:
            if platforms[1].rect.top > player.bottom:
                platform.rect.move_ip(0, platformSpeed)
            else:
                platforms[1].rect.top = player.bottom - 1
                platformSpeed = 1
                closestPlatforms = None
                goingUP = False
                goingDOWN = False


def checkIfPlayerMoved():
    global closestPlatforms
    if closestPlatforms is not None and closestPlatforms[0].rect.left < player.right:
        if closestPlatforms[0].rect.colliderect(player) or closestPlatforms[1].rect.colliderect(player):
            return True
        return False
    return True


# Looking for platforms that are the closest to the cube
def findClosestPlatform():
    global closestPlatforms, platforms
    for idx, platform in enumerate(platforms):  # OVDE GI IMA I GORNATA I DOLNATA PLATFORMA
        if platform.rect.right > player.right:
            closestPlatforms = [platform, platforms[idx + 1]]
            break


def renderScore():
    global scoreFont, score, platform_spawn_area
    scoreSurf = scoreFont.render("Score: %s" % score, True, const.WHITE, const.BLACK).convert()
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (const.WINDOW_WIDTH, 0)
    platform_spawn_area.blit(scoreSurf, scoreRect)


def homeScreen(mousePos, pressedButtons):
    global screen, homeScreenFont, gameActive, scoreFont, highScore
    gameTitleSurf = homeScreenFont.render("Eternal Cube", True, (150, 150, 150), const.BLACK).convert()
    gameTitleRect = gameTitleSurf.get_rect()
    gameTitleRect.midbottom = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT / 3)
    startSurf = homeScreenFont.render("START", True, const.BLUE, const.BLACK).convert()
    startSurfRect = startSurf.get_rect()
    startSurfRect.center = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT - const.WINDOW_HEIGHT / 3)
    # creating hover animation on Start button
    if startSurfRect.collidepoint(mousePos) and not gameActive:
        startSurf = homeScreenFont.render("START", True, const.BLUE, (150, 150, 150)).convert()
        # starting the game when left clicking
        if pressedButtons[0]:
            reinitializeVariables()
            gameActive = True
    updateHighScore()
    highScoreSurf = scoreFont.render("High Score %s" % highScore, True, const.WHITE, const.BLACK).convert()
    highScoreRect = highScoreSurf.get_rect()

    screen.blits(((gameTitleSurf, gameTitleRect, None), (startSurf, startSurfRect, None),(highScoreSurf, highScoreRect, None)))


def updateHighScore():
    global highScore, score
    if score > highScore:
        highScore = score


def detectCollisionWithRed():
    global platforms
    for platform in platforms:
        if platform.rect.colliderect(player) and platform.color == const.RED:
            return True
    return False


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
        if event.type == UPDATE_SCORE and gameActive:
            updateScore()

    homeScreen(pyg.mouse.get_pos(), pyg.mouse.get_pressed())
    if gameActive:
        platform_spawn_area.fill((0, 0, 0))
        movePlatforms()
        findClosestPlatform()
        if goingUP and closestPlatforms:
            moveClosestPlatforms(closestPlatforms, direction='UP')
        if goingDOWN and closestPlatforms:
            moveClosestPlatforms(closestPlatforms, direction='DOWN')
        if goingUP is not True and goingDOWN is not True:
            gameActive = checkIfPlayerMoved()
            if detectCollisionWithRed() is True:
                gameActive = False
        drawPlatforms()
        player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), player)
        renderScore()
        screen.blit(platform_spawn_area, (0, 0))


    pyg.display.update()
    clock.tick(60)

pyg.quit()
