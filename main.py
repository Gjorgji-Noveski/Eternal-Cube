import sys
import os
import gameConstants as const
from collections import deque
import pygame as pyg
from PlatformBuilder import Platform
import random
os.environ['SDL_VIDEO_CENTERED '] = '1'
pyg.init()
pyg.display.set_caption('Eternal Cube')
# Events
SPAWN_NEW_PLATFORMS = pyg.event.custom_type()
UPDATE_SCORE = pyg.event.custom_type()
INCREASE_SPEED = pyg.event.custom_type()

# Variables
platforms = deque([], 10)
pyg.time.set_timer(SPAWN_NEW_PLATFORMS, 1500)
pyg.time.set_timer(UPDATE_SCORE, 1000)
pyg.time.set_timer(INCREASE_SPEED, 6000)
clock = pyg.time.Clock()
goingUP = False
goingDOWN = False
closestPlatforms = None
platformSpeed = 1
gameActive = False
crashed = False
howToPlay = False
highScore = 0
score = 0
PLATFORM_SPEED = -5
explanationText = ["Press the UP and DOWN arrow keys to go to a platform", "Not gliding on any platform makes you lose", "Green - good", "Red - Bad"]

# Fonts
titleFont = pyg.font.Font(pyg.font.get_default_font(), 80)
scoreFont = pyg.font.Font(pyg.font.get_default_font(), 35)
textFont = pyg.font.Font(pyg.font.get_default_font(), 60)
explanationFont = pyg.font.Font(pyg.font.get_default_font(), 20)

# Surfaces
screen = pyg.display.set_mode((800, 600))
platform_spawn_area = pyg.Surface((1600, 600)).convert()
player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), (50, const.WINDOW_HEIGHT // 2 - 25, 50, 50))
gameTitleSurf = titleFont.render("Eternal Cube", True, (150, 150, 150), const.BLACK).convert()
startTextSurf = titleFont.render("START", True, const.BLUE, const.BLACK).convert()
startTextSurfHovered = titleFont.render("START", True, const.BLUE, (150, 150, 150)).convert()
highScoreSurf = scoreFont.render("High Score: %s" % highScore, True, const.WHITE, const.BLACK).convert()
deathTextSurf = titleFont.render("You crashed :(", True, const.RED, const.BLACK).convert()
retryTextSurf = textFont.render("Retry", True, const.BLUE, const.BLACK).convert()
retryTextSurfHovered = textFont.render("Retry", True, const.BLUE, (150, 150, 150)).convert()
homeTextSurf = textFont.render("Main menu", True, const.BLUE, const.BLACK).convert()
homeTextSurfHovered = textFont.render("Main menu", True, const.BLUE, (150, 150, 150)).convert()
tutorialTextSurf = textFont.render("How to play", True, const.BLUE, const.BLACK).convert()
tutorialTextSurfHovered = textFont.render("How to play", True, const.BLUE, (150, 150, 150)).convert()
explanationTextSurfs = []

# Rects
gameTitleRect = gameTitleSurf.get_rect()
gameTitleRect.midbottom = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT / 3)
startTextRect = startTextSurf.get_rect()
startTextRect.center = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT - const.WINDOW_HEIGHT / 3)
highScoreRect = highScoreSurf.get_rect()
deathTextRect = deathTextSurf.get_rect()
deathTextRect.midbottom = (int(const.WINDOW_WIDTH / 2), int(const.WINDOW_HEIGHT / 3))
retryTextRect = retryTextSurf.get_rect()
retryTextRect.center = (int(const.WINDOW_WIDTH / 2), int(const.WINDOW_HEIGHT / 2))
homeTextRect = homeTextSurf.get_rect()
homeTextRect.midtop = (int(const.WINDOW_WIDTH / 2), int(const.WINDOW_HEIGHT - const.WINDOW_HEIGHT / 3))
tutorialTextRect = tutorialTextSurf.get_rect()
tutorialTextRect.center = (const.WINDOW_WIDTH / 2, const.WINDOW_HEIGHT / 2)


def makeExplanationTextSurfs():
    global explanationText, explanationFont, explanationTextSurfs
    for line in explanationText:
        explanationTextSurfs.append(explanationFont.render(line, True, const.WHITE, const.BLACK).convert())


def updateScore():
    global score
    score += 1


def reinitializeVariables():
    global platforms, goingUP, goingDOWN, closestPlatforms, platformSpeed, gameActive, score, PLATFORM_SPEED, crashed
    platforms.clear()
    goingUP = False
    goingDOWN = False
    crashed = False
    closestPlatforms = None
    platformSpeed = 1
    score = 0
    PLATFORM_SPEED = -5


def createPlatforms():
    colors = random.sample(const.COLORS, 2)
    platformBottom = Platform(platform_spawn_area, colors[0], player.bottom + player.height * 1.6)
    platformTop = Platform(platform_spawn_area, colors[1], player.top - player.height * 1.6)
    platforms.append(platformTop)
    platforms.append(platformBottom)


def movePlatforms():
    global PLATFORM_SPEED
    for platform in platforms:
        platform.rect.move_ip(PLATFORM_SPEED, 0)


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
    global closestPlatforms, platforms
    if closestPlatforms is not None and closestPlatforms[0].rect.left < player.right < closestPlatforms[0].rect.right:
        if closestPlatforms[0].rect.colliderect(player) or closestPlatforms[1].rect.colliderect(player):
            return True
        return False
    return True


# Looking for platforms that are the closest to the cube
def findClosestPlatform():
    global closestPlatforms, platforms
    for idx, platform in enumerate(platforms):  # Both platforms are present here
        if platform.rect.right > player.right:
            closestPlatforms = [platform, platforms[idx + 1]]
            break


def renderScore():
    global scoreFont, score, platform_spawn_area
    scoreSurf = scoreFont.render("Score: %s" % score, True, const.WHITE, const.BLACK).convert()
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (const.WINDOW_WIDTH, 0)
    platform_spawn_area.blit(scoreSurf, scoreRect)


def homeScreen():
    global platform_spawn_area, gameTitleSurf, gameTitleRect, startTextSurf, startTextRect, highScoreSurf, highScoreRect, startTextSurfHovered, highScore, tutorialTextSurf, tutorialTextRect
    screen.fill((0, 0, 0))
    if startTextRect.collidepoint(pyg.mouse.get_pos()):
        screen.blit(startTextSurfHovered, startTextRect, None)
    else:
        screen.blit(startTextSurf, startTextRect, None)
    if tutorialTextRect.collidepoint(pyg.mouse.get_pos()):
        screen.blit(tutorialTextSurfHovered, tutorialTextRect)
    else:
        screen.blit(tutorialTextSurf, tutorialTextRect)
    highScoreSurf = scoreFont.render("High Score: %s" % highScore, True, const.WHITE, const.BLACK).convert()
    screen.blits(((gameTitleSurf, gameTitleRect, None), (highScoreSurf, highScoreRect, None)))


def tutorialScreen():
    global screen, explanationTextSurfs, homeTextSurf, homeTextRect
    screen.fill((0, 0, 0))
    textPos = ((const.WINDOW_WIDTH / 3) / 2, (const.WINDOW_HEIGHT / 3) / 2)
    for line in range(len(explanationTextSurfs)):
        screen.blit(explanationTextSurfs[line], (textPos[0], textPos[1] + (line * 30)))
    if homeTextRect.collidepoint(pyg.mouse.get_pos()):
        screen.blit(homeTextSurfHovered, homeTextRect)
    else:
        screen.blit(homeTextSurf, homeTextRect)


def deathScreen():
    global deathTextSurf, deathTextRect, retryTextSurf, retryTextRect, homeTextSurf, homeTextRect, retryTextSurfHovered, homeTextSurfHovered
    updateHighScore()

    if retryTextRect.collidepoint(pyg.mouse.get_pos()):
        screen.blit(retryTextSurfHovered, retryTextRect, None)
    else:
        screen.blit(retryTextSurf, retryTextRect, None)
    if homeTextRect.collidepoint(pyg.mouse.get_pos()):
        screen.blit(homeTextSurfHovered, homeTextRect, None)
    else:
        screen.blit(homeTextSurf, homeTextRect, None)

    screen.blit(deathTextSurf, deathTextRect, None)


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


makeExplanationTextSurfs()
while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        if gameActive and not crashed:
            if event.type == SPAWN_NEW_PLATFORMS:
                createPlatforms()
            if event.type == pyg.KEYDOWN:
                # Remember, we are moving the platforms not the player, goingUP will bring the platforms down,
                # and vice versa
                if event.key == pyg.K_UP:
                    goingUP = True
                if event.key == pyg.K_DOWN:
                    goingDOWN = True
            if event.type == UPDATE_SCORE:
                updateScore()
            if event.type == INCREASE_SPEED:
                PLATFORM_SPEED -= 2
        elif not gameActive and crashed:
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if homeTextRect.collidepoint(pyg.mouse.get_pos()):
                        reinitializeVariables()
                        homeScreen()
                        gameActive = False
                    elif retryTextRect.collidepoint(pyg.mouse.get_pos()):
                        reinitializeVariables()
                        gameActive = True
        elif howToPlay:
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if homeTextRect.collidepoint(pyg.mouse.get_pos()):
                        howToPlay = False
                        homeScreen()
        else:
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if startTextRect.collidepoint(pyg.mouse.get_pos()):
                        gameActive = True
                    if tutorialTextRect.collidepoint(pyg.mouse.get_pos()):
                        tutorialScreen()
                        howToPlay = True

    if not gameActive and crashed:
        deathScreen()
    elif gameActive:
        platform_spawn_area.fill((0, 0, 0))
        movePlatforms()
        findClosestPlatform()
        if goingUP and closestPlatforms:
            moveClosestPlatforms(closestPlatforms, direction='UP')
        if goingDOWN and closestPlatforms:
            moveClosestPlatforms(closestPlatforms, direction='DOWN')
        if goingUP is False and goingDOWN is False:
            gameActive = checkIfPlayerMoved()
        if detectCollisionWithRed() is True:
            gameActive = False
        drawPlatforms()
        player = pyg.draw.rect(platform_spawn_area, (0, 0, 250), player)
        renderScore()
        if not gameActive:
            crashed = True
            deathScreen()
        screen.blit(platform_spawn_area, (0, 0))
    elif howToPlay:
        tutorialScreen()
    else:
        homeScreen()
    pyg.display.update()
    clock.tick(60)
pyg.quit()
