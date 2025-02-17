
from pygame import mixer, Vector2
from .node import Node

mixer.init()

class AudioPlayer(Node):
    def __init__(self, name:str, pos=Vector2(0,0), audio:str=None):
        super().__init__(name, pos)
        self.audio = audio

    def play(self, filePath:str):
        self.audio = mixer.Sound(filePath)
        self.audio.play()