import pygame
import scaler
import objects
import cv2
import numpy as np


class PicarSim:
    def __init__(
        self,
        picar,
        track,
        env_size=(200, 200),
        update_interval=0.01,
        graphics=True,
        speed_multiplier=1.0,
        graphics_perspective=None,
        perspective=None,
    ):
        self.picar = picar  # keep a pointer to picar for easy access
        self.env = [track, picar]
        self.env_size = env_size
        self.update_interval = update_interval
        self.graphics = graphics
        self.graphics_perspective = graphics_perspective
        self.speed_multiplier = speed_multiplier
        self.perspective = perspective

        self.add_track_to_env(track)  # add as obstacles to get state

        if graphics:
            self.framerate = 1 / update_interval * speed_multiplier
            pygame.init()
            self.display = pygame.display.set_mode(scaler.scale_coords(env_size))
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
                    track_objects.append(objects.TrackMaterial(center))

        self.add_objects(track_objects)
        print(f"Converted track image to {len(track_objects)} obstacles")

    def add_objects(self, new_objects):
        self.env.extend(new_objects)

    def random_picar_position(self):
        self.picar.center = np.array(
            [np.random.rand() * 300 - 150, np.random.rand() * 200 - 100]
        )
        self.picar.angle = np.random.randint(0, 360)

    def random_obstacle_region(self, *rects):
        num_obstacles = np.random.randint(1, 8)  # create variance between simulations

        for rect in rects:
            rx, ry, rw, rh = rect
            for _ in range(num_obstacles):
                x = np.random.randint(rx, rx + rw)
                y = np.random.randint(ry, ry + rh)
                self.add_objects([objects.Obstacle(center=(x, y))])

    def set_perspective(self, perspective: objects.SimulatorObject):
        self.perspective = perspective

    def update_env(self, dt):
        for obj in self.env:
            obj.update(dt, self.env)

    def render_env(self):
        # clear display
        self.display.fill((255, 255, 255))

        for obj in self.env:
            if obj == self.picar or obj.__class__.__name__ == "TrackMaterial":
                continue
            obj.render(self.display, self.perspective)

        # render picar at end to make sure it's on top
        self.picar.render(self.display, self.perspective)

        # refresh display with new render
        pygame.display.update()

    def loop(self):
        while True:
            self.update_env(self.update_interval * self.speed_multiplier)

            if self.graphics:
                # check for window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                self.render_env()

                self.clock.tick(self.framerate)
