import pygame

from src.script.log import logMSG, logError, logSuccess
from src.script.loader import getPithagoreanHipotenuse, STGS, FIX_STGS

from src.script.item import Item
from src.script.animation import Animation
from src.script.tilemap import Tilemap
from src.fixData.itemSurface import ITEM_IMAGE

class FloatingItem:
    def __init__(self, pos: list[float], item: Item) -> None:
        self.pos: list[float] = pos
        self.item: Item = item
        self.velocity: list[float] = [0, 0]

    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.pos[0] + int(ITEM_IMAGE[self.item.id].get_width() * 0.25),
            self.pos[1] + int(ITEM_IMAGE[self.item.id].get_height() * 0.25),
            int(ITEM_IMAGE[self.item.id].get_width() * 0.5),
            int(ITEM_IMAGE[self.item.id].get_height() * 0.5)
        )
        ######## #: png
        ###xxx##
        ###xxx## x: hitbox i guess
        ########

    def update(self, tilemap: Tilemap, pos: tuple[float] = (0, 0)) -> None:
        """
        Update the item's position and handle collisions with the tilemap.

        Args:
            tilemap (Tilemap): The tilemap the item collides with.
            movement (tuple[int], optional): The movement vector. Defaults to (0, 0).
        """

        # Check if the player is close enough
        if getPithagoreanHipotenuse(abs(pos[0] - self.pos[0] - self.rect().w * 0.5), abs(pos[1] - self.pos[1] - self.rect().h * 0.5)) <= STGS["tileSize"] * FIX_STGS["reach"]:
            movement: tuple[float] = ((pos[0] - self.pos[0]) / STGS["tileSize"], (pos[1] - self.pos[1]) / STGS["tileSize"])
        else:
            movement: tuple[float] = (0, 0)

        self.collisions: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
        frameMovement: tuple[float] = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frameMovement[0]
        itemRect: pygame.Rect = self.rect()
        for rect in tilemap.physicsRectsAround((int(itemRect.x + itemRect.w * 0.5), int(itemRect.y + itemRect.h * 0.5))):
            if rect.colliderect(itemRect):
                if frameMovement[0] > 0:
                    itemRect.right = rect.left
                    self.collisions["right"] = True
                if frameMovement[0] < 0:
                    itemRect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = itemRect.x

        self.pos[1] += frameMovement[1]
        itemRect: pygame.Rect = self.rect()
        for rect in tilemap.physicsRectsAround((int(itemRect.x + itemRect.w * 0.5), int(itemRect.y + itemRect.h * 0.5))):
            if rect.colliderect(itemRect):
                if frameMovement[1] > 0:
                    itemRect.bottom = rect.top
                    self.collisions["down"] = True
                if frameMovement[1] < 0:
                    itemRect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = itemRect.y
        
        if movement[0] > 0:
            if not self.collisions["right"]:
                self.velocity[0] = self.velocity[0] + 0.1
        elif movement[0] < 0:
            if not self.collisions["left"]:
                self.velocity[0] = self.velocity[0] - 0.1

        self.velocity[1] = min(STGS["tileSize"] / 8, self.velocity[1] + 0.1)
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        surface.blit(ITEM_IMAGE[self.item.id], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
