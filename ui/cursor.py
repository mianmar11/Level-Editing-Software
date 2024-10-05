import pygame as py

class CursorManager:
    def __init__(self):
        self.mbuttons = [False, False, False]
        self.holding_space = False
        self.mode = 'default'

    def mouse_down(self, button):
        if button == py.BUTTON_LEFT:
            self.mbuttons[0] = True

    def mouse_up(self, button):
        if button == py.BUTTON_LEFT:
            self.mbuttons[0] = False
            if self.holding_space == False:
                py.mouse.set_cursor(0)
                self.mode = 'default'

    def keydown(self, key):
        if key == py.K_SPACE:
            self.holding_space = True
            py.mouse.set_cursor(9)
            self.mode = 'move'

    def keyup(self, key):
        if key == py.K_SPACE:
            self.holding_space = False
            if self.mbuttons[0] == False:
                py.mouse.set_cursor(0)
                self.mode = 'default'
    
