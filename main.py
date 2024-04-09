import scenes


def main():
    sim = scenes.Scene2()
    sim.set_perspective(sim.picar)  # optional, but makes driving easier
    sim.loop()


if __name__ == "__main__":
    main()
