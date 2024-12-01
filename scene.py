import pygame as py

class Scene:
    def __init__(self, size:list|tuple):
        self.surf = py.Surface(size)
        self.surf_width, self.surf_height = self.surf.get_size()
    
    def render(self, draw_surf, camera_pos):
        draw_surf.blit(self.surf, camera_pos)
    