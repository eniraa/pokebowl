import math

from game import Game, Scene
import pygame
from pygame.locals import K_RETURN


class StartScene(Scene):
    def __init__(self):
        self.frame = 0

        self.anim = [
            pygame.transform.scale(
                pygame.image.load(f"pokebowl/assets/intro/wild{i}.png"), (512, 288)
            )
            for i in range(1, 226)
        ]
        self.logo = pygame.transform.scale(
            pygame.image.load("pokebowl/assets/poke.png"), (256, 94)
        )
        self.font = pygame.font.Font("pokebowl/assets/fonts/pixel.ttf", 16)

        pygame.mixer.music.load("pokebowl/assets/music/start.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)

    def update(self, game: Game):
        self.frame += 1
        game.screen.blit(self.anim[self.frame // 2 % 225], (0, 32))

        logo = pygame.transform.rotate(
            self.logo, 4 * math.sin(self.frame * math.pi / 128)
        )
        game.screen.blit(logo, logo.get_rect(center=(game.screen.get_width() // 2, 96)))

        prompt = self.font.render(
            "press [return] to continue",
            False,
            (int(64 * math.sin(self.frame * math.pi / 64) + 191),) * 3,
        )

        # hardcoded height, screen size *shouldn't* change
        game.screen.blit(
            prompt, prompt.get_rect(center=(game.screen.get_width() // 2, 352))
        )

        if pygame.key.get_pressed()[K_RETURN]:
            from test import MovementScene

            game.switch_scene(MovementScene)  # change later

    def __del__(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
