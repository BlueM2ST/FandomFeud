

from pygame import MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE
from textBox import TextBox, draw


class Container(TextBox):
    def __init__(self, name:str, posX:int, posY:int, width:int, height:int, text:str="", center:bool=False, padding:int=0):
        super().__init__(name, posX, posY)
        self.size = self.toVector((width, height))
        self.scaleSize = self.toVector((0, 0))
        self.colorInactive = (100, 100, 100)
        self.colorActive = (150, 150, 150)
        self.colorCurrent = self.colorInactive
        self.active = False
    
    def draw(self, screen, initX:int, initY:int):
        self.rect = draw.rect(screen, self.colorCurrent, (self.scale(screen, initX, initY)), 0)

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
                self.renderText(self.text)
            
            