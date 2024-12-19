
from pygame import draw, MOUSEBUTTONDOWN
from screenObject import ScreenObject
from textBox import TextBox


class Button(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, text:str="", color:tuple=(255, 255, 0), connection:list=[], disabled:bool=False, centerText:bool=True):
        super().__init__(name, posX, posY)
        self.size = self.toVector((width, height))
        self.text = text
        self.color = color
        self.connection = connection
        self.connection.append(self)
        self.disabled = disabled
        self.centerText = centerText
        if self.text:
            self.addChild(TextBox(self.name+"text", 0, 0, self.text, center=centerText))


    def draw(self, screen, initX:int, initY:int):
        self.rect = draw.rect(screen, self.color, (self.scale(screen, initX, initY)), 0)

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if not self.disabled and not self.hidden:
                    return self.connection

    def setText(self, text):
        self.getChild(self.name + "text").setText(text)
