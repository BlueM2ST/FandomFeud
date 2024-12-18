
from screenObject import ScreenObject


class Container(ScreenObject):
    def __init__(self, name:str, posX:int=0, posY:int=0):
        self.name = name
        self.pos = self.toVector((posX, posY))
        self.relPos = self.toVector((0, 0))
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []
    
