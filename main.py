from objects.tracks import OvalTrack
from shared.model import MoeController
from controllers import GridCaptureController, MouseController


# idk


default_cfg = {
    "track": OvalTrack(),
    "controller": GoslingController(),
    "controller_interval": 0.1,  # simulate real-world delay
    "graphics_scale": 4,
    "speed_multiplier": 2,
    "follow_picar": False,
}

default_cfg = {
    "track": OvalTrack(),
    "controller": CaptureController(),
    "controller_interval": 0.01,  # capture more data
    "graphics_scale": 4,
    "speed_multiplier": 1,
    "follow_picar": True,
}

sim = PicarSim(**default_cfg)

sim.start_loop()


if __name__ == "__main__":
    main()
