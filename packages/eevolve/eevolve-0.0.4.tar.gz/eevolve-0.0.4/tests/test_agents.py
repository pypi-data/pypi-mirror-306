import numpy

import eevolve

game = eevolve.Game((128, 72), (1280, 720), "test", numpy.zeros((128, 72, 3)), 10)


def test() -> None:
    surface = numpy.full((5, 5, 3), (255, 255, 255))

    game.add_agents(10, eevolve.AgentGenerator.default(game, 10, surface=surface, size=(5, 5)))
    game.run()


if __name__ == '__main__':
    test()
