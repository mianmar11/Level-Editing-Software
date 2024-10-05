import pygame as py

class Camera:
    def __init__(self, pos):
        self.pos = py.math.Vector2(pos)
        self.vel = py.math.Vector2(0, 0)

        self.holding_space = False
        self.holding_button = False # mouse button
        self.dx, self.dy = 0, 0
    
    def keydown(self, key):
        if key == py.K_SPACE:
            self.holding_space = True
            # py.mouse.set_cursor(9)      
    
    def keyup(self, key):
        if key == py.K_SPACE:
            self.holding_space = False
            # py.mouse.set_cursor(0)

    def set_delta_values(self):
        self.dx = self.pos.x - self.mpos[0]
        self.dy = self.pos.y - self.mpos[1]

    def move(self):
        if self.holding_button:
            self.pos.xy = self.mpos[0] + self.dx, self.mpos[1] + self.dy

    def update(self, mpos):
        self.mpos = mpos