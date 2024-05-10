import pygame
import picar_sim.scaler as scaler
import objects
import cv2
import numpy as np


class PicarSim:
    def __init__(
        self,
        track,
        env_size=(350, 200),  # viewable area in cm
        controller=None,
        controller_interval=0.1,
        update_interval=0.01,
        graphics=True,
        speed_multiplier=1,
        graphics_perspective=None,
    ):
        self.picar = objects.Picar(controller)  # keep a pointer to picar for easy access
        self.env = [track, self.picar]
        self.env_size = env_size
        self.update_interval = update_interval
        self.graphics = graphics
        self.graphics_perspective = graphics_perspective
        self.speed_multiplier = speed_multiplier

        self.cvt_track_to_obstacles(track)  # track -> mini obstacles for state capture
        # keep the track in environment so it can still be rendered

        if graphics:
            self.framerate = 1 / update_interval * speed_multiplier
            pygame.init()
            self.display = pygame.display.set_mode(scaler.scale_coords(env_size))
            self.clock = pygame.time.Clock()

    def cvt_track_to_obstacles(self, track, res=1, threshold_color=180):
        # iterate over track image and add objects where there are pixels
        track_objects = []

        # turn track to grid, then iterate over grid to add obstacle objects
        track_grid = cv2.resize(
            cv2.imread(track.image_path, cv2.IMREAD_GRAYSCALE),
            np.array(track.size / res, dtype=int),
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

    def add_random_obstacles(self, x1, y1, x2, y2):
        # for obj in self.env:
        #     if obj.__class__.__name__ == "Obstacle":
        #         self.env.remove(obj)

        num_obstacles = np.random.randint(1, 4)  # some variance between simulations
        obstacles = []
        for _ in range(num_obstacles):
            x, y = np.random.randint(x1, x2), np.random.randint(y1, y2)
            obstacles.append(objects.Obstacle(center=(x, y)))
            print(f"adding obstacle at {x}, {y}")
        self.add_objects(obstacles)

    def add_objects(self, new_objects):
        self.env.extend(new_objects)

    def random_picar_position(self):
        self.picar.center = np.array(
            [np.random.rand() * 200 - 100, np.random.rand() * 100 - 50]
        )
        self.picar.direction = np.random.randint(0, 360)

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

    def start_loop(self):
        while True:
            for _ in range(self.speed_multiplier):
                self.update_env(self.update_interval)

            if self.graphics:
                # check for window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                self.render_env()
                self.clock.tick(self.framerate)
