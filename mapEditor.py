import sys

if __name__ != '__main__':
    sys.exit()

import pygame

pygame.init()

from scripts.settings import Settings
from scripts.tilemap import Tilemap
from scripts.log import logMSG, logError
from scripts.assetLoader import loadImage, loadDirectory, loadTiles

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
            self.assets["tiles"] = loadTiles("src/tile")
            logMSG("Loaded tile assets")
            self.assets["mob"] = loadDirectory("src/mob")
            logMSG("Loaded mob assets")

            self.tilemap: Tilemap = Tilemap(tileAssets = self.assets["tiles"], tileSize = self.tileSize)
            logMSG("Created tilemap")

            self.clock: pygame.time.Clock = pygame.time.Clock()

            self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS.winWidth, self.STGS.winHeight])
            pygame.display.set_caption('Das Spielplatz von Map Editor')
            self.scroll: list[float] = [0, 0]
            
            self.pos: list[float] = [0, 0]
            self.movementInput: dict[str, bool] = {"left" : False, "right" : False, "up" : False, "down" : False}
            self.clicking: dict[str, bool] = {"left" : False, "right" : False, "middle" : False, "up" : False, "down" : False}

            self.tileList: list[tuple[str | int]] = []
            for block in self.assets["tiles"]:
                for variant in self.assets["tiles"][block]:
                    self.tileList.append((block, variant))
            self.tileIndex: int = 0
            self.currentTileImg: pygame.Surface = self.assets["tiles"][self.tileList[self.tileIndex][0]][self.tileList[self.tileIndex][1]].copy()
            self.currentTileImg.set_alpha(100)
            
        except Exception as e:
            logError(f"An error occurred during initialization: {e}")
            sys.exit(1)

    def exitApp(self) -> None:
        """Exit the application."""
        pygame.quit()
        sys.exit()

    def handleEvents(self) -> None:
        """Handle input game events."""
        self.mousePos: tuple[int] = pygame.mouse.get_pos()
        self.tilePos = (int(self.mousePos[0] + self.pos[0]) // self.tileSize, int(self.mousePos[1] + self.pos[1]) // self.tileSize)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitApp()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking["left"] = True
                if event.button == 2:
                    self.clicking["middle"] = True
                if event.button == 3:
                    self.clicking["right"] = True
                if event.button == 4:
                    self.clicking["up"] = True
                    self.tileIndex = (self.tileIndex + 1) % len(self.tileList)
                if event.button == 5:
                    self.clicking["down"] = True
                    self.tileIndex = (self.tileIndex - 1) % len(self.tileList)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking["left"] = False
                if event.button == 2:
                    self.clicking["middle"] = False
                if event.button == 3:
                    self.clicking["right"] = False
                if event.button == 4:
                    self.clicking["up"] = False
                if event.button == 5:
                    self.clicking["down"] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.tilemap.saveMap()
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

        if self.clicking["left"]:
            self.tilemap.insertTile(pos = (self.tilePos[0], self.tilePos[1]), tile = {
                "block": self.tileList[self.tileIndex][0],
                "variant": self.tileList[self.tileIndex][1]
                })

        if self.clicking["right"]:
            if self.tilemap.isTileAt(self.tilePos):
                logMSG(f"Tile deleted at {self.tilePos}")
                self.tilemap.deleteTile(self.tilePos)

        self.currentTileImg = self.assets["tiles"][self.tileList[self.tileIndex][0]][self.tileList[self.tileIndex][1]].copy()
        self.currentTileImg.set_alpha(100)
    
    def handleRender(self) -> None:
        """Handle rendering of game objects."""
        self.WINDOW.fill([0, 0, 0])

        self.tilemap.render(self.WINDOW, offset = self.pos)

        self.WINDOW.blit(self.currentTileImg, (self.tilePos[0] * self.tileSize - self.pos[0], self.tilePos[1] * self.tileSize - self.pos[1]))
        self.WINDOW.blit(self.currentTileImg, (int(self.tileSize / 2), int(self.tileSize / 2)))
    
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
