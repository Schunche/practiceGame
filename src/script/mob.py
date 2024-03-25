import pygame

from src.script.tilemap import Tilemap

class Mob:
    def __init__(self, species: str, assets, pos: list[int]) -> None:
        self.pos: list[float] = pos
        self.width: int = 48
        self.height: int = 48

        self.pivot: tuple[int] = (0, 0)  # Vector from TopLeft of posxy to TopLeft of hitboxWH
        self.hitBoxWidth: int = 48
        self.hitBoxHeight: int = 48

        self.species = species
        self.assets: dict[str, pygame.Surface] = assets
        self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False, "space" : False}
        self.velocity: list[int] = [0, 0]

        self.action: str = ""
        self.animationOffset = (0, 0)
        self.flip = False

        self.setAction("idle")

    def rect(self):
        return pygame.Rect(self.pos[0] + self.pivot[0], self.pos[1] + self.pivot[1], self.hitBoxWidth, self.hitBoxHeight)

    def setAction(self, action) -> None:
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.species][self.action].copy()

    def update(self, tilemap: Tilemap, movement: tuple = (0, 0)) -> None:
        self.collisions: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
        frameMovement: tuple[float] = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frameMovement[0]
        entityRect: pygame.Rect = self.rect()
        for rect in tilemap.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(entityRect):
                if frameMovement[0] > 0:
                    entityRect.right = rect.left
                    self.collisions["right"] = True
                if frameMovement[0] < 0:
                    entityRect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entityRect.x - self.pivot[0]

        self.pos[1] += frameMovement[1]
        entityRect: pygame.Rect = self.rect()
        for rect in tilemap.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(entityRect):
                if frameMovement[1] > 0:
                    entityRect.bottom = rect.top
                    self.collisions["down"] = True
                if frameMovement[1] < 0:
                    entityRect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entityRect.y - self.pivot[1]
        
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True
        else: pass

        self.velocity[1] = min(32 / 10 * 2, self.velocity[1] + 0.1)
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
            (self.pos[0] - offset[0] + self.animationOffset[0], self.pos[1] - offset[1] + self.animationOffset[1]))
