import pygame

from src.script.loader import resizeImage, getPithagoreanHipotenuse, STGS

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
            self.pos[0],
            self.pos[1],
            int(ITEM_IMAGE[self.item.id].get_width() * 0.5),
            int(ITEM_IMAGE[self.item.id].get_height() * 0.5))

    def update(self, tilemap: Tilemap, pos: tuple[float] = (0, 0)) -> None:
        """
        Update the item's position and handle collisions with the tilemap.

        Args:
            tilemap (Tilemap): The tilemap the item collides with.
            movement (tuple[int], optional): The movement vector. Defaults to (0, 0).
        """

        # Check if the player is close enough
        if getPithagoreanHipotenuse(abs(pos[0] - self.pos[0]) / STGS["tileSize"], abs(pos[1] - self.pos[1]) / STGS["tileSize"] * 2) <= STGS["reach"]:
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
                self.velocity[0] = min(2, self.velocity[0] + 0.1 / movement[0])
        elif movement[0] < 0:
            if not self.collisions["left"]:
                self.velocity[0] = max(-2, self.velocity[0] - 0.1 / movement[0])
        else:
            if self.velocity[0] > 0.1 or self.velocity[0] < -0.1:
                self.velocity[0] = self.velocity[0] * 0.96
            else:
                self.velocity[0] = 0

        if self.velocity[1] > 0:
            self.velocity[1] = min(self.velocity[1] + 0.05, 5)
        else:
            self.velocity[1] += 0.05

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        surface.blit(resizeImage(ITEM_IMAGE[self.item.id], self.rect().size), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
