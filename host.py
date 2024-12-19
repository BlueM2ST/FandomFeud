
import pygame
import sys
from rpc import RPCClient
from button import Button
from colorRect import ColorRect
from textBox import TextBox
from textEdit import TextEdit
from textureRect import TextureRect
from container import Container
from threading import Thread


pygame.init()

clock = pygame.time.Clock()

infoObject = pygame.display.Info()
monitorSize = (infoObject.current_w, infoObject.current_h)

# this line will set the window to borderless fullscreen
# screen = pygame.display.set_mode(monitorSize, pygame.NOFRAME)

# this winow size is the size that all nodes will scale from
windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('Halcon Feud')

server = RPCClient('127.0.0.1', 46980)

root = Container("root", 0, 0)
currentScene:str = "root"
rootNodes:dict = {"root": root}

roundData:dict = {}
currentRound:str = ""


def mainLoop():
    while True:
        # Set the frame rate
        clock.tick(120)
        # delta = clock.get_fps()/1000

        # Fill the display with color
        screen.fill((255, 255, 255))
        sceneNodes = rootNodes[currentScene].allChildren

        # this will force only one event per frame, some events may be lost (unlikely in this case)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            # quit the game
            server.disconnect()
            pygame.quit()
            sys.exit()
        for node in sceneNodes:
            action = node.handleEvent(event)
            if action:
                connections[action[0]](action[1])
            # draw/redraw objects on screen
            if not node.hidden:
                node.draw(screen, windowSize[0], windowSize[1])
        root.getChild("fps").setText(str(int(clock.get_fps())))
        pygame.display.flip()


def getScoreboardData(filename="scoreboard.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        round = ""
        for line in file.readlines():
            line = line.strip()
            if line.startswith("#"):
                round = line.replace("#", "")
                roundData[round] = []
            elif not line:
                continue
            else:
                roundData[round].append({"answer": line.split(",")[0], "score": line.split(",")[1].replace(" ", "")})


def hostCreateControlPanel():
    # round tabs
    pos = 100
    for round in roundData:
        root.getChild("roundTabContainer").addChild(Button(round, pos, 50, 100, 40, round, (150, 150, 150), ["hostRoundButtonClicked"]))
        pos += 110
    root.getChild("roundTabContainer").addChild(Button("fastmoney", pos, 50, 100, 40, "fast money", (150, 150, 150), ["hostFastMoneyButtonClicked"]))

    # answer slots
    x, y = (0, 0)
    for i in range(8):
        if i % 2:
            x = 400
            id = i + 4 - i/2
        else:
            x = 0
            y += 120
            id = i / 2
        id = str(int(id))
        background = ColorRect(id, x, y, 350, 75, (120, 120, 120))
        background.addChild(Button("button" + id, 0, 0, 100, 75, "None", (150, 150, 150), ["hostAnswerButtonClicked"], disabled=True))
        background.addChild(TextBox("textbox" + id, 100, 0, "Round not started", center=False, padding=30))
        root.getChild("scoreboardContainer").addChild(background)
    
    # X buttons

    # editable text
    root.getChild("scoreboardContainer").addChild(TextEdit("textedittext", 100, 650, 200, 100))


def hostShowRound(round):
    container = root.getChild("scoreboardContainer")
    for i in range(8):
        slot = container.getChild(str(i))
        # if there is an answer in this slot
        if i < len(roundData[round]):
            slot.getChild("button" + str(i)).setText("Show")
            slot.getChild("button" + str(i)).disabled = False
            slot.getChild("textbox" + str(i)).setText(roundData[round][i]["answer"])
        # if not, set it to blank
        else:
            slot.getChild("button" + str(i)).setText("")
            slot.getChild("button" + str(i)).disabled = True
            slot.getChild("textbox" + str(i)).setText("")


def hostFastMoneyButtonClicked(button:Button):
    pass


def hostRoundButtonClicked(button:Button):
    hostShowRound(button.name)
    # reset all button colors
    for tab in root.getChild("roundTabContainer").getChildren():
        tab.color = (150, 150, 150)
    # only color the selected button
    button.color = (100, 200, 200)
    if server.is_connected():
        server.clientShowRound(roundData[button.name])


def hostAnswerButtonClicked(button:Button):
    print("clicked on " + button.name)
    button.hide()


def hostConnectionButtonClicked(button:Button):
    serverThread = Thread(target = server.connect, daemon=True)
    serverThread.start()
    serverThread.join()
    if server.is_connected():
        button.free()


def hostXButtonClicked(button:Button):
    if server.is_connected():
        server.clientShowX(roundData[button.name])


# connects button clicks to a function
connections = {
    "hostAnswerButtonClicked": hostAnswerButtonClicked,
    "hostConnectionButtonClicked": hostConnectionButtonClicked,
    "hostRoundButtonClicked": hostRoundButtonClicked,
    "hostXButtonClicked": hostXButtonClicked,
    "hostFastMoneyButtonClicked": hostFastMoneyButtonClicked
}
# background
root.addChild(TextureRect("test", 0, 0, 1280, 720, "img/ff_bg_edited.jpg"))
# containers
root.addChild(Container("scoreboardContainer", 100, 0))
root.addChild(Container("roundTabContainer"))
root.addChild(Container("fastMoneyContainer"))
# show fps
root.addChild(TextBox("fps", 10, 10, "0"))
# rpc connect
root.addChild(Button("rpcConnectButton", 1240, 0, 40, 40, "rpc", (100, 100, 100), ["hostConnectionButtonClicked"]))

getScoreboardData()
hostCreateControlPanel()
mainLoop()
