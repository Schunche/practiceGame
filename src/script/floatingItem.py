import pygame

from src.script.mathFunc import playerMagnetFunc, getHyp
from src.script.log import logMSG, logError, logSuccess
from src.script.loader import STGS, FIX_STGS

from src.script.item import Item
from src.script.animation import Animation
from src.script.tilemap import Tilemap
from src.fixData.itemSurface import ITEM_IMAGE

class FloatingItem:
    def __init__(self, pos: list[float], item: Item) -> None:
        self.pos: list[float] = pos
        self.item: Item = item
        self.velocity: list[float] = [0, 0]

    def getCollisonRect(self) -> pygame.Rect:
        return pygame.Rect(
            self.pos[0] + ITEM_IMAGE[self.item.id].get_width() * 0.25,
            self.pos[1] + ITEM_IMAGE[self.item.id].get_height() * 0.25,
            ITEM_IMAGE[self.item.id].get_width() * 0.5,
            ITEM_IMAGE[self.item.id].get_height() * 0.5
        )
    
    def update(self, tilemap: Tilemap, playerPos: tuple[float] = (0, 0)) -> None:
        """
        Update the item's position and handle collisions with the tilemap.

        Args:
            tilemap (Tilemap): The tilemap the item collides with.
            playerPos (tuple[float], optional)
        """
        self.collisions: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
        frameMovement: tuple[float] = (self.velocity[0], self.velocity[1])

        self.pos[0] += frameMovement[0]
        itemRect: pygame.Rect = self.getCollisonRect()
        for tileRect in tilemap.physicsRectsAround((int(itemRect.x + itemRect.w * 0.5), int(itemRect.y + itemRect.h * 0.5))):
            if tileRect.colliderect(itemRect):
                if frameMovement[0] > 0:
                    itemRect.right = tileRect.left
                    self.collisions["right"] = True
                if frameMovement[0] < 0:
                    itemRect.left = tileRect.right
                    self.collisions["left"] = True

                if self.collisions["left"] or self.collisions["right"]:
                    self.velocity[0] = 0

                self.pos[0] = itemRect.x - ITEM_IMAGE[self.item.id].get_width() * 0.25

        self.pos[1] += frameMovement[1]
        itemRect: pygame.Rect = self.getCollisonRect()
        for tileRect in tilemap.physicsRectsAround((int(itemRect.x + itemRect.w * 0.5), int(itemRect.y + itemRect.h * 0.5))):
            if tileRect.colliderect(itemRect):
                if frameMovement[1] > 0:
                    itemRect.bottom = tileRect.top
                    self.collisions["down"] = True
                if frameMovement[1] < 0:
                    itemRect.top = tileRect.bottom
                    self.collisions["up"] = True
                self.pos[1] = itemRect.y - ITEM_IMAGE[self.item.id].get_width() * 0.25
        
        # Slow down the item
        if self.velocity[0] > FIX_STGS["airResistHorizontal"]:
            self.velocity[0] -= FIX_STGS["airResistHorizontal"]
        elif self.velocity[0] < -FIX_STGS["airResistHorizontal"]:
            self.velocity[0] += FIX_STGS["airResistHorizontal"]
        else:
            self.velocity[0] = 0

        if getHyp(
            self.getCollisonRect().centerx - playerPos[0],
            self.getCollisonRect().centery - playerPos[1]
        ) <= STGS["tileSize"] * FIX_STGS["reach"]:
            # The item is in the range of the player
            # So it approaches the player
            appVel: tuple[float] = playerMagnetFunc((
                (playerPos[0] - self.getCollisonRect().centerx) / STGS["tileSize"] / FIX_STGS["reach"],
                (playerPos[1] - self.getCollisonRect().centery) / STGS["tileSize"] / FIX_STGS["reach"]
            ))

            #####-------#####
            ##-------------##
            #---------------#
            #-------O-------#
            #---------------#
            ##-------------##
            #####-------#####

            # Set horizontal velocity
            self.velocity[0] += appVel[0] * 0.4

            # Set vertical velocity
            self.velocity[1] += appVel[1] * 0.15
            if not self.collisions["down"] and not self.collisions["up"]:
                self.velocity[1] -= FIX_STGS["gravityStrength"] * abs(appVel[1]) * 0.5

        # Terminal velocity
        if self.velocity[0] > FIX_STGS["floatingItemTermVel"]:
            self.velocity[0] = FIX_STGS["floatingItemTermVel"]
        elif self.velocity[0] < -FIX_STGS["floatingItemTermVel"]:
            self.velocity[0] = -FIX_STGS["floatingItemTermVel"]

        if self.velocity[1] > FIX_STGS["floatingItemTermVel"]:
            self.velocity[1] = FIX_STGS["floatingItemTermVel"]
        elif self.velocity[1] < -FIX_STGS["floatingItemTermVel"]:
            self.velocity[1] = -FIX_STGS["floatingItemTermVel"]

        self.velocity[1] = min(FIX_STGS["floatingItemTermVel"], self.velocity[1] + FIX_STGS["gravityStrength"])
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        surface.blit(ITEM_IMAGE[self.item.id], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
