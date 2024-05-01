import controllers.grid_state
import scenes
import controllers


TRAINING = False


def main():
    grid_params = {
        "cell_size": 2,
        "range": 60,
        "camera_offset": 15,  # ~5cm from front, ~15cm from wheels (= sprite center)
    }

    sim = scenes.Scene7(
        controller=controllers.MoeController(**grid_params, smoothing=0.0)
        if not TRAINING
        else controllers.GridCaptureController(**grid_params),
        speed_multiplier=1,
        controller_interval=0.05,
        env_size=(150, 150) if TRAINING else (350, 200),
    )

    if TRAINING:
        sim.set_perspective(sim.picar)
        sim.random_picar_position()

    sim.picar.max_speed = 30 if TRAINING else 100  # plaid mode

    print(sim.picar.controller_interval)
    sim.loop()


if __name__ == "__main__":
    main()
