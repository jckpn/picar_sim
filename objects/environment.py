class Environment:
    def __init__(self, picar, track, obstacles=[], width=350, height=210):
        self.width = width  # cm
        self.height = height

        self.picar = picar
        self.track = track
        self.obstacles = obstacles

    def update(self, delta_time):
        self.picar.update(delta_time)

    def render(self, display, perspective=None):
        display.fill((255, 255, 255))  # clear previous frame

        # render order: track -> obstacles -> picar
        self.track.render(display, perspective)
        for obstacle in self.obstacles:
            obstacle.render(display, perspective)
        self.picar.render(display, perspective)
        self.picar.render_extras(display)
