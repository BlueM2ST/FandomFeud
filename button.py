
from pygame import Rect, font, draw

font.init()
font = font.Font(None, 24)


class Button:
    def __init__(self, posX:int, posY:int, width:int, height:int, text:str="", color:tuple=(255, 255, 0)):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.rect = Rect(posX, posY, width, height)


    def draw(self, screen, initX, initY):
        # scale with screen size
        x = self.posX * (screen.get_width() / initX)
        y = self.posY * (screen.get_height() / initY)
        w = self.width * (screen.get_width() / initX)
        h = self.height * (screen.get_height() / initY)
        # draw button background
        self.rect = draw.rect(screen, self.color, (x, y, w, h), 0)
        # if text, draw text on top of background
        if self.text:
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=(w*1.5, h*1.5)))


    # call this when the button is pressed
    def onClick(self):
        print("clicked")