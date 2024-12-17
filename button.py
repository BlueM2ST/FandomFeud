
from pygame import draw
from screenObject import ScreenObject
from textBox import TextBox


class Button(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, text:str="", color:tuple=(255, 255, 0), connection:list=[]):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.connection = connection
        self.connection.append(self)
        self.textBox:TextBox
        if self.text:
            self.textBox = TextBox(self.name+"text", posX, posY, self.text)


    def draw(self, screen, initX:int, initY:int):
        # draw button background
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)
        # if text, draw text on top of background
        if self.text:
            self.textBox.draw(screen, initX, initY)


    # call this when the button is pressed
    def onClick(self):
        # return the connected function call as string, as well as a ref to this button
        return self.connection