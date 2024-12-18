
from pygame import draw
from screenObject import ScreenObject


class ColorRect(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, color:tuple):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.color = color
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []
    
    def draw(self, screen, initX, initY):
        # draw button background
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)
    
        