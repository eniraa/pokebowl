from typing import Sequence

from game import Game, Scene
import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((100, 100))
        self.surf.fill((255, 50, 30))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys: Sequence[bool]):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class TestScene(Scene):
    def __init__(self):
        self.player = Player()

    def update(self, game):
        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys)

        game.screen.fill((255, 255, 255))
        game.screen.blit(self.player.surf, self.player.rect)


if __name__ == "__main__":
    game = Game()
    game.switch_scene(TestScene)
    game.start(SCREEN_WIDTH, SCREEN_HEIGHT, 60)
