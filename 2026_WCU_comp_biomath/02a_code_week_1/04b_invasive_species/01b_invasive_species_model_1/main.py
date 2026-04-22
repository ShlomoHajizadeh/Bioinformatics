from core.simulation import Simulation


def main():
    sim = Simulation()
    sim.run()
    sim.save_all_plots()
    sim.save_animation()


if __name__ == "__main__":
    main()