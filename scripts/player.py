import pygame

from scripts.mob import Mob
from scripts.tilemap import Tilemap

class Player(Mob):
    """
    A class representing the player character in the game.

    Attributes:
        assets (dict[str, pygame.Surface]): Dictionary of assets for the player.
        movementInput (dict[str, bool]): Dictionary indicating the current movement input state.
        velocity (list[int]): List representing the current velocity of the player in pixels per frame.
    """
    def __init__(self, assets: dict[str, pygame.Surface], pos: list[int]) -> None:
        """
        Initialize the Player object.

        Args:
            assets (dict[str, pygame.Surface]): Dictionary of assets for the player.
        """
        super().__init__()
        self.pos: list[int] = pos
        self.assets: dict[str, pygame.Surface] = assets
        self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False, "space" : False}
        self.velocity: list[int] = [0, 0]

    def update(self, tilemap: Tilemap, movement: tuple = (0, 0)) -> None:
        """
        Update the player's position and handle collisions with the tilemap.

        Args:
            tilemap (Tilemap): The Tilemap object representing the game world.
            movement (tuple, optional): Tuple representing additional movement input. Defaults to (0, 0).
        """
        self.collisions: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
        frameMovement: tuple[float] = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frameMovement[0]
        playerRect: pygame.Rect = pygame.Rect(self.pos[0] + self.pivot[0], self.pos[1] + self.pivot[1], self.hitBoxWidth, self.hitBoxHeight)
        for rect in tilemap.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(playerRect):
                if frameMovement[0] > 0:
                    playerRect.right = rect.left
                    self.collisions["right"] = True
                if frameMovement[0] < 0:
                    playerRect.left = rect.right
                    self.collisions["left"] = True
                # self.pos[0] + self.pivot[0] = playerRect.x same as below, but rearranged
                self.pos[0] = playerRect.x - self.pivot[0]


        self.pos[1] += frameMovement[1]
        playerRect: pygame.Rect = pygame.Rect(self.pos[0] + self.pivot[0], self.pos[1] + self.pivot[1], self.hitBoxWidth, self.hitBoxHeight)
        for rect in tilemap.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(playerRect):
                if frameMovement[1] > 0:
                    playerRect.bottom = rect.top
                    self.collisions["down"] = True
                if frameMovement[1] < 0:
                    playerRect.top = rect.bottom
                    self.collisions["up"] = True
                # self.pos[1] + self.pivot[1] = playerRect.y same as below, but rearranged
                self.pos[1] = playerRect.y - self.pivot[1]

        self.velocity[1] = min(32 / 10 * 2, self.velocity[1] + 0.1)
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        """
        Render the player on the specified surface.

        Args:
            surface (pygame.Surface): The surface onto which the player will be rendered.
            offset (tuple[float, float], optional): Tuple representing the offset of the player's position from the surface's top-left corner. Defaults to (0, 0).
        """
        surface.blit(self.assets["player.png"], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
