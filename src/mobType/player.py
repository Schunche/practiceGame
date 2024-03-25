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

    def update(self, tilemap, movement=(0, 0)) -> None:
        """
        Update the player's position and animation.

        Args:
            tilemap: The tilemap object representing the game's environment.
            movement (tuple, optional): A tuple representing movement input. Defaults to (0, 0).
        """
        super().update(tilemap, movement=movement)

        self.airTime += 1
        if self.collisions["down"]:
            self.airTime = 0

        if self.airTime > 4:
            self.setAction("jump")
        elif movement[0] != 0:
            self.setAction("run")
        else:
            self.setAction("idle")
