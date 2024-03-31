import sys

if __name__ != '__main__':
    sys.exit()

from src.script.log import *
logSuccess("Program started")

import pygame
pygame.init()
logMSG("Initialized pygame")

from src.script.tilemap import Tilemap
from src.script.log import *
from src.script.loader import *
logMSG("Loaded all local dependency script")

class Main:
    """
    Main class to manage the game loop and handle game events.
    """
    def __init__(self, tileSize: int = 1) -> None:
        """
        Initialize the game.

        Args:
            tileSize (int, optional): Size of the tiles. Defaults to 2.
        """
        try:
            self.STGS: dict[str, str | int] = loadJson("data/settings")
            self.tileSize: int = tileSize

            self.assets: dict[str, dict[str, pygame.Surface]] = {}
            self.assets["tiles"] = loadTilesResized("src/img/bit", tileSize = self.tileSize)
            logMSG("Loaded tile assets")

            self.tilemap: Tilemap = Tilemap(
                assets = self.assets["tiles"],
                mapName = "procedural",
                tileSize = self.tileSize)
            logMSG("Created tilemap")

            self.clock: pygame.time.Clock = pygame.time.Clock()

            self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS["windowWidth"], self.STGS["windowHeight"]])
            pygame.display.set_caption(f'{self.STGS["windowName"]} von Map Seeker')
            
            self.pos: list[float] = [0, 0]
            self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
            
        except Exception as e:
            logError(f"An error occurred during initialization: {e}")
            sys.exit(1)

    def exitApp(self) -> None:
        """Exit the application."""
        logSuccess("Successfully run program")
        pygame.quit()
        sys.exit()

    def handleEvents(self) -> None:
        """Handle input game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitApp()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exitApp()

                if event.key == pygame.K_a:
                    self.movementInput["left"] = True
                if event.key == pygame.K_d:
                    self.movementInput["right"] = True
                if event.key == pygame.K_w:
                    self.movementInput["up"] = True
                if event.key == pygame.K_s:
                    self.movementInput["down"] = True
                if event.key == pygame.K_r:
                    self.pos = [self.tileSize, self.tileSize * 0]
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movementInput["left"] = False
                if event.key == pygame.K_d:
                    self.movementInput["right"] = False
                if event.key == pygame.K_w:
                    self.movementInput["up"] = False
                if event.key == pygame.K_s:
                    self.movementInput["down"] = False
    
    def handleUpdates(self) -> None:
        """Handle game updates."""
        self.pos[0] += (self.movementInput["right"] - self.movementInput["left"]) * 5
        self.pos[1] += (self.movementInput["down"] - self.movementInput["up"]) * 5
    
    def handleRender(self) -> None:
        """Handle rendering of game objects."""
        self.WINDOW.fill([0, 0, 0])

        self.tilemap.renderSeek(self.WINDOW, offset = self.pos)
    
    def run(self) -> None:
        """Run the game loop."""
        while True:
            self.handleEvents()
            self.handleUpdates()
            self.handleRender()

            self.clock.tick(int(self.STGS["FPS"] / 4))
            pygame.display.update()

GAME: Main = Main()
GAME.run()
