import pygame
import sys
from rpc import RPCServer
from button import Button
from colorRect import ColorRect
from textBox import TextBox


pygame.init()

clock = pygame.time.Clock()

infoObject = pygame.display.Info()
monitorSize = (infoObject.current_w, infoObject.current_h)

# this line will set the window to borderless fullscreen
# screen = pygame.display.set_mode(monitorSize, pygame.NOFRAME)

windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('Halcon Feud')

server = RPCServer()


root = ColorRect("root", 0, 0, windowSize[0], windowSize[1], (255, 255, 255))
currentScene:str = "root"
rootNodes = {"root": root}


def mainLoop():
    delta:float = 0
    while True:
        # Set the frame rate
        clock.tick(60)
        delta = clock.get_fps()/1000

        # Fill the display with color
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit the game
                pygame.quit()
                sys.exit()
        # draw/redraw objects on screen
        for node in rootNodes[currentScene].getAllChilden():
            node.draw(screen, windowSize[0], windowSize[1])
        root.getChild("fps").setText(str(int(clock.get_fps())))
        pygame.display.flip()



def clientShowSoreboard():
    print("showing scoreboard")


root.addChild(TextBox("fps", 10, 10, "0"))
server.registerMethod(clientShowSoreboard)
server.start()
mainLoop()
