
from .nodes.button import Button
from .nodes.colorRect import ColorRect
from .nodes.textBox import TextBox
from .nodes.textEdit import TextEdit
from .nodes.textureRect import TextureRect
from .nodes.container import Container
from .nodes.scene import Scene
from threading import Thread


class ScoreBoard(Scene):
    def __init__(self, server=None):
        super().__init__(server)
        self.roundData:dict = {}
        self.currentRound:str = ""
    
    def create(self):
        self.getScoreboardData()
        self.createControlPanel()


    def getScoreboardData(self, filename="scoreboard.txt"):
        with open(filename, "r", encoding="utf-8") as file:
            round = ""
            for line in file.readlines():
                line = line.strip()
                if line.startswith("#"):
                    round = line.replace("#", "")
                    self.roundData[round] = []
                elif not line:
                    continue
                else:
                    self.roundData[round].append({"answer": line.split(",")[0], "score": line.split(",")[1].replace(" ", "")})


    def createControlPanel(self):
        # background
        self.root.addChild(TextureRect("test", 0, 0, 1280, 720, "img/ff_bg_edited.jpg"))
        # containers
        self.root.addChild(Container("scoreboardContainer", 100, 0))
        self.root.addChild(Container("roundTabContainer"))
        # rpc connect button
        self.root.addChild(Button("rpcConnectButton", 1240, 0, 40, 40, "rpc", (100, 100, 100), self.connectionButtonClicked))
        # round tabs
        pos = 100
        for round in self.roundData:
            self.root.getChild("roundTabContainer").addChild(Button(round, pos, 50, 100, 40, round, (150, 150, 150), self.roundButtonClicked))
            pos += 110
        self.root.getChild("roundTabContainer").addChild(Button("fastmoney", pos, 50, 100, 40, "fast money", (150, 150, 150), self.fastMoneyButtonClicked))

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
            background.addChild(Button("button" + id, 0, 0, 100, 75, "None", (150, 150, 150), self.answerButtonClicked, disabled=True))
            background.addChild(TextBox("textbox" + id, 100, 0, "Round not started", center=False, padding=30))
            self.root.getChild("scoreboardContainer").addChild(background)
        
        # X buttons

        # editable text
        self.root.getChild("scoreboardContainer").addChild(TextEdit("textedit", 100, 600, 200, 100, (100, 100, 100), (150, 150, 150), centerText=True))


    def showRound(self, round):
        container = self.root.getChild("scoreboardContainer")
        for i in range(8):
            slot = container.getChild(str(i))
            # if there is an answer in this slot
            if i < len(self.roundData[round]):
                slot.getChild("button" + str(i)).setText("Show")
                slot.getChild("button" + str(i)).disabled = False
                slot.getChild("textbox" + str(i)).setText(self.roundData[round][i]["answer"])
            # if not, set it to blank
            else:
                slot.getChild("button" + str(i)).setText("")
                slot.getChild("button" + str(i)).disabled = True
                slot.getChild("textbox" + str(i)).setText("")


    def fastMoneyButtonClicked(self, button:Button):
        # change scene here
        pass


    def roundButtonClicked(self, button:Button):
        self.showRound(button.name)
        # reset all button colors
        for tab in self.root.getChild("roundTabContainer").getChildren():
            tab.color = (150, 150, 150)
        # only color the selected button
        button.color = (100, 200, 200)
        if self.server.is_connected():
            self.server.showRound(self.roundData[button.name])


    def answerButtonClicked(self, button:Button):
        print("clicked on " + button.name)
        button.hide()


    def connectionButtonClicked(self, button:Button):
        serverThread = Thread(target = self.server.connect, daemon=True)
        serverThread.start()
        serverThread.join()
        if self.server.is_connected():
            button.free()


    def xButtonClicked(self, button:Button):
        if self.server.is_connected():
            self.server.showX(self.roundData[button.name])





