

from pygame import image, transform
from .screenObject import ScreenObject


class TextureRect(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, imagePath:str):
        super().__init__(name, posX, posY)
        self.size = self.toVector((width, height))
        self.image = image.load(imagePath).convert_alpha()
    
    def draw(self, screen, initX, initY):
        x, y, w, h = self.scale(screen, initX, initY)
        image = transform.smoothscale(self.image, (w, h))
        screen.blit(image, (x, y))