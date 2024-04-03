import pygame
import objects
import controllers
from utils import scale_coords


ENV_SIZE = (350, 200)

track = objects.tracks.Oval()
picar = objects.Picar(center=(0, -45), angle=-90)
environment = [track, picar]
perspective = picar


def sim_loop(controller, display=None, clock=None, dt=0.1, max_fps=30):
    throttle, steer = controller.get_controls(picar)
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

    # controller = controllers.KeyboardController()
    controller = controllers.NeuroTargetController()
    controller.targets = [(-50, -50), (50, -50), (50, 50), (-50, 50)]
    display = pygame.display.set_mode(scale_coords(ENV_SIZE))
    clock = pygame.time.Clock()

    while True:
        sim_loop(controller, display, clock, dt=0.01, max_fps=100)


if __name__ == "__main__":
    run_with_graphics()
