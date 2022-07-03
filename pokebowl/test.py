from typing import Sequence

from game import Scene
import pygame
from pygame.locals import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP

# constants
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 550

TILE_SIZE = 50
WIDTH = SCREEN_WIDTH // TILE_SIZE
HEIGHT = SCREEN_HEIGHT // TILE_SIZE


class Player(pygame.sprite.Sprite):
    """
    A player.
    Has values surf, rect
    """

    def __init__(self, x=TILE_SIZE * 7, y=TILE_SIZE * 5):
        super(Player, self).__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surf.fill((200, 50, 30))
        self.rect: pygame.rect.Rect = self.surf.get_rect()
        # Maybe something better?
        self.rect.update(x, y, TILE_SIZE, TILE_SIZE)


class Tile(pygame.sprite.Sprite):
    """
    A tile.
    Temporary implementation.
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int = TILE_SIZE,
        h: int = TILE_SIZE,
        color: pygame.Color = pygame.Color(0, 0, 0),
    ):
        """
        Temporary implementation. Method signature will change.
        """
        super(Tile, self).__init__()
        self.color = color
        self.surf = pygame.Surface((w, h))
        self.surf.fill(color)
        self.rect: pygame.rect.Rect = self.surf.get_rect()
        self.rect.update(x, y, w, h)

        self.w = w
        self.h = h


class Camera:
    MOVE_TIME = 30

    def __init__(self, x: int, y: int, w: int = WIDTH, h: int = HEIGHT):
        """
        Make a new camera
        x: x-coordinate of the TOP-LEFT tile
        y: y-coordinate of the TOP-LEFT tile
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # State:
        #   state = 0 => Not moving
        #   state in 1..MOVE_TIME => Moving (progress)
        self.state = 0
        self.old_x = x
        self.old_y = y

    def move(self, dx, dy):
        """
        Move the camera
        dx: amount to move in the x direction (should be 1 or -1)
        dy: amount to move in the y direction (should be 1 or -1)
        """
        self.x = self.x + dx
        self.y = self.y + dy
        self.state = 1

    def update(self, pressed_keys: Sequence[bool]):
        if self.state == 0:
            # handle key presses
            if pressed_keys[K_UP]:
                self.move(0, -1)
            elif pressed_keys[K_DOWN]:
                self.move(0, 1)
            elif pressed_keys[K_LEFT]:
                self.move(-1, 0)
            elif pressed_keys[K_RIGHT]:
                self.move(1, 0)
        elif self.state >= self.MOVE_TIME:
            self.state = 0
            self.old_x = self.x
            self.old_y = self.y
        elif self.state in range(1, self.MOVE_TIME + 1):
            self.state += 1

    def get_draw_tiles(self, map: Sequence[Sequence[Tile]]) -> Sequence[Sequence[Tile]]:
        """
        WILL CAUSE ISSUES if map is not rectangular or `len(map) == 0`
        map should be represented like this:
        [[ A B C D E ]
        [ A B C D E ]
        [ A B C D E ]]
        so accessing the tile at (x, y) = map[y][x]

        returns all `Tile`s that need to be drawn
        """
        # Not moving
        if self.state == 0:
            y_min = max(self.y, 0)
            y_max = min(self.y + self.h, len(map) - 1)
            assert y_max >= y_min
            x_min = max(self.x, 0)
            x_max = min(self.x + self.w, len(map[y_min]) - 1)
            # Section out y's from y_min to y_max and x's from x_min to x_max inclusive
            return [i[x_min : x_max + 1] for i in map[y_min : y_max + 1]]
        elif self.state in range(1, self.MOVE_TIME + 1):
            # Update tile positions
            assert len(map) > 0
            y_min = max(self.y - 1, 0)
            y_max = min(self.y + self.h + 1, len(map) - 1)
            x_min = max(self.x - 1, 0)
            x_max = min(self.x + self.w + 1, len(map[y_min]) - 1)
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    x_start = (x - self.old_x) * TILE_SIZE
                    x_end = (x - self.x) * TILE_SIZE
                    y_start = (y - self.old_y) * TILE_SIZE
                    y_end = (y - self.y) * TILE_SIZE
                    # Hopefully doesn't break anything
                    tile = map[y][x]
                    tile.rect.update(
                        # trying to make a lerp
                        x_start + int(self.state / self.MOVE_TIME * (x_end - x_start)),
                        y_start + int(self.state / self.MOVE_TIME * (y_end - y_start)),
                        tile.w,
                        tile.h,
                    )
            # Give back all the tiles
            return [i[x_min : x_max + 1] for i in map[y_min : y_max + 1]]
        else:
            # For functionality only
            return [[]]


class MovementScene(Scene):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.player = Player()
        self.camera = Camera(0, 0)

        # Make map
        self.map: Sequence[Sequence[Tile]] = []
        for y in range(0, HEIGHT + 3):
            map_row = []
            for x in range(0, WIDTH + 3):
                color = (
                    pygame.Color(200, 200, 200)
                    if (x + y) % 2 == 0
                    else pygame.Color(150, 150, 150)
                )
                map_row.append(Tile(x * TILE_SIZE, y * TILE_SIZE, color=color))
            self.map.append(map_row)

    def update(self, game):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:
            game.switch_scene(None)
        self.camera.update(pressed_keys)

        self.screen.fill((255, 255, 255))
        # show map/environment
        # (random hard-coded solution)
        shown = self.camera.get_draw_tiles(self.map)
        for row in shown:
            for tile in row:
                self.screen.blit(tile.surf, tile.rect)

        # Put player on screen
        self.screen.blit(self.player.surf, self.player.rect)
