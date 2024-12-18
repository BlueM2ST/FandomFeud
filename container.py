
from screenObject import ScreenObject


class Container(ScreenObject):
    def __init__(self, name:str):
        self.name = name
        self.children = []
        self.parent = None
        self.nodes = []