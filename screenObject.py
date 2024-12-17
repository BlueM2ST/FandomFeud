

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


    # called when a node is added to the tree
    def addedToTree(self):
        pass


    def addChild(self, node):
        self.getChildren().append(node)
        node.parent = self
        node.addedToTree()
    
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
    
    def getAllChilden(self):
        self.iterTree(self)
        nodes = self.nodes
        self.nodes = []
        return nodes

    # populate an array of all child items recursively
    def iterTree(self, fromNode):
        for node in fromNode.getChildren():
            self.nodes.append(node)
            if node.getChildren():
                self.iterTree(node)
