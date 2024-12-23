
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
            # show/hide button
            background.addChild(Button("showButton", 0, 0, 60, 75, "None", (150, 150, 150), self.answerButtonClicked, disabled=True))
            # answer text
            background.addChild(TextBox("textbox", 0, 0, "Round not started", center=True))
            # points text
            background.addChild(Button("pointsDisplay", 300, 0, 50, 75, "0", (150, 150, 150)))

            self.root.getChild("scoreboardContainer").addChild(background)
        
        # X buttons
        self.root.getChild("scoreboardContainer").addChild(Button("smallX", 0, 640, 100, 50, "Small X", (150, 150, 150), self.xButtonClicked))
        self.root.getChild("scoreboardContainer").addChild(Button("oneX", 120, 640, 100, 50, "One X", (150, 150, 150), self.xButtonClicked))

        # show score for team and rounds
        self.root.getChild("scoreboardContainer").addChild(TextEdit("leftTeamScore", 800, 120, 100, 100, (100, 100, 100), (150, 150, 150), text="0", centerText=True))
        self.root.getChild("scoreboardContainer").addChild(TextEdit("currentRoundScore", 920, 120, 100, 100, (100, 100, 100), (150, 150, 150), text="0", centerText=True))
        self.root.getChild("scoreboardContainer").addChild(TextEdit("rightTeamScore", 1040, 120, 100, 100, (100, 100, 100), (150, 150, 150), text="0", centerText=True))

        # buttons to assign score for teams
        self.root.getChild("scoreboardContainer").addChild(Button("left", 800, 240, 100, 50, "Assign Left", (150, 150, 150), self.assignPoints))
        self.root.getChild("scoreboardContainer").addChild(Button("right", 1040, 240, 100, 50, "Assign Right", (150, 150, 150), self.assignPoints))

        # button to update points on client
        self.root.getChild("scoreboardContainer").addChild(Button("update", 920, 240, 100, 75, "Update", (150, 150, 150), self.updatePointsOnClient))


    def showRound(self, round):
        container = self.root.getChild("scoreboardContainer")
        for i in range(8):
            slot = container.getChild(str(i))
            # if there is an answer in this slot
            if i < len(self.roundData[round]):
                slot.getChild("showButton").setText("Show")
                slot.getChild("showButton").disabled = False
                slot.getChild("textbox").setText(self.roundData[round][i]["answer"])
                slot.getChild("pointsDisplay").setText(self.roundData[round][i]["score"])
            # if not, set it to blank
            else:
                slot.getChild("showButton").setText("")
                slot.getChild("showButton").disabled = True
                slot.getChild("textbox").setText("")
                slot.getChild("pointsDisplay").setText("")


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
        print("clicked on " + button.getParent().name)
        if button.getText() == "Show":
            button.setText("Hide")
            currentScoreDisplay = self.root.getChild("scoreboardContainer").getChild("currentRoundScore")
            pointsDisplay = button.getParent().getChild("pointsDisplay")
            currentScoreDisplay.setText(str(int(currentScoreDisplay.getText()) + int(pointsDisplay.getText())))


    def connectionButtonClicked(self, button:Button):
        serverThread = Thread(target = self.server.connect, daemon=True)
        serverThread.start()
        serverThread.join()
        if self.server.is_connected():
            button.free()


    def xButtonClicked(self, button:Button):
        if self.server.is_connected():
            self.server.showX(button.name)
    

    def assignPoints(self, button:Button):
        currentScoreDisplay = button.getParent().getChild("currentRoundScore")
        if button.name == "left":
            scoreDisplay = button.getParent().getChild("leftTeamScore")
        else:
            scoreDisplay = button.getParent().getChild("rightTeamScore")
        scoreDisplay.setText(str(int(currentScoreDisplay.getText()) + int(scoreDisplay.getText())))
        currentScoreDisplay.setText("0")
    
    def updatePointsOnClient(self, button:Button):
        pass





