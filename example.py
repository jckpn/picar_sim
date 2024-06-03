from picar_sim import PicarSim, objects
from keyboard_controller import KeyboardController


PicarSim(
    picar=objects.Picar(controller=KeyboardController()),
    track=objects.Track(image_path="track_oval.png"),
    obstacles=[
        objects.Obstacle(center=(50, 25)),
        objects.Obstacle(center=(-100, 0)),
    ],
    view_size=(350, 200),  # use None for no graphics
    speed_multiplier=1,
    follow_picar=False,
).start_loop()
