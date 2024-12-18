
from pygame import font
from screenObject import ScreenObject

font.init()
font = font.Font(None, 24)


class TextBox(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, text:str="", center:bool=True, padding:int=0):
        self.name = name
        self.pos = self.toVector((posX, posY))
        self.relPos = self.toVector((0, 0))
        self.text = text
        self.center = center
        self.padding = padding
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []


    def draw(self, screen, initX:int, initY:int):
        # scale with screen size
        x, y, w, h = self.scale(screen, initX, initY)
        # if text, draw text on top of background
        text = font.render(self.text, True, (0, 0, 0))
        textRect = (x, y)
        if self.center:
            textRect = text.get_rect(center = (x + self.getParent().size.x /2, y + self.getParent().size.y /2))
        screen.blit(text, (textRect[0] + self.padding, textRect[1] + self.padding))
    
    def setText(self, text):
        self.text = text
