
import pygame
import sys
from button import Button
from colorRect import ColorRect
from textBox import TextBox


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
    # TODO: clean up this math
    x = 100
    y = 50
    w = 300
    h = 100
    for i in range(8):
        if i >= 4:
            x = 600
        if i == 4:
            y = 50
        y += 120
        for object in hostCreateAnswerSlot(str(i), x, y, w, h):
            screenObjects.append(object)


def hostCreateAnswerSlot(id:str, x:int, y:int, w:int, h:int) -> list:
    button = Button("button" + id, x, y, w/3, h, "show", (150, 150, 150), ["hostAnswerButtonClicked"])
    background = ColorRect("bg" + id, x + w/3, y, w, h, (120, 120, 120))
    answer = TextBox("textBox" + id, x + w/3, y, "some answer here" + button.name)
    return [background, button, answer]


def hostAnswerButtonClicked(button:Button):
    print("clicked on " + button.name)


# connects button clicks to a function
connections = {"hostAnswerButtonClicked": hostAnswerButtonClicked}
hostCreateControlPanel()
mainLoop()
