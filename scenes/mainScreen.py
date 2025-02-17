
from .nodes.colorRect import ColorRect
from .nodes.textBox import TextBox
from .nodes.textureRect import TextureRect
from .nodes.node import Node
from .nodes.scene import Scene
from threading import Thread
from time import sleep


class MainScreen(Scene):
    def __init__(self, server=None):
        super().__init__(server)
        self.server.registerMethod(self.showRound)
        self.server.registerMethod(self.showAnswer)
        self.server.registerMethod(self.showX)

        self.serverThread = Thread(target = server.run, daemon=True)
        self.serverThread.start()
    

    def create(self):
        self.createScoreboard()
    

    def createScoreboard(self):
        self.root.addChild(TextureRect("test", 0, 0, 1280, 720, "img/ff_bg_edited.jpg"))
        self.root.addChild(TextureRect("test", 0, 0, 1280, 720, "img/board.png"))
        self.root.addChild(Node("scoreboardContainer", 100, 0))

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
            self.root.getChild("scoreboardContainer").addChild(background)
        
        # X icons
        self.root.addChild(TextureRect("smallX", 540, 260, 200, 200, "img/wrong.png")).hide()


    def showRound(self, round):
        pass


    def showAnswer(self, id:str):
        pass


    def showX(self, name:str):
        xNode = self.root.getChild(name)
        if xNode.hidden:
            self.root.getChild(name).show()
            # this will block the process, but should be fine
            sleep(2)
            self.root.getChild(name).hide()
