import pygame

from src.script.loader import STGS
from src.script.animation import Animation
from src.script.tilemap import Tilemap

class Mob:
    """
    A class representing a mobile entity in a game.

    Attributes:
        pos (list[float]): The position of the mob as a list containing x and y coordinates.
        width (int): The width of the mob's hitbox.
        height (int): The height of the mob's hitbox.
        pivot (tuple[int]): Vector from TopLeft of posxy to TopLeft of hitboxWH.
        hitBoxWidth (int): The width of the mob's hitbox.
        hitBoxHeight (int): The height of the mob's hitbox.
        species: The species of the mob.
        assets (dict[str, dict[str, Animation]]): Dictionary mapping species names to dictionaries containing action names and Animation objects.
        movementInput (dict[str, bool]): Dictionary mapping movement direction keys to boolean values indicating if the key is pressed.
        velocity (list[float]): The velocity of the mob in the x and y directions.
        action (str): The current action of the mob.
        animationOffset (tuple[int]): Offset to adjust the position of the mob's animation.
        flip (bool): Flag indicating if the mob's sprite should be flipped horizontally.
    """
    def __init__(self, species: str, assets: dict[str, dict[str, Animation]], pos: list[float]) -> None:
        """
        Initialize a Mob object.

        Args:
            species (str): The species of the mob.
            assets (dict[str, dict[str, Animation]]): Dictionary mapping species names to dictionaries containing action names and Animation objects.
            pos (list[float]): The initial position of the mob as a list containing x and y coordinates.
        """
        self.pos: list[float] = pos
        self.width: int = 48
        self.height: int = 48

        self.pivot: tuple[int] = (0, 0)  # Vector from TopLeft of posxy to TopLeft of hitboxWH
        self.hitBoxWidth: int = 48
        self.hitBoxHeight: int = 48

        self.species = species
        self.assets: dict[str, dict[str, Animation]] = assets
        self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False, "space" : False}
        self.velocity: list[float] = [0, 0]

        self.action: str = ""
        self.animationOffset: tuple[int] = (0, 0)
        self.flip: bool = False

        self.setAction("idle")

    def rect(self) -> pygame.Rect:
        """Return the rectangular hitbox of the mob."""
        return pygame.Rect(self.pos[0] + self.pivot[0], self.pos[1] + self.pivot[1], self.hitBoxWidth, self.hitBoxHeight)

    def setAction(self, action: str) -> None:
        """
        Set the action of the mob.

        Args:
            action (str): The new action of the mob.
        """
        if action != self.action:
            self.action: str = action
            self.animation: Animation = self.assets[self.species][self.action].copy()

    def update(self, tilemap: Tilemap, movement: tuple[int] = (0, 0)) -> None:
        """
        Update the mob's position and handle collisions with the tilemap.

        Args:
            tilemap (Tilemap): The tilemap the mob interacts with.
            movement (tuple[int], optional): The movement vector. Defaults to (0, 0).
        """
        self.collisions: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
        frameMovement: tuple[float] = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frameMovement[0]
        mobRect: pygame.Rect = self.rect()
        for rect in tilemap.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(mobRect):
                if frameMovement[0] > 0:
                    mobRect.right = rect.left
                    self.collisions["right"] = True
                if frameMovement[0] < 0:
                    mobRect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = mobRect.x - self.pivot[0]

        self.pos[1] += frameMovement[1]
        mobRect: pygame.Rect = self.rect()
        for rect in tilemap.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(mobRect):
                if frameMovement[1] > 0:
                    mobRect.bottom = rect.top
                    self.collisions["down"] = True
                if frameMovement[1] < 0:
                    mobRect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = mobRect.y - self.pivot[1]
        
        if movement[0] > 0:
            self.flip = False
            if not self.collisions["right"]:
                self.velocity[0] = min(2, self.velocity[0] + 0.1)
        elif movement[0] < 0:
            self.flip = True
            if not self.collisions["left"]:
                self.velocity[0] = max(-2, self.velocity[0] - 0.1)
        else:
            if self.velocity[0] > 0.1:
                self.velocity[0] -= 0.1
            elif self.velocity[0] < -0.1:
                self.velocity[0] += 0.1
            else:
                self.velocity[0] = 0

        self.velocity[1] = min(STGS["tileSize"] / 8, self.velocity[1] + 0.1)
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        """
        Render the mob on the given surface with optional offset.

        Args:
            surface (pygame.Surface): The surface to render the mob on.
            offset (tuple[float], optional): The offset to apply to the mob's position. Defaults to (0, 0).
        """
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
            (self.pos[0] - offset[0] + self.animationOffset[0], self.pos[1] - offset[1] + self.animationOffset[1]))
