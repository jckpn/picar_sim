import pygame
import objects
import controllers
from utils import scale_coords


ENV_SIZE = (350, 200)

track = objects.tracks.Oval()
picar = objects.Picar(center=(0, -45), angle=-90)
wood = objects.obstacles.Wood(center=(60, 80), size=(5, 5))
obstacles = [
    wood,
]
environment = [track, picar, *obstacles]
perspective = picar


def sim_loop(
    controller, display=None, clock=None, dt=0.1, speed_multiplier=1.0, max_fps=60
):
    # update picar controls
    dt = clock.get_time() / 1000 * speed_multiplier if display and clock else dt

    throttle, steer = controller.get_controls(dt)
    picar.set_controls(throttle, steer)
    picar.update(dt)

    if display and clock:  # clear display and render environment
        display.fill((255, 255, 255))
        for obj in environment:
            obj.render(display, perspective)

        pygame.display.update()
        clock.tick(max_fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def run_with_graphics():
    pygame.init()

    controller = controllers.KeyboardController()
    display = pygame.display.set_mode(scale_coords(ENV_SIZE))
    clock = pygame.time.Clock()

    while True:
        sim_loop(controller, display, clock, speed_multiplier=2.0)


if __name__ == "__main__":
    run_with_graphics()
