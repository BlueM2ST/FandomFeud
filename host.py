
import pygame
import sys
import button
from colorRect import ColorRect

pygame.init()

clock=pygame.time.Clock()

infoObject = pygame.display.Info()
monitorSize = (infoObject.current_w, infoObject.current_h)

# this line will set the window to borderless fullscreen
# screen = pygame.display.set_mode(monitorSize, pygame.NOFRAME)

windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('Halcon Feud')

screenObjects:list = []

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
            # handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for screenObj in screenObjects:
                    if screenObj.rect.collidepoint(event.pos):
                        action = screenObj.onClick()
                        if action:
                            connections[action[0]](action[1])
        # draw/redraw objects on screen
        for screenObj in screenObjects:
            screenObj.draw(screen, windowSize[0], windowSize[1])
        pygame.display.flip()


def hostCreateControlPanel():
    textButton = button.Button("answerButton1", 100, 100, 100, 100, "testing", connection=["hostAnswerButtonClicked"])
    screenObjects.append(textButton)
    screenObjects.append(ColorRect("Test rect", 200, 200, 100, 100, (255, 255, 0)))


def hostAnswerButtonClicked(button:str):
    print("clicked on " + button.name)


connections = {"hostAnswerButtonClicked": hostAnswerButtonClicked}
hostCreateControlPanel()
mainLoop()
