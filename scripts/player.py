import pygame
from scripts.mob import Mob
from scripts.tilemap import Tilemap

class Player(Mob):
    def __init__(self, assets: dict[str, pygame.Surface]) -> None:
        super().__init__()
        self.assets: dict[str, pygame.Surface] = assets
        self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False, "space" : False}
        self.velocity: list[int] = [0, 0]

    def update(self, tilemap: Tilemap, movement: tuple = (0, 0)) -> None:
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

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.assets["player.png"], self.pos)
