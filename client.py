import pygame
import sys
from rpc import RPCServer
from button import Button
from colorRect import ColorRect
from textBox import TextBox
from textureRect import TextureRect
from container import Container
from audioPlayer import AudioPlayer
from threading import Thread
from time import sleep


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
    x, y = (220, 180)
    for i in range(8):
        if i % 2:
            x = 560
            id = i + 4 - i/2
        else:
            x = 220
            y += 60
            id = i / 2
        background = ColorRect(str(id), x, y, 300, 50, (120, 120, 120))
        background.addChild(TextBox("textBox" + str(id), 0, 0, "Round not started"))
        root.getChild("scoreboardContainer").addChild(background)
    
    # X icons
    root.addChild(TextureRect("smallX", 540, 260, 200, 200, "img/wrong.png"))


def clientShowRound(round):
    pass


def clientShowAnswer(id:str):
    pass


def clientShowX(name:str):
    root.getChild(name).show()
    # TODO: test if this is what we actually want to use here
    sleep(3)
    root.getChild(name).hide()


root.addChild(TextureRect("test", 0, 0, 1280, 720, "img/ff_bg_edited.jpg"))
root.addChild(TextureRect("test", 0, 0, 1280, 720, "img/board.png"))
root.addChild(TextBox("fps", 10, 10, "0"))
root.addChild(Container("scoreboardContainer", 100, 0))
server.registerMethod(clientShowRound)
server.registerMethod(clientShowAnswer)
server.registerMethod(clientShowX)
serverThread = Thread(target = server.run, daemon=True)
serverThread.start()
clientShowScoreboard()
mainLoop()
