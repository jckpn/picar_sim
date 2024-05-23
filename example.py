from picar_sim import PicarSim, objects
import pygame


class SimpleKeyboardController:
    def predict(self, picar, env):
        angle, speed = 90, 0  # defaults

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed = 35
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            angle = 55
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            angle = 125

        return angle, speed


picar = objects.Picar(controller=SimpleKeyboardController())
track = objects.Track(image_path="track_oval.png")
obstacles = [
    objects.Obstacle(center=(50, 25)),
    objects.Obstacle(center=(-100, 0)),
]

sim = PicarSim(
    picar,
    track,
    obstacles,  # add obstacles here
    view_size=(350, 200),  # use None for no graphics
    speed_multiplier=1,
    follow_picar=False,
)

sim.start_loop()
