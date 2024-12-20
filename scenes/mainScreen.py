
from .nodes.button import Button
from .nodes.colorRect import ColorRect
from .nodes.textBox import TextBox
from .nodes.textEdit import TextEdit
from .nodes.textureRect import TextureRect
from .nodes.container import Container
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
        self.root.addChild(Container("scoreboardContainer", 100, 0))

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
        self.root.addChild(TextureRect("smallX", 540, 260, 200, 200, "img/wrong.png"))


    def showRound(self, round):
        pass


    def showAnswer(self, id:str):
        pass


    def showX(self, name:str):
        self.root.getChild(name).show()
        # TODO: test if this is what we actually want to use here
        sleep(3)
        self.root.getChild(name).hide()
