import pygame
import sys
from rpc import RPCServer
from button import Button
from colorRect import ColorRect
from textBox import TextBox
from textureRect import TextureRect
from container import Container
from threading import Thread


pygame.init()

clock = pygame.time.Clock()

infoObject = pygame.display.Info()
monitorSize = (infoObject.current_w, infoObject.current_h)

# this line will set the window to borderless fullscreen
# screen = pygame.display.set_mode(monitorSize, pygame.NOFRAME)

windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('Halcon Feud')

server = RPCServer('127.0.0.1', 46980)


root = Container("root")
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


def clientShowScoreboard():
    print("showing scoreboard")
    x, y, w, h = (320, 100, 300, 50)
    for i in range(8):
        if i % 2:
            x = 660
            id = i + 4 - i/2
        else:
            x = 320
            y += 60
            id = i / 2
        background = ColorRect(str(id), x, y, w, h, (120, 120, 120))
        background.addChild(TextBox("textBox" + str(id), x + w/3, y, "Round not started"))
        root.addChild(background)


def clientShowRound(round):
    pass


def clientShowAnswer(id:str):
    pass


root.addChild(TextBox("fps", 10, 10, "0"))
server.registerMethod(clientShowRound)
server.registerMethod(clientShowAnswer)
serverThread = Thread(target = server.run, daemon=True)
serverThread.start()
clientShowScoreboard()
mainLoop()
