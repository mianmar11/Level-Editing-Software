import pygame as py
from editor import Editor


class APP:
    def __init__(self):
        self.SIZE = (1080, 720)
        self.screen = py.display.set_mode(self.SIZE)
        self.clock = py.time.Clock()

        self.running = True

        # delta time settings
        self.FPS = 1000
        self.delta_time_setting = 60

        self.main_editor = Editor(self.screen)
    
    def run_main_loop(self):
        while self.running:
            delta_time = self.get_delta_time()
            self.handle_events()
            # print(self.clock.get_fps())
            
            # update screen
            self.screen.fill((0, 0, 0))

            # update editor
            self.main_editor.update()

            # update pygame
            py.display.flip()


    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            
            self.main_editor.update_events(event)

    def get_delta_time(self):
        delta_time = self.clock.tick(self.FPS) / 1000.0
        delta_time *= self.delta_time_setting
        
        if delta_time > 3:
            delta_time = 3

        return delta_time


if __name__ == "__main__":
    app = APP()
    app.run_main_loop()
    py.quit()