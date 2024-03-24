import pygame

from scripts.mob import Mob

class Player(Mob):
    def __init__(self, assets, pos) -> None:
        super().__init__(species = "player", assets = assets, pos = pos)
        self.airTime = 0

    def update(self, tilemap, movement=(0, 0)) -> None:
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
