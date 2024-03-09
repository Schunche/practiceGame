import sys

if __name__ != '__main__':
    sys.exit()

import pygame
import os
import random

from scripts.settings import Settings

pygame.init()

from scripts.tilemap import Tilemap
from scripts.player import Player

class Main:
    def __init__(self, tileSize: int = 32, settings: Settings = Settings()) -> None:
        self.STGS: Settings = settings
        self.tileSize: int = tileSize

        self.assets: dict[str, dict[str, pygame.Surface]] = {}
        self.assets["tiles"] = self.loadDirectory("src/tile")
        self.assets["mob"] = self.loadDirectory("src/mob")
        
        self.tilemap: Tilemap = Tilemap(tileAssets = self.assets["tiles"], tileSize = self.tileSize)
        self.player: Player = Player(self.assets["mob"])

        self.clock: pygame.Clock = pygame.time.Clock()

        self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS.winWidth, self.STGS.winHeight])
        pygame.display.set_caption('Das Spielplatz')
        self.scroll: list[float] = [0, 0]

        self.COLOR: dict[str, list[int]] = {
            "black" : [0, 0, 0],
            "pink" : [200, 50, 75]}
    
    def loadImage(self, path) -> pygame.Surface:
        image: pygame.Surface = pygame.image.load(path)
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
        # Camera movement
        self.scroll[0] += (self.player.pos[0] + self.player.width / 2  - self.STGS.winWidth / 2 - self.scroll[0]) / self.STGS.FPS
        self.scroll[1] += (self.player.pos[1] + self.player.height / 2  - self.STGS.winHeight / 2 - self.scroll[1]) / self.STGS.FPS
        self.renderScroll: tuple[int] = (int(self.scroll[0]), int(self.scroll[1]))

        # Player movement
        self.player.update(self.tilemap,
            (self.player.movementInput["right"] - self.player.movementInput["left"],
            0))
    
    def handleRender(self) -> None:
        self.WINDOW.fill(self.COLOR["pink"])

        self.tilemap.render(self.WINDOW, offset = self.renderScroll)
            
        self.player.render(self.WINDOW, offset = self.renderScroll)
    
    def run(self) -> None:
        while True:
            self.handleEvents()
            self.handleUpdates()
            self.handleRender()
            self.clock.tick(self.STGS.FPS)
            pygame.display.update()

GAME: Main = Main()
GAME.run()
