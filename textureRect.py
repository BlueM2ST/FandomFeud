

from pygame import image, transform
from screenObject import ScreenObject


class TextureRect(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, imagePath:str):
        self.name = name
        self.pos = self.toVector((posX, posY))
        self.relPos = self.toVector((0, 0))
        self.size = self.toVector((width, height))
        self.image = image.load(imagePath).convert_alpha()
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []
    
    def draw(self, screen, initX, initY):
        x, y, w, h = self.scale(screen, initX, initY)
        image = transform.smoothscale(self.image, (w, h))
        screen.blit(image, (x, y))