import scenes
import controllers


# TODO: current problem is, the model learns too many different things and averages them
# out e.g. at a junction the average of the training data is to go straight need a way
# to encourage the model to take one or the other
# 
# I'm pretty sure using recurrent connections would solve it so it can see past
# decisions or a transformer model
#
# I'm also thinking:
# - several models for steering 
# - with an overlooking model (could be manual, even a bunch of if statements might
#   work) which controls throttle and decides which steering model to use e.g. if it
#   sees an obstacle, no model / throttle 0, if it sees a junction with a left turn, use
#   left turn model
#
# this would also potentially solve the issue of averaging out decisions


def main():
    sim = scenes.Scene1(
        # controller=controllers.GridNeuralController(),
        controller=controllers.MouseController(),  # to capture training data
        speed_multiplier=1.0,
    )
    sim.random_picar_position()

    sim.set_perspective(sim.picar)  # makes manual driving easier
    sim.loop()


if __name__ == "__main__":
    main()
