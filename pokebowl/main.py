from game import Game
from scenes.start import StartScene

# constants
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 384


if __name__ == "__main__":
    game = Game()
    game.switch_scene(StartScene)
    game.start(SCREEN_WIDTH, SCREEN_HEIGHT, 60)
