import sys

if __name__ != '__main__':
    sys.exit()

import random
import math

from src.data.color import color as COLOR
from src.data.settings import Settings
from src.script.log import logMSG, logError, logSuccess

import pygame

pygame.init()

from src.script.assetLoader import loadImage, loadDirectory, loadTiles, loadImagesAsList

from src.script.tilemap import Tilemap
from src.script.cloud import Clouds
from src.script.animation import Animation
from src.script.particle import Particle
from src.mobType.player import Player

logSuccess("Program started")
logMSG("Initialized pygame")
logMSG("Loaded local dependency from script")

class Main:
    """Main class responsible for managing the game."""
    def __init__(self, tileSize: int = 32, settings: Settings = Settings()) -> None:
        """Initialize the game with specified tile size and settings.

        Args:
            tileSize (int, optional): The size of each tile. Defaults to 32.
            settings (Settings, optional): Game settings. Defaults to Settings().

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.STGS: Settings = settings
            self.tileSize: int = tileSize

            # Main assets
            # tile/block/int
            # mob/species/action/int
            # paricle/species/int
            # cloud/int
            self.assets: dict[str, dict[str, dict[str | int, pygame.Surface | Animation] | Animation]] = {
                "mob": {
                    "player": {}
                },
                "particle": {},
                "icon": {
                   "main": loadImage("src/img/icon/main.png")
                    }
            }
            
            # Main window, timer, camera offset
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS.winWidth, self.STGS.winHeight])
            pygame.display.set_caption('Das Spielplatz')
            pygame.display.set_icon(self.assets["icon"]["main"])
            self.scroll: list[float] = [0, 0]
            logMSG("Created main window")

            # Tilemap
            self.assets["tile"] = loadTiles("src/img/tile")
            logMSG("Loaded tile assets")

            self.tilemap: Tilemap = Tilemap(assets = self.assets["tile"], tileSize = self.tileSize)
            logMSG("Created tilemap")

            # Clouds
            self.assets["cloud"] = loadImagesAsList("src/img/cloud")

            self.clouds = Clouds(self.assets["cloud"], count = 2 ** 4)
            logMSG("Generated clouds")

            # Player
            self.assets["mob"]["player"]["idle"] = Animation(loadImagesAsList("src/img/mob/player/idle"), imageDuration = 6)
            self.assets["mob"]["player"]["run"] = Animation(loadImagesAsList("src/img/mob/player/run"), imageDuration = 4)
            self.assets["mob"]["player"]["jump"] = Animation(loadImagesAsList("src/img/mob/player/jump"), imageDuration = self.STGS.FPS / 6)
            self.assets["mob"]["player"]["slide"] = Animation(loadImagesAsList("src/img/mob/player/slide"))
            self.assets["mob"]["player"]["wallSlide"] = Animation(loadImagesAsList("src/img/mob/player/wallSlide"))

            self.player: Player = Player(self.assets["mob"], pos = [self.STGS.winWidth / 2, self.STGS.winHeight / 2])
            logMSG("Created player")

            # Particles
            self.assets["particle"]["leaf"] = Animation(loadImagesAsList("src/img/particle/leaf"), imageDuration = self.STGS.FPS // 2, loop = False)
            self.particles: list[Particle] = [] # List of all existing particles at a given moment

            # "leaf" : [("oakLeaf", 0), ("oakLogLeaf", 0)]
            self.particleTilePairs: dict[str, list[tuple[str | int]]] = {"leaf": [("oakLeaf", 0), ("oakLogLeaf", 0)]}
            
            # Format: {"leaf": [rects], "": [rects]} ~ dict[particle] = rectsOfTilesThatEmit{particle}
            # This contains all the rects of tiles, that emit particles
            self.particleSpawnerTiles: dict[str, list[pygame.Rect]] = {}
            
            for particleStr, spawnerPairs in self.particleTilePairs.items():
                for spawner in self.tilemap.extract(spawnerPairs, keep=True):
                    if particleStr in self.particleSpawnerTiles:
                        self.particleSpawnerTiles[particleStr].append(pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize))
                    else:
                        self.particleSpawnerTiles[particleStr] = [pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize)]
            logMSG("Loaded and generated particles, and their respective spawning tiles")
            
        except Exception as e:
            logError(f"An error occurred during initialization: {e}")
            sys.exit(1)

    def exitApp(self) -> None:
        """Exit the application."""
        logSuccess("Successful run of program")
        pygame.quit()
        sys.exit()

    def handleEvents(self) -> None:
        """Handle pygame events."""
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
        """Update game state."""

        # Camera movement
        self.scroll[0] += (self.player.pos[0] + self.player.width / 2  - self.STGS.winWidth / 2 - self.scroll[0]) / self.STGS.FPS * 2
        self.scroll[1] += (self.player.pos[1] + self.player.height / 2  - self.STGS.winHeight / 2 - self.scroll[1]) / self.STGS.FPS * 2
        self.renderScroll: tuple[int] = (int(self.scroll[0]), int(self.scroll[1]))

        # Background
        self.clouds.update()

        # Particles
        # Spawn particles
        rectsOnWindow: list[pygame.Rect] = self.tilemap.getRectsOnWindow(self.WINDOW, self.renderScroll)
        for rect in rectsOnWindow:
            for particleStr, rects in self.particleSpawnerTiles.items():
                if rect in rects:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos: tuple[float] = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(
                            assets = self.assets["particle"],
                            species = particleStr,
                            pos = pos,
                            velocity = [random.random() * 0.2, random.random() * 0.4],
                            frame = random.randint(0, len(self.assets["particle"][particleStr].images)) ))

        # Udpate particles
        for particle in self.particles.copy():
            kill = particle.update()
            if kill:
                self.particles.remove(particle)
            if particle.species in ["leaf"]:
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.25

        # Player movement
        self.player.update(self.tilemap,
            (self.player.movementInput["right"] - self.player.movementInput["left"],
            0))
    
    def handleRender(self) -> None:
        """Render game elements."""
        # Background
        self.WINDOW.fill(COLOR["pink"])

        self.clouds.render(self.WINDOW, offset = self.renderScroll)

        # Tilemap
        self.tilemap.render(self.WINDOW, offset = self.renderScroll)
        
        # Mobs
        self.player.render(self.WINDOW, offset = self.renderScroll)
        
        # Particles
        # If generation is optimized, this -v does not need to be
        for particle in self.particles:
            particle.render(self.WINDOW, offset = self.renderScroll)
    
    def run(self) -> None:
        """Main game loop."""
        while True:
            self.handleEvents()
            self.handleUpdates()
            self.handleRender()

            self.clock.tick(self.STGS.FPS)
            pygame.display.update()

GAME: Main = Main()
GAME.run()
