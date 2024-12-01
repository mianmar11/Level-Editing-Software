import pygame as py

from tile import *
from camera import Camera
from ui.cursor import CursorManager

class Editor:
    def __init__(self, window):
        self.window = window
        self.tile_map_manager = TileMapManager(window)
        self.camera = Camera((0, 0))
        self.cursor = CursorManager()

        self.mpos = [0, 0]
        self.mbuttons = [0, 0, 0]

    def draw(self):
        pass

    def update(self):
        self.camera.update(self.mpos)
        self.tile_map_manager.update(self.camera.pos)
        if self.cursor.mode == 'default':
            self.tile_map_manager.button_control(self.mbuttons)
        
    def update_events(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            self.cursor.mouse_down(event.button)
            if event.button == py.BUTTON_LEFT:
                self.mbuttons[0] = True
                self.camera.holding_button = True
                self.camera.set_delta_values()
            elif event.button == py.BUTTON_MIDDLE:
                self.mbuttons[1] = True
            elif event.button == py.BUTTON_RIGHT:
                self.mbuttons[2] = True
        elif event.type == py.MOUSEBUTTONUP:
            self.cursor.mouse_up(event.button)
            if event.button == py.BUTTON_LEFT:
                self.mbuttons[0] = False
                self.camera.holding_button = False
            elif event.button == py.BUTTON_MIDDLE:
                self.mbuttons[1] = False
            elif event.button == py.BUTTON_RIGHT:
                self.mbuttons[2] = False
        elif event.type == py.MOUSEWHEEL:
            self.tile_map_manager.mouse_wheel(event.y)
        
        if event.type == py.MOUSEMOTION:
            self.mpos = py.mouse.get_pos()
            # if self.camera.holding_button and self.camera.holding_space:
            if self.cursor.mode == 'move':
                self.camera.move()
            self.tile_map_manager.update_pos(self.mpos, self.camera.pos)

        if event.type == py.KEYDOWN:
            self.camera.keydown(event.key)
            self.cursor.keydown(event.key)
            
            if self.camera.holding_space == False:
                self.tile_map_manager.keyboard_down(event.key)
        elif event.type == py.KEYUP:
            self.camera.keyup(event.key)
            self.cursor.keyup(event.key)
