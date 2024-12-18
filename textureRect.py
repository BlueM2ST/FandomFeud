

from pygame import image, transform
from screenObject import ScreenObject


class TextureRect(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, imagePath:str):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.image = image.load(imagePath).convert_alpha()
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []
    
    def draw(self, screen, initX, initY):
        x, y, w, h = self.scale(screen, initX, initY)
        image = transform.smoothscale(self.image, (w, h))
        screen.blit(image, (x, y))