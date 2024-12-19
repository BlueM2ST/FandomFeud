
from pygame import draw
from screenObject import ScreenObject


class ColorRect(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, color:tuple):
        super().__init__(name, posX, posY)
        self.size = self.toVector((width, height))
        self.color = color
    
    def draw(self, screen, initX, initY):
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)
    
        