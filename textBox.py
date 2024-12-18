
from pygame import font, time
from screenObject import ScreenObject

font.init()
font = font.Font(None, 24)


class TextBox(ScreenObject):
    def __init__(self, name:str, posX:int, posY:int, text:str="", center:bool=True, padding:int=0):
        super().__init__(name, posX, posY)
        self.text = font.render(text, True, (0, 0, 0))
        self.center = center
        self.padding = padding


    def draw(self, screen, initX:int, initY:int):
        # scale with screen size
        x, y, w, h = self.scale(screen, initX, initY)
        # if text, draw text on top of background
        textRect = (x, y)
        if self.center:
            textRect = self.text.get_rect(center = (x + self.getParent().scaleSize.x /2, y + self.getParent().scaleSize.y /2))
        screen.blit(self.text, (textRect[0] + self.padding, textRect[1] + self.padding))
    
    def setText(self, text):
        self.text = font.render(text, True, (0, 0, 0))
