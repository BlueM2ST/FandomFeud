

from pygame import Rect, Vector2

# base class for all objects that show on the screen
class Node:
    def __init__(self, name:str, position:Vector2=Vector2(0,0)):
        self.name = name
        self.pos =  position
        self.relPos = Vector2(0, 0)
        self.size = Vector2(0,0)
        self.scaleSize = Vector2(0,0)
        self.rect = Rect(0, 0, 0, 0)
        self.hidden = False
        self.children = []
        self.parent = None
        self.allChildren = []
    
    def __repr__(self):
        return "{} : \"{}\"".format(self.__class__.__name__, self.name)

    def draw(self, screen, initX:int, initY:int):
        pass

    def handleEvent(self, event):
        return None
    
    # scale the position and dimensions based on original positioning and new screen sizes
    def scale(self, screen, initX:int, initY:int):
        x = self.relPos.x * (screen.get_width() / initX)
        y = self.relPos.y * (screen.get_height() / initY)
        w = self.scaleSize.x = self.size.x * (screen.get_width() / initX)
        h = self.scaleSize.y = self.size.y * (screen.get_height() / initY)
        return (x, y, w, h)

    def hide(self):
        self.hidden = True
        for child in self.getChildren():
            child.hide()
    
    def show(self):
        self.hidden = False
        for child in self.getChildren():
            child.show()

    # called when a node is added to the tree
    def addedToTree(self):
        pass

    def addChild(self, child):
        if child.parent:
            print("Warning: {} is already a child of {}".format(child, child.parent))
            return
        self.getChildren().append(child)
        child.parent = self
        child.setRelativePosition()
        child.updateAllChildren()
        child.addedToTree()
        return child
    
    def updateAllChildren(self):
        self.allChildren = []
        self.allChildren = self.getAllChilden()
        if self.parent:
            self.getParent().updateAllChildren()
    
    # when a node is added as a child, inherit its position
    def setRelativePosition(self):
        self.relPos.x = self.getParent().relPos.x + self.pos.x
        self.relPos.y = self.getParent().relPos.y + self.pos.y
        for child in self.getChildren():
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
            print("Parent {} has no child {}".format(self.parent.name, self.name))
    
    # get all children recursively
    def getAllChilden(self):
        self.iterTree(self)
        return self.allChildren

    # used in getAllChildren() for recursively getting children
    def iterTree(self, fromNode):
        for node in fromNode.getChildren():
            self.allChildren.append(node)
            if node.getChildren():
                self.iterTree(node)
