import pygame
import objects
from controllers import KeyboardController, LaneController
from utils import scale_coords
from constants import ENV_SIZE, TARGET_FPS, SPEED_MULTIPLIER


track = objects.tracks.Figure8()
picar = objects.Picar(center=(0, -20))
environment = [track, picar, objects.obstacles.Wood()]
perspective = picar


pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode(scale_coords(ENV_SIZE))
controller = LaneController(display, picar)


def simulation_loop():
    # clear display
    display.fill((255, 255, 255))

    # update and render objects
    dt = clock.get_time() / 1000 * SPEED_MULTIPLIER

    for obj in environment:
        obj.update(dt)
        obj.render(display, perspective)

    # update display
    pygame.display.update()

    # update picar controls
    steer, throttle = controller.get_controls(dt)
    picar.set_controls(steer, throttle)

    # wait for next frame if needed
    clock.tick(TARGET_FPS)


def display_info():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Speed: {picar.throttle:.2f}", True, (0, 0, 0))

    display.blit(text, (10, 10))


def main():
    while True:
        simulation_loop()
        display_info()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == "__main__":
    main()
