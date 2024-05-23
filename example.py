from picar_sim import PicarSim, objects
import pygame


class SimpleKeyboardController:
    def predict(self, picar, env):
        angle, speed = 90, 0  # defaults

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed = 35
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            angle = 50
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            angle = 130

        return angle, speed


sim = PicarSim(
    picar=objects.Picar(controller=SimpleKeyboardController()),
    track=objects.Track(image_path="track_oval.png"),
    obstacles=[],  # add obstacles here
    view_size=(300, 200),  # use None for no graphics
    speed_multiplier=2,
    follow_picar=False,
)

sim.start_loop()
