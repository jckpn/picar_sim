import pygame
import objects
import controllers
from utils import scale_coords


TARGET_FPS = 60
SPEED_MULTIPLIER = 1.5
ENV_SIZE = (350, 200)

track = objects.tracks.Oval()
picar = objects.Picar()
wood = objects.obstacles.Wood(center=(0, 80))
obstacles = [
    objects.obstacles.Wood(center=(-40, 20)),
    objects.obstacles.Wood(center=(40, 20)),
    wood,
]
environment = [track, picar, *obstacles]
perspective = picar


pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode(size=scale_coords(ENV_SIZE))
controller = controllers.KeyboardController()


def sim_loop():
    # clear display
    display.fill((255, 255, 255))

    # render environment
    for obj in environment:
        obj.render(display, perspective)

    # update picar controls
    picar.get_state(display)
    dt = clock.get_time() / 1000 * SPEED_MULTIPLIER
    steer, throttle = controller.get_controls()
    picar.set_controls(steer, throttle)
    picar.update(dt)

    pygame.display.update()
    clock.tick(TARGET_FPS)


def main():
    while True:
        sim_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == "__main__":
    main()
