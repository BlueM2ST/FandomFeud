

from pygame import Rect
from vector2d import Vector2D

# base class for all objects that show on the screen
class ScreenObject:
    def __init__(self, name:str, posX:int, posY:int):
        self.name = name
        self.pos = Vector2D((posX, posY))
        self.relPos = Vector2D((0,0))
        self.size = Vector2D((0,0))
        self.scaleSize = Vector2D((0,0))
        self.rect = Rect(0, 0, 0, 0)
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []
    
    def __repr__(self):
        return "{} : \"{}\"".format(self.__class__.__name__, self.name)

    def draw(self, screen, initX:int, initY:int):
        pass
    
    # scale the position and dimensions based on original positioning and new screen sizes
    def scale(self, screen, initX:int, initY:int):
        x = self.relPos.x * (screen.get_width() / initX)
        y = self.relPos.y * (screen.get_height() / initY)
        w = self.scaleSize.x = self.size.x * (screen.get_width() / initX)
        h = self.scaleSize.y = self.size.y * (screen.get_height() / initY)
        return (x, y, w, h)

    def toVector(self, vector:tuple):
        return Vector2D(vector)

    # call this when the object is pressed
    def onClick(self):
        # return the connected function call as string, as well as a ref to this object
        return []

    def hide(self):
        self.hidden = True
    
    def show(self):
        self.hidden = False

    # called when a node is added to the tree
    def addedToTree(self):
        pass

    def addChild(self, node):
        self.getChildren().append(node)
        node.parent = self
        node.setRelativePosition()
        node.addedToTree()
    
    # when a node is added as a child, inherit its position
    def setRelativePosition(self):
        self.relPos.x = self.getParent().relPos.x + self.pos.x
        self.relPos.y = self.getParent().relPos.y + self.pos.y
        for child in self.getAllChilden():
            child.setRelativePosition()
    
    def getChild(self, name:str):
        for child in self.getChildren():
            if child.name == name:
                return child
    
    def getChildren(self):
        return self.children
    
    def getParent(self):
        return self.parent

    # will also remove all children
    def free(self):
        for child in self.getChildren():
            child.free()
        try:
            self.parent.getChildren().remove(self)
        except ValueError:
            print("parent " + self.parent + "has no child " + self.name)
    
    # get all children recursively
    def getAllChilden(self):
        self.iterTree(self)
        nodes = self.nodes
        self.nodes = []
        return nodes

    # used in getAllChildren() for recursively getting children
    def iterTree(self, fromNode):
        for node in fromNode.getChildren():
            self.nodes.append(node)
            if node.getChildren():
                self.iterTree(node)
