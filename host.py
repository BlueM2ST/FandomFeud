
import pygame
import sys

import button


pygame.init()

clock=pygame.time.Clock()

infoObject = pygame.display.Info()
monitorSize = (infoObject.current_w, infoObject.current_h)

# this line will set the window to borderless fullscreen
# screen = pygame.display.set_mode(monitorSize, pygame.NOFRAME)

windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('Halcon Feud')

interactables:list = []

def mainLoop():
    while True:
        # Set the frame rate
        clock.tick(60)

        # Fill the display with color
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for interactable in interactables:
                    if interactable.rect.collidepoint(event.pos):
                        interactable.onClick()

        for interactable in interactables:
            interactable.draw(screen, windowSize[0], windowSize[1])
        pygame.display.flip()


def createHostDisplay():
    textButton = button.Button(100, 100, 100, 100, "testing")
    interactables.append(textButton)


createHostDisplay()
mainLoop()
