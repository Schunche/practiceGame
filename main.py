import sys

if __name__ != '__main__':
    sys.exit()

import pygame
import os
import random

pygame.init()

class Settings:
    def __init__(self, winW: int = 1280, winH: int = 720, FPS: int = 60) -> None:
        self.winWidth: int = winW
        self.winHeight: int = winH
        self.FPS: int = FPS

class Mob: # Player, Enemies # Hopefully not used directly
    def __init__(self) -> None:
        self.pos: list[float] = [72, 0]

        self.width: int = 48
        self.height: int = 48
        self.pivot: list[int] = [0, 0] # Vector from TopLeft of posxy to TopLeft of hitboxWH
        self.hitBoxWidth: int = 48
        self.hitBoxHeight: int = 48

class Player(Mob):
    def __init__(self) -> None:
        super().__init__()

        self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False, "space" : False}

        self.velocity = [0, 0]

    def update(self, game, movement: tuple = (0, 0)):
        self.collisions: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
        frameMovement: tuple[float] = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frameMovement[0]
        playerRect: pygame.Rect = pygame.Rect(self.pos[0] + self.pivot[0], self.pos[1] + self.pivot[1], self.hitBoxWidth, self.hitBoxHeight)
        for rect in game.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
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
        for rect in game.physicsRectsAround((self.pos[0] + self.pivot[0] + self.hitBoxWidth / 2, self.pos[1] + self.pivot[1] + self.hitBoxHeight / 2)):
            if rect.colliderect(playerRect):
                if frameMovement[1] > 0:
                    playerRect.bottom = rect.top
                    self.collisions["down"] = True
                if frameMovement[1] < 0:
                    playerRect.top = rect.bottom
                    self.collisions["up"] = True
                # self.pos[1] + self.pivot[1] = playerRect.y same as below, but rearranged
                self.pos[1] = playerRect.y - self.pivot[1]

        self.velocity[1] = min(game.tileSize / 10 * 2, self.velocity[1] + 0.1)
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

class Projectile: # Arrow, Bullet
    def __init__(self) -> None:
        self.pos: list[float] = [0, 0]

class Main:
    def __init__(self, tileSize: int = 32, settings: Settings = Settings(), player: Player = Player()) -> None:
        self.STGS: Settings = settings
        self.player: Player = player
        self.tileSize: int = tileSize
        self.nOffsets: list[tuple[int]] = [(i, j) for j in range(-2, 3) for i in range(-1, 2)]
        self.physicsTiles: list[str] = ["dirt"]

        self.clock: pygame.Clock = pygame.time.Clock()

        self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS.winWidth, self.STGS.winHeight])
        pygame.display.set_caption('Das Spielplatz')
        
        self.tiles: dict[tuple, dict[str, str | int]] = {
            (0, 0) : {
                "block" : "dirt",
                "variant" : 0
            }, (0, 2) : {
                "block" : "dirt",
                "variant" : 0
            }, (1, 5) : {
                "block" : "dirt",
                "variant" : 0
            }, (0, 4) : {
                "block" : "dirt",
                "variant" : 0
            }, (0, 5) : {
                "block" : "dirt",
                "variant" : 0
            }, (0, 3) : {
                "block" : "dirt",
                "variant" : 0
            }, (2, 2) : {
                "block" : "dirt",
                "variant" : 0
            }, (3, 6) : {
                "block" : "dirt",
                "variant" : 0
            }, (9, 9) : {
                "block" : "dirt",
                "variant" : 0
            }}

        self.assets: dict[str, pygame.Surface] = {}
        self.assets.update(self.loadDirectory("src/tile"))
        self.assets.update(self.loadDirectory("src/mob"))

        self.COLOR: dict[str, list[int]] = {
            "black" : [0, 0, 0],
            "pink" : [200, 50, 75]}
    
    def tilesAround(self, pos) -> list[tuple[tuple[int], dict[str, str | int]]]:
        dasTiles: list[int] = []
        tileLocation = (
            int(pos[0] // self.tileSize),
            int(pos[1] // self.tileSize))
        for offset in self.nOffsets:
            checkLocation = (
                tileLocation[0] + offset[0],
                tileLocation[1] + offset[1])
            if checkLocation in self.tiles:
                dasTiles.append((checkLocation, self.tiles[checkLocation]))
        return dasTiles
    
    def physicsRectsAround(self, pos) -> list[tuple[tuple[int], dict[str, str | int]]]:
        rects: list[pygame.Rect] = []
        for tile in self.tilesAround(pos):
            if tile[1]["block"] in self.physicsTiles:
                rects.append(pygame.Rect(
                    tile[0][0] * self.tileSize,
                    tile[0][1] * self.tileSize,
                    self.tileSize,
                    self.tileSize
                    ))
        return rects
    
    def loadImage(self, path) -> pygame.Surface:
        image = pygame.image.load(path)
        image.set_colorkey([23, 23, 32])
        return image
        
    def loadDirectory(self, path) -> dict[str, pygame.Surface]:
        images = {}
        for imageName in os.listdir(path):
            images[imageName] = self.loadImage(path + '/' + imageName)
        return images

    def exitApp(self) -> None:
        pygame.quit()
        sys.exit()

    def handleEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitApp()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exitApp()

                if event.key == pygame.K_a:
                    self.player.movementInput["left"] = True
                if event.key == pygame.K_d:
                    self.player.movementInput["right"] = True
                if event.key == pygame.K_w:
                    self.player.movementInput["up"] = True
                if event.key == pygame.K_s:
                    self.player.movementInput["down"] = True
                if event.key == pygame.K_SPACE:
                    self.player.velocity[1] = -self.tileSize / 10
                if event.key == pygame.K_r:
                    self.player.pos = [self.tileSize, self.tileSize * 0]
                if event.key == pygame.K_t:
                    self.player.pos = [self.tileSize * 5, self.tileSize * 0]
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.movementInput["left"] = False
                if event.key == pygame.K_d:
                    self.player.movementInput["right"] = False
                if event.key == pygame.K_w:
                    self.player.movementInput["up"] = False
                if event.key == pygame.K_s:
                    self.player.movementInput["down"] = False
                if event.key == pygame.K_SPACE:
                    self.player.movementInput["space"] = False
    
    def handleUpdates(self) -> None:
        # Player movement
        self.player.update(self,
            (self.player.movementInput["right"] - self.player.movementInput["left"],
            0))
    
    def handleRender(self) -> None:
        self.WINDOW.fill(self.COLOR["pink"])

        # BAD!!! Render all tiles
        for location in self.tiles:
            tile = self.tiles[location]
            self.WINDOW.blit(self.assets[tile["block"] + str(tile["variant"]) + '.png'],
                [location[0] * self.tileSize,
                location[1] * self.tileSize])
            
        self.WINDOW.blit(self.assets["player.png"], self.player.pos)
    
    def run(self) -> None:
        while True:
            self.handleEvents()
            self.handleUpdates()
            self.handleRender()
            self.clock.tick(self.STGS.FPS)
            pygame.display.update()

GAME: Main = Main()
GAME.run()