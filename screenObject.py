

# base class for all objects that show on the screen
class ScreenObject:
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.children = []
        self.parent = None
        self.nodes = []


    def draw(self, screen, initX:int, initY:int):
        # scale position and size with screen size
        x, y, w, h = self.scale(screen, initX, initY)
    

    # scale the position and dimensions based on original positioning and new screen sizes
    def scale(self, screen, initX:int, initY:int):
        x = self.posX * (screen.get_width() / initX)
        y = self.posY * (screen.get_height() / initY)
        w = self.width * (screen.get_width() / initX)
        h = self.height * (screen.get_height() / initY)
        return (x, y, w, h)


    # call this when the object is pressed
    def onClick(self):
        # return the connected function call as string, as well as a ref to this button
        return []

    def addChild(self, node):
        self.getChildren().append(node)
        node.parent = self
    
    def getChildren(self):
        return self.children
    
    def getParent(self):
        return self.parent

    def free(self):
        for child in self.getChildren():
            child.free()
        self.parent.getChildren().remove(self)
    
    def getAllChilden(self):
        self.iterTree(self)
        nodes = self.nodes
        self.nodes = []
        return nodes

    # return an array of all child items
    def iterTree(self, fromNode) -> list:
        for node in fromNode.getChildren():
            self.nodes.append(node)
            if node.getChildren() and node != fromNode:
                self.iterTree(node)
