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
    grid_size = 25
    cell_size = 3.5
    grid_params = {
        "cell_size": cell_size,
        "range": grid_size * cell_size,
        "camera_offset": 5,  # MEASURED
    }

    sim = scenes.Scene7(
        controller=controllers.MoeController(**grid_params, smoothing=0.5),
        # controllers.GridDetController(**grid_params),
        # controllers.GridCaptureController(**grid_params),
        controller_interval=0.1 if not TRAINING else 0.01,
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
