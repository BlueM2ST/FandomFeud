
from pygame import Rect, font, draw
from screenObject import ScreenObject

font.init()
font = font.Font(None, 24)


class TextBox(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, text:str=""):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.width = 0
        self.height = 0
        self.text = text
        self.rect = Rect(0, 0, 0, 0)
        self.children = []
        self.parent = None
        self.nodes = []


    def draw(self, screen, initX:int, initY:int):
        # scale with screen size
        x, y, w, h = self.scale(screen, initX, initY)
        # if text, draw text on top of background
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (x + 10, y + 10))
    
    def setText(self, text):
        self.text = text
