from objects.tracks import OvalTrack
from shared.model import MoeController
from controllers import GridCaptureController, MouseController


# idk


default_cfg = {
    "track": OvalTrack(),
    "controller": GoslingController(),
    "controller_interval": 0.1,  # simulate real-world delay
    "env_size": (300, 200),
    "graphics_scale": 4,
    "speed_multiplier": 2,
    "follow_picar": False,
}

capture_cfg = {
    "track": OvalTrack(),
    "controller": CaptureController(),
    "controller_interval": 0.01,  # capture more data
    "env_size": (150, 150),
    "graphics_scale": 4,
    "speed_multiplier": 1,
    "follow_picar": True,
}

PicarSim(**default_cfg).start_loop()