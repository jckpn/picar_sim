import pygame
import os

from objects.environment import Environment
from objects.picar import Picar
from objects.track import Track
from objects.obstacles import WoodBlock
from controllers.controllers import KeyboardController, LaneController, CNNController
from utils import scale_coords

# get file path
main_dir = os.path.dirname(os.path.abspath(__file__))


# TODO: a lot of the object classes have similar properties/methods, refactor to base class?

env_width = 300
env_height = 200
display_width = env_width
display_height = env_height
target_fps = 60
speed_multiplier = 2

picar = Picar(image_path=main_dir + "/assets/picar.png")

track = Track(
    image_path=main_dir + "/assets/track_oval.png",
    center_x=env_width // 2,
    center_y=env_height // 2,
)

obstacles = [
    # WoodBlock(
    #     width=np.random.randint(5, 20),
    #     height=np.random.randint(5, 20),
    #     center_x=np.random.randint(0, env_width),
    #     center_y=np.random.randint(0, env_height),
    # )
    # for _ in range(10)
]

env = Environment(
    width=env_width,
    height=env_height,
    picar=picar,
    track=track,
    obstacles=obstacles,
)


perspective = None  # set none for fixed perspective
env.picar.display_x = display_width // 2
env.picar.display_y = display_height // 2
env.track.center_x = env.width // 2
env.track.center_y = env.height // 2

# randomise start position
# disabled as controllers not yet good enough for this..

# env.picar.direction = np.random.randint(0, 360)
# env.picar.center_x = np.random.randint(env.width // 5, env.width // 5 * 4)
# env.picar.center_y = np.random.randint(env.width // 5, env.height // 5 * 4)

# env.picar.direction = 90

# set pygame win pos https://stackoverflow.com/a/4155723
os.environ["SDL_VIDEO_WINDOW_POS"] = "100, 100"
os.environ["SDL_VIDEO_CENTERED"] = "0"

pygame.init()
clock = pygame.time.Clock()  # clock object to control frame rate
display_size = scale_coords(display_width, display_height)
display = pygame.display.set_mode(display_size)


# controller = KeyboardController()
controller = CNNController(
    display,
    env.picar,
    steer_model_path=main_dir + "/models/roadwarp-angle-32.h5",
    throttle_model_path=main_dir + "/models/roadwarp-speed-32.h5",
    display_view=True,
)


def sim_loop(dt):
    dt *= speed_multiplier

    env.update(dt)  # update environment

    env.render(
        display, perspective=env.picar
    )  # render from picar perspective for controller
    throttle, steer = controller.get_controls(dt)
    env.picar.set_controls(throttle, steer)

    # re-render from fixed perspective if needed
    if perspective is None:
        env.render(display, perspective=perspective)

    # also render picar velocity, steering etc.
    env.picar.render_extras(display)

    pygame.display.flip()  # update display
    clock.tick(target_fps)

    return clock.get_time() / 1000


if __name__ == "__main__":
    dt = 0
    sim_running = True
    while sim_running:
        dt = sim_loop(dt)

        # handle close window event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sim_running = False
