import pygame

from src.script.animation import Animation
from src.script.mob import Mob

class Player(Mob):
    """
    A class representing the player character in the game.

    Inherits from Mob class.

    Attributes:
        airTime (int): The time the player has spent in the air since the last contact with the ground.
    """
    def __init__(self, assets: dict[str, dict[str, Animation]], pos: list[float]) -> None:
        """
        Initialize a Player object.

        Args:
            assets (dict[str, dict[str, Animation]]): A dictionary containing player assets.
            pos (list[float]): The initial position of the player as a list containing x and y coordinates.
        """
        super().__init__(species = "player", assets = assets, pos = pos)
        self.airTime: int = 0

        self.maxJumps: int = 1
        self.jumps: int = self.maxJumps

        self.wallSlide = False

    def update(self, tilemap, movement=(0, 0)) -> None:
        """
        Update the player's position and animation.

        Args:
            tilemap: The tilemap object representing the game's environment.
            movement (tuple, optional): A tuple representing movement input. Defaults to (0, 0).
        """
        # Inherit parent's .update
        super().update(tilemap, movement=movement)

        # Reset number of jumps
        self.airTime += 1
        if self.collisions["down"]:
            self.airTime = 0
            self.jumps = self.maxJumps

        # Check for wall slide
        self.wallSlide = False
        if (self.collisions["left"] or self.collisions["right"]) and self.airTime > 4:
            self.wallSlide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.setAction("wallSlide")

        # Set action
        if not self.wallSlide:
            if self.airTime > 4:
                self.setAction("jump")
            elif movement[0] != 0:
                self.setAction("run")
            else:
                self.setAction("idle")

    def jump(self) -> None:
        if self.wallSlide:
            if self.flip:
                self.velocity[0] = 3.5
            else:
                self.velocity[0] = -3.5

            self.velocity[1] = -2.5
            self.airTime = 5
            self.jumps = max(0, self.jumps - 1)

        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.airTime = 5
