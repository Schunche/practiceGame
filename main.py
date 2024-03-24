import sys

if __name__ != '__main__':
    sys.exit()

import pygame

pygame.init()

from scripts.settings import Settings
from scripts.tilemap import Tilemap
from scripts.player import Player
from scripts.log import logMSG, logError
from scripts.assetLoader import loadImage, loadDirectory

logMSG("Initialized pygame")
logMSG("Loaded all local dependency scripts")

class Main:
    """
    Main class to manage the game loop and handle game events.
    """
    def __init__(self, tileSize: int = 32, settings: Settings = Settings()) -> None:
        """
        Initialize the game.

        Args:
            tileSize (int, optional): Size of the tiles. Defaults to 32.
            settings (Settings, optional): Game settings. Defaults to Settings().
        """
        try:
            self.STGS: Settings = settings
            self.tileSize: int = tileSize

            self.assets: dict[str, dict[str, pygame.Surface]] = {}
            self.assets["tiles"] = loadDirectory("src/tile")
            logMSG("Loaded tile assets")
            self.assets["mob"] = loadDirectory("src/mob")
            logMSG("Loaded mob assets")

            self.tilemap: Tilemap = Tilemap(tileAssets = self.assets["tiles"], tileSize = self.tileSize)
            logMSG("Created tilemap")
            self.player: Player = Player(self.assets["mob"])
            logMSG("Created player")

            self.clock: pygame.time.Clock = pygame.time.Clock()

            self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS.winWidth, self.STGS.winHeight])
            pygame.display.set_caption('Das Spielplatz')
            self.scroll: list[float] = [0, 0]

            self.COLOR: dict[str, list[int]] = {
                "black" : [0, 0, 0],
                "pink" : [200, 50, 75]
                }
            
        except Exception as e:
            logError(f"An error occurred during initialization: {e}")
            sys.exit(1)

    def exitApp(self) -> None:
        """Exit the application."""
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
        """Handle game updates."""
        # Camera movement
        self.scroll[0] += (self.player.pos[0] + self.player.width / 2  - self.STGS.winWidth / 2 - self.scroll[0]) / self.STGS.FPS
        self.scroll[1] += (self.player.pos[1] + self.player.height / 2  - self.STGS.winHeight / 2 - self.scroll[1]) / self.STGS.FPS
        self.renderScroll: tuple[int] = (int(self.scroll[0]), int(self.scroll[1]))

        # Player movement
        self.player.update(self.tilemap,
            (self.player.movementInput["right"] - self.player.movementInput["left"],
            0))
    
    def handleRender(self) -> None:
        """Handle rendering of game objects."""
        self.WINDOW.fill(self.COLOR["pink"])

        self.tilemap.render(self.WINDOW, offset = self.renderScroll)
            
        self.player.render(self.WINDOW, offset = self.renderScroll)
    
    def run(self) -> None:
        """Run the game loop."""
        while True:
            self.handleEvents()
            self.handleUpdates()
            self.handleRender()
            self.clock.tick(self.STGS.FPS)
            pygame.display.update()

GAME: Main = Main()
GAME.run()
