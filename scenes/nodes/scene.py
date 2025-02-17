
from .node import Node

class Scene():
    def __init__(self, server=None):
        self.server = server
        self.root = Node(self.__class__.__name__, 0, 0)
    
    def __repr__(self):
        return self.__class__.__name__

    def create(self):
        pass

    def getRoot(self):
        return self.root

    def free(self):
        self.root.free()
    