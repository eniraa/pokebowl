from typing import Type

import pygame


class Scene:
    def update(self, game: "Game"):
        """Updates the scene"""
        raise NotImplementedError


class Game:
    def __init__(self):
        self.scene = None
        self.screen = None
        self.clock = None

    def switch_scene(self, scene: Type[Scene] | None):
        """Switches the scene."""
        del self.scene

        if scene is None:
            self.scene = None
        else:
            self.scene = scene()

    def start(self, width: int, height: int, framerate: int):
        """Starts the game. This blocks the program."""
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        while self.scene:
            self.clock.tick(framerate)
            self.scene.update(self)

            if pygame.event.peek(pygame.QUIT):
                self.switch_scene(None)

            pygame.display.flip()

        pygame.quit()
