

from pygame import MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE, Vector2
from .button import Button


class TextEdit(Button):
    def __init__(self, name:str, pos:Vector2, size:Vector2, colorInactive:tuple, colorActive:tuple, text:str="", connection:list=[], disabled:bool=False, centerText:bool=False):
        super().__init__(name, pos, size, text, colorInactive, connection, disabled, centerText)
        self.colorInactive = colorInactive
        self.colorActive = colorActive
        self.active = False

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.colorActive
            else:
                self.active = False
                self.color = self.colorInactive
        elif event.type == KEYDOWN:
            if self.active:
                if event.key == K_BACKSPACE:
                    self.textBox.text = self.textBox.text[:-1]
                else:
                    self.textBox.text += event.unicode
                self.textBox.renderedText = self.textBox.renderText()
            
            