
import pygame
import sys
from rpc import RPCClient
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

server = RPCClient('127.0.0.1', 46980)

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
        sceneNodes = rootNodes[currentScene].getAllChilden()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit the game
                server.disconnect()
                pygame.quit()
                sys.exit()
            # handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for node in sceneNodes:
                    if node.rect.collidepoint(event.pos):
                        action = node.onClick()
                        if action:
                            connections[action[0]](action[1])
        # draw/redraw objects on screen
        for node in sceneNodes:
            node.draw(screen, windowSize[0], windowSize[1])
        root.getChild("fps").setText(str(int(clock.get_fps())))
        pygame.display.flip()


def hostCreateControlPanel():
    x, y, w, h = (100, 0, 300, 100)
    for i in range(8):
        if i % 2:
            x = 600
            id = i + 4 - i/2
        else:
            x = 100
            y += 120
            id = i / 2
        root.addChild(hostCreateAnswerSlot(str(int(id)), x, y, w, h))


def hostCreateAnswerSlot(id:str, x:int, y:int, w:int, h:int) -> list:
    background = ColorRect("bg" + id, x + w/3, y, w, h, (120, 120, 120))
    button = Button("button" + id, x, y, w/3, h, "show", (150, 150, 150), ["hostAnswerButtonClicked"])
    answer = TextBox("textBox" + id, x + w/3, y, "This is an answer: " + button.name)
    background.addChild(button)
    background.addChild(answer)
    return background


def hostAnswerButtonClicked(button:Button):
    print("clicked on " + button.name)
    button.getParent().free()


def hostConnectionButtonClicked(button:Button):
    if server.is_connected():
        button.free()
    server.connect()


# connects button clicks to a function
connections = {
    "hostAnswerButtonClicked": hostAnswerButtonClicked,
    "hostConnectionButtonClicked": hostConnectionButtonClicked
}
hostCreateControlPanel()
root.addChild(TextBox("fps", 10, 10, "0"))
root.addChild(Button("rpcConnectButton", 1240, 0, 40, 40, "rpc", (100, 100, 100), ["hostConnectionButtonClicked"]))
mainLoop()
