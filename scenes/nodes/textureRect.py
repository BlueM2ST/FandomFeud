

from pygame import image, transform, Vector2
from .node import Node


class TextureRect(Node):
    def __init__(self, name:str, pos:Vector2, size:Vector2, imagePath:str):
        super().__init__(name, pos)
        self.size = size
        self.image = image.load(imagePath).convert_alpha()
    
    def draw(self, screen, initX, initY):
        x, y, w, h = self.scale(screen, initX, initY)
        image = transform.smoothscale(self.image, (w, h))
        screen.blit(image, (x, y))