import controllers.grid_state
import scenes
import controllers

# TODO:
# gating model which decides to:
# 1. stop/wait (immediately, or at intersection line if appropriate), or
# 2. follow track (always straight at junctions), or
# 3. always turn right at junctions, or
# 4. always turn left at junctions
# where these are each small, separate models to be trained


TRAINING = False
FOLLOW_PICAR = False


def main():
    grid_params = {
        "cell_size": 2,
        "range": 60,
        "camera_offset": 15,  # 5cm from front, 15cm from wheel = sim 'center'
    }

    sim = scenes.Scene4(
        controller=controllers.MoeController(**grid_params, smoothing=0.8)
        if not TRAINING
        else controllers.GridCaptureController(**grid_params),
        speed_multiplier=10 if not TRAINING else 1,
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
