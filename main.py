import controllers.grid_state
import scenes
import controllers


TRAINING = False
FOLLOW_PICAR = False


def main():
    grid_params = {
        "cell_size": 2,
        "range": 60,
        "camera_offset": 14,  # ~5cm from front, ~14cm from wheels (= sprite center)
    }

    sim = scenes.Scene4(
        controller=controllers.MoeController(**grid_params, smoothing=0.0)
        if not TRAINING
        else controllers.GridCaptureController(**grid_params),
        speed_multiplier=5 if not TRAINING else 1,
        controller_interval=0.05,
        env_size=(150, 150) if FOLLOW_PICAR else (350, 200),
    )

    # if TRAINING:
    #     sim.random_picar_position()
    # sim.set_perspective(sim.picar)  # makes manual driving easier

    if FOLLOW_PICAR:
        sim.set_perspective(sim.picar)

    print(sim.picar.controller_interval)
    sim.loop()


if __name__ == "__main__":
    main()
