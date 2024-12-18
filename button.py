
from pygame import draw
from screenObject import ScreenObject
from textBox import TextBox


class Button(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, text:str="", color:tuple=(255, 255, 0), connection:list=[], disabled:bool=False):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.connection = connection
        self.connection.append(self)
        self.disabled = disabled
        self.hidden = False
        self.children = []
        self.parent = None
        self.nodes = []
        if self.text:
            self.addChild(TextBox(self.name+"text", posX, posY, self.text))


    def draw(self, screen, initX:int, initY:int):
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)

    # call this when the button is pressed
    def onClick(self):
        # return the connected function call as string, as well as a ref to this button
        if not self.disabled:
            return self.connection

    def setText(self, text):
        self.getChild(self.name + "text").setText(text)
