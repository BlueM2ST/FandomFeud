

from pygame import draw, MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE
from screenObject import ScreenObject
from colorRect import ColorRect
from textBox import TextBox


class TextEdit(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, text:str="", center:bool=False, padding:int=0):
        super().__init__(name, posX, posY)
        self.size = self.toVector((width, height))
        self.colorInactive = (100, 100, 100)
        self.colorActive = (150, 150, 150)
        self.colorCurrent = self.colorInactive
        self.active = False
        self.text = text
        self.rect = self.addChild(ColorRect(self.name + "rect", self.pos.x, self.pos.y, self.size.x, self.size.y, self.colorInactive))
        self.textBox = self.addChild(TextBox(self.name + "text", self.pos.x, self.pos.y, self.text))

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.colorCurrent = self.colorActive
            else:
                self.active = False
                self.colorCurrent = self.colorInactive
        elif event.type == KEYDOWN:
            if self.active:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.textBox.text = self.text
                self.textBox.renderedText = self.renderText(self.text)
            
            