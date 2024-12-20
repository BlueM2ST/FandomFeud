
from pygame.math import Vector2

class Vector2D(Vector2):
    def __init__(self, vector:tuple):
        self.vector = vector
        self.x = vector[0]
        self.y = vector[1]
    
    def __repr__(self):
        return self.vector

    def __str__(self):
        return str(self.vector)
