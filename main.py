import scenes
import controllers


def main():
    sim = scenes.Scene2(
        controller=controllers.KeyboardController(),
        speed_multiplier=3.0,
    )

    while True:
        sim.loop()
        sim.render()


if __name__ == "__main__":
    main()
