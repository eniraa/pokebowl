from test import MovementScene

from game import Game

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


if __name__ == "__main__":
    game = Game()
    game.switch_scene(MovementScene)
    game.start(SCREEN_WIDTH, SCREEN_HEIGHT, 60)
