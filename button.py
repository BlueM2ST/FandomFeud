
from pygame import MOUSEBUTTONDOWN
from colorRect import ColorRect
from textBox import TextBox


class Button(ColorRect):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, text:str="", color:tuple=(255, 255, 0), connection:list=[], disabled:bool=False, centerText:bool=True):
        super().__init__(name, posX, posY, width, height, color)
        self.connection = connection
        self.connection.append(self)
        self.disabled = disabled
        self.centerText = centerText
        self.textBox = self.addChild(TextBox("textbox", 0, 0, text, center=centerText))

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if not self.disabled and not self.hidden:
                    return self.connection

    def setText(self, text):
        self.textBox.setText(text)
    
    def getText(self):
        return self.textBox.getText()
