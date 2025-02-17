
from pygame import draw, Vector2
from .node import Node


class ColorRect(Node):
    def __init__(self, name:str, pos:Vector2, size:Vector2, color=(255, 255, 0)):
        super().__init__(name, pos)
        self.size = size
        self.color = color
    
    def draw(self, screen, initX, initY):
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)
    
    def setColor(self, color):
        self.color = color