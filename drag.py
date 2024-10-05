import pygame as py
class APP:
    def __init__(self):
        self.SIZE = (1080, 720)
        self.screen = py.display.set_mode(self.SIZE)
        self.clock = py.time.Clock()

        self.running = True
        self.rect = py.Rect(0, 0, 64, 64)
        self.rect.center = [i/2 for i in self.SIZE]

        # delta time settings
        self.FPS = 60
        self.delta_time_setting = 60
        self.holding = False
        self.init_pos = []
        self.dx, self.dy = 0, 0
        self.final_pos = []
        self.moving = False

        self.scroll = [0, 0]

    def run_main_loop(self):
        while self.running:
            delta_time = self.get_delta_time()
            self.moving = False
            self.handle_events()
            
            # update screen
            self.screen.fill((0, 0, 0))
            py.draw.rect(self.screen, 'red', (self.rect.x + self.scroll[0], self.rect.y + self.scroll[1], self.rect.w, self.rect.h))

            self.mpos = py.mouse.get_pos()

            if self.holding:
                # self.rect.topleft = (self.mpos[0] + self.dx), self.mpos[1] + self.dy
                self.scroll[0] = self.mpos[0] + self.dx
                self.scroll[1] = self.mpos[1] + self.dy
            
            # update pygame
            py.display.flip()


    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            if event.type == py.MOUSEBUTTONDOWN:
                self.holding = True
                self.init_pos = self.mpos
                self.dx = self.scroll[0] - self.mpos[0]
                self.dy = self.scroll[1] - self.mpos[1]
            if event.type== py.MOUSEBUTTONUP:
                self.holding = False
            if event.type == py.MOUSEMOTION:
                self.moving = True

            
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