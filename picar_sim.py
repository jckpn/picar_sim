import pygame
from utils import scale_coords


class PicarSim:
    def __init__(
        self,
        controller,
        picar,
        track,
        obstacles=[],
        env_size=(200, 200),
        update_rate=60,
        speed_multiplier=1.0,
    ):
        self.controller = controller
        self.picar = picar
        self.track = track
        self.obstacles = obstacles
        self.size = env_size
        self.update_rate = update_rate
        self.speed_multiplier = speed_multiplier

        self.perspective = self.picar

        pygame.init()
        self.display = pygame.display.set_mode(scale_coords(env_size))
        self.clock = pygame.time.Clock()

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def render(self):
        self.display.fill((255, 255, 255))
        for obj in [self.track, self.picar, *self.obstacles]:
            obj.render(self.display, self.perspective)
        pygame.display.update()
        self.clock.tick(self.update_rate * self.speed_multiplier)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        dt = 1 / self.update_rate

        throttle, steer = self.controller.get_controls(self.picar)
        self.picar.set_controls(throttle, steer)
        self.picar.update(dt)

    # def get_picar_view(display, view_size=(40, 40)):
    #     view_size = scale_coords(view_size)
    #     y_offset = scale_coords(10)

    #     view_rect = (
    #         display.get_width() // 2 - view_size[1] // 2,
    #         display.get_height() // 2 - y_offset - view_size[0],
    #         *view_size,
    #     )

    #     # capture rect and convert to cv2 image
    #     view_cap = display.subsurface(view_rect).copy()
    #     view_cap = pygame.surfarray.array3d(view_cap)
    #     view_cap = np.rot90(view_cap)
    #     view_cap = cv2.flip(view_cap, 0)
    #     view_cap = cv2.cvtColor(view_cap, cv2.COLOR_RGB2BGR)

    #     # show view
    #     cv2.imshow("view", view_cap)
    #     # pygame.draw.rect(display, (255, 0, 255), view_rect, 2)

    #     return view_cap
