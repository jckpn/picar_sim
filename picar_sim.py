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
        env_size,  # viewable window size
        update_interval=0.01,
        graphics=True,
        speed_multiplier=1,
        graphics_perspective=None,
        perspective=None,
        obstacle_regions=[],
    ):
        self.picar = picar  # keep a pointer to picar for easy access
        self.env = [track, picar]
        self.env_size = env_size
        self.update_interval = update_interval
        self.graphics = graphics
        self.graphics_perspective = graphics_perspective
        self.speed_multiplier = speed_multiplier
        self.perspective = perspective
        self.obstacle_regions = []

        self.cvt_track_to_obstacles(track)  # add as obstacles to get state

        if graphics:
            self.framerate = 1 / update_interval * speed_multiplier
            pygame.init()
            self.display = pygame.display.set_mode(scaler.scale_coords(env_size))
            self.clock = pygame.time.Clock()

    def cvt_track_to_obstacles(self, track, res=1, threshold_color=245):
        # iterate over track image and add objects where there are pixels
        track_objects = []

        # turn track to grid, then iterate over grid to add obstacle objects
        track_grid = cv2.resize(
            cv2.imread(track.image_path, cv2.IMREAD_GRAYSCALE),
            track.size // res,
        )

        for y in range(track_grid.shape[0]):
            for x in range(track_grid.shape[1]):
                if track_grid[y, x] < threshold_color:
                    # offset positions to match track object
                    center = np.array([x, y]) * res
                    center -= track.size // 2
                    track_objects.append(objects.TrackMaterial(center))

        self.add_objects(track_objects)
        print(f"Converted track image to {len(track_objects)} obstacles")

    def reset_objects(self):
        for obj in self.env:
            if obj.__class__.__name__ == "Obstacle":
                self.env.remove(obj)

    def add_objects(self, new_objects):
        self.env.extend(new_objects)

    def random_picar_position(self):
        self.picar.center = np.array(
            [np.random.rand() * 200 - 100, np.random.rand() * 100 - 50]
        )
        self.picar.angle = np.random.randint(0, 360)

    def fill_obstacle_regions(self):
        num_obstacles = np.random.randint(1, 4)  # some variance between simulations

        for rect in self.obstacle_regions:
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
            if obj == self.picar:  # render picar at end to make sure it's on top
                continue
            obj.render(self.display, self.perspective)
        self.picar.render(self.display, self.perspective)

        # refresh display with new render
        pygame.display.update()

    def loop(self):
        while True:
            for _ in range(self.speed_multiplier):
                self.update_env(self.update_interval)

            if self.graphics:
                # check for window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # randomly shuffle obstacles if the scene has them
                if np.random.rand() < self.update_interval * 0.2:  # every ~5s
                    self.reset_objects()

                    if 0.5:
                        self.fill_obstacle_regions()

                self.render_env()
                self.clock.tick(self.framerate)
