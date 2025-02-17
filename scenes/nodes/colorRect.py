
from pygame import draw, Vector2
from .node import ScreenObject


class ColorRect(ScreenObject):
    color = (0,0,0)
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int):
        super().__init__(name, posX, posY)
        self.size = Vector2(width, height)
    
    def draw(self, screen, initX, initY):
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)
    
    def setColor(self, color):
        self.color = color