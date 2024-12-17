
from pygame import Rect, font, draw
from screenObject import ScreenObject

font.init()
font = font.Font(None, 24)


class TextBox(ScreenObject):
    def __init__(self, name:str, width:int, height:int, text:str=""):
        self.name = name
        self.posX = 0
        self.posY = 0
        self.width = width
        self.height = height
        self.text = text


    def draw(self, screen, initX, initY):
        # scale with screen size
        x, y, w, h = self.scale(screen, initX, initY)
        # if text, draw text on top of background
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=(w*1.5, h*1.5)))


    def onClick(self):
        return []