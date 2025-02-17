
import pygame
import sys
from rpc import RPCClient, RPCServer
from scenes.nodes.container import Container
from scenes.nodes.textBox import TextBox
from scenes import scoreboard, mainScreen


pygame.init()

clock = pygame.time.Clock()
TARGETFPS = 120

# these lines will set the window to borderless fullscreen
# infoObject = pygame.display.Info()
# screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.NOFRAME)

# this winow size is the size that all nodes will scale from
windowSize = (1280, 720)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption('Halcon Feud')

# determine if running as client or server
args = sys.argv
if len(args) > 1 and args[1] == "client":
    print("set up as client")
    server = RPCServer('127.0.0.1', 46980)
    initScene = mainScreen.MainScreen(server)
else:
    print("set up as host")
    server = RPCClient('127.0.0.1', 46980)
    initScene = scoreboard.ScoreBoard(server)

root = Container("root", 0, 0)


def mainLoop():
    fps:int = 0
    frame:int = 0
    fpsNode = root.getChild("fps")
    while True:
        # delta = clock.get_fps()/1000

        # Fill the display with color
        screen.fill((255, 255, 255))
        sceneNodes = root.allChildren

        # this will force only one event per frame, some events may be lost (unlikely in this case)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            # quit the game
            server.disconnect()
            pygame.quit()
            sys.exit()
        for node in sceneNodes:
            # draw/redraw objects on screen, handle events
            if not node.hidden:
                node.handleEvent(event)
                node.draw(screen, windowSize[0], windowSize[1])
        frame += 1
        fps += clock.get_fps()
        if frame == TARGETFPS:
            fpsNode.setText(str(int(fps/TARGETFPS)))
            frame = 0
            fps = 0
        pygame.display.flip()
        # Set the frame rate
        clock.tick(TARGETFPS)



initScene.create()
root.addChild(initScene.getRoot())
# show fps
root.addChild(TextBox("fps", 10, 10, "0"))

mainLoop()
