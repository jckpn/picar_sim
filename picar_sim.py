import pygame
from utils import scale_coords
from objects import SimulatorObject, obstacles
import cv2
import numpy as np


class PicarSim:
    def __init__(
        self,
        picar,
        track,
        env_size=(150, 150),
        update_interval=0.01,
        graphics=True,
        speed_multiplier=1.0,
        graphics_perspective=None,
    ):
        self.picar = picar  # keep a pointer to picar for easy access
        self.env = [picar]
        self.env_size = env_size
        self.update_interval = update_interval
        self.graphics = graphics
        self.graphics_perspective = graphics_perspective
        self.graphics_speed_multiplier = speed_multiplier

        self.add_track_to_env(track)

        if graphics:
            self.framerate = 1 / update_interval * speed_multiplier
            pygame.init()
            self.display = pygame.display.set_mode(scale_coords(env_size))
            self.clock = pygame.time.Clock()

    def add_track_to_env(self, track, res=1):
        # iterate over track image and add objects where there are pixels
        track_objects = []

        # resize so 1px = 1cm (or specified)
        track_image = cv2.imread(track.image_path, cv2.IMREAD_GRAYSCALE)
        track_image = cv2.resize(
            track_image,
            track.size // res,
            interpolation=cv2.INTER_AREA,
        )

        for y in range(track_image.shape[0]):
            for x in range(track_image.shape[1]):
                if track_image[y, x] < 200:
                    # offset positions to match track object
                    center = np.array([x, y]) * res
                    center -= track.size // 2
                    track_objects.append(obstacles.TrackMaterial(center))
                    print(f"Adding object at {x}, {y}")

        self.add_objects(track_objects)

        print(f"Added {len(track_objects)} track objects")

    def add_objects(self, new_objects):
        self.env.extend(new_objects)

    def set_perspective(self, perspective: SimulatorObject):
        self.perspective = perspective

    def update_env(self, dt):
        for obj in self.env:
            obj.update(dt, self.env)

    def render_env(self):
        # clear display
        self.display.fill((255, 255, 255))

        for obj in self.env:
            obj.render(self.display, self.perspective)

        # refresh display with new render
        pygame.display.update()

    def loop(self):
        while True:
            self.update_env(self.update_interval * self.graphics_speed_multiplier)

            if self.graphics:
                # check for window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                self.render_env()

                self.clock.tick(self.framerate)
