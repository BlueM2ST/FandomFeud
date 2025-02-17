
from .node import ScreenObject

class Container(ScreenObject):
    def __init__(self, name:str, posX:int=0, posY:int=0):
        super().__init__(name, posX, posY)
    
