
from pygame import mixer
from .screenObject import ScreenObject

mixer.init()

class AudioPlayer(ScreenObject):
    def __init__(self, name:str, posX:int=0, posY:int=0):
        super().__init__(name, posX, posY)
        self.audio = None

    def play(self, filePath:str):
        self.audio = mixer.Sound(filePath)
        self.audio.play()