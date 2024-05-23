import pygame
from .graphics_scaler import scale_coords


class PicarSim:
    def __init__(
        self,
        picar,
        track,
        obstacles=[],
        update_interval=0.01,  # dt to process each update, regardless of graphics
        view_size=(350, 200),  # viewable area in real-world cm
        speed_multiplier=1,
        follow_picar=False,
    ):
        self.view_size = view_size
        self.picar = picar  # keep pointer to picar for graphics perspective
        self.env = [picar, track, *obstacles]
        self.update_interval = update_interval

        self.graphics_perspective = self.picar if follow_picar else None
        self.speed_multiplier = speed_multiplier
        if view_size is not None:
            self.framerate = 1 / update_interval * speed_multiplier
            pygame.init()
            self.display = pygame.display.set_mode(scale_coords(view_size))
            self.clock = pygame.time.Clock()

    def add_object(self, obj):
        self.env.append(obj)

    def update_env(self, dt):
        for obj in self.env:
            obj.update(dt, self.env)

    def render_env(self):
        self.display.fill((255, 255, 255))  # remove last frame's blits

        for obj in self.env:
            if obj == self.picar:  # render picar at end to make sure it's on top
                continue
            obj.render(self.display, self.graphics_perspective)
        self.picar.render(self.display, self.graphics_perspective)

        pygame.display.update()  # display new graphics
        self.clock.tick(self.framerate)

    def start_loop(self):
        while True:
            for _ in range(self.speed_multiplier):
                self.update_env(self.update_interval)

            if self.view_size is not None:
                # check for window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                self.render_env()
