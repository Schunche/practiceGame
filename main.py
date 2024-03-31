import sys

if __name__ != '__main__':
    sys.exit()

import random
import math

from src.script.log import *
logSuccess("Program started")

import pygame
pygame.init()
logMSG("Initialized pygame")

from src.script.loader import *

from src.script.tilemap import Tilemap
from src.script.cloud import Clouds
from src.script.animation import Animation
from src.script.particle import Particle
from src.mobType.player import Player
logMSG("Loaded local dependency from script")

### INITIAL INPUTS HERE
GAME_MODE: str = "admin"

class Main:
    """Main class responsible for managing the game."""
    def __init__(self, tileSize: int = 32) -> None:
        """Initialize the game with specified tile size and settings.

        Args:
            tileSize (int, optional): The size of each tile. Defaults to 32.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.STGS: dict[str, str | int] = loadJson("data/settings")
            logMSG("Loaded settings")
            self.tileSize: int = tileSize
            self.color: dict[str, list[int]] = loadJson("fixData/nameSpace")["color"]

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
            self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS["windowWidth"], self.STGS["windowHeight"]])
            pygame.display.set_caption(self.STGS["windowName"])
            pygame.display.set_icon(self.assets["icon"]["main"])
            self.scroll: list[float] = [0, 0]
            logMSG("Created main window")

            # Tilemap
            self.assets["tile"] = loadTiles("src/img/tile")
            logMSG("Loaded tile assets")

            self.tilemap: Tilemap = Tilemap(
                assets = self.assets["tile"],
                mapName = "map1",
                tileSize = self.tileSize)
            logMSG("Created tilemap")

            # Clouds
            self.assets["cloud"] = loadImagesAsList("src/img/cloud")

            self.windSpeed: float = random.random() * 2 - 1
            logMSG(f"Starting wind speed: {round(self.windSpeed, 2)}")
            logMSG(f"Starting wind direction: {'west' if self.windSpeed < 0 else 'east'}")
            self.clouds = Clouds(self.assets["cloud"], count = 2 ** 4)
            logMSG("Generated clouds")

            # Player
            self.assets["mob"]["player"]["idle"] = Animation(loadImagesAsList("src/img/mob/player/idle"), imageDuration = 6)
            self.assets["mob"]["player"]["run"] = Animation(loadImagesAsList("src/img/mob/player/run"), imageDuration = 4)
            self.assets["mob"]["player"]["jump"] = Animation(loadImagesAsList("src/img/mob/player/jump"), imageDuration = self.STGS["FPS"] / 6)
            self.assets["mob"]["player"]["slide"] = Animation(loadImagesAsList("src/img/mob/player/slide"))
            self.assets["mob"]["player"]["wallSlide"] = Animation(loadImagesAsList("src/img/mob/player/wallSlide"))

            self.player: Player = Player(
                self.assets["mob"],
                pos = [self.STGS["windowWidth"] / 2, self.STGS["windowHeight"] / 2],
                gameMode = GAME_MODE)
            logMSG("Created player")

            # Particles
            self.assets["particle"]["leaf"] = Animation(loadImagesAsList("src/img/particle/leaf"), imageDuration = self.STGS["FPS"] // 2, loop = False)
            self.particles: list[Particle] = [] # List of all existing particles at a given moment

            # Any tile that spawns particles
            self.particleTilePairs: dict[str, list[tuple[str | int]]] = loadJson("fixData/nameSpace")["idPairParticleSpawners"]

            # Any tile thats any variant spawns particles
            self.particleTiles: dict[str, list[str]] = loadJson("fixData/nameSpace")["anyVariantParticleSpawners"]
            
            # Format: {"leaf": [rects], "": [rects]} ~ dict[particle] = rectsOfTilesThatEmit{particle}
            # This contains all the rects of tiles, that emit particles
            self.particleSpawnerTiles: dict[str, list[pygame.Rect]] = {}
            
            for particleStr, spawnerPairs in self.particleTilePairs.items():
                for spawner in self.tilemap.extract(spawnerPairs, keep=True):
                    if particleStr in self.particleSpawnerTiles:
                        self.particleSpawnerTiles[particleStr].append(pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize))
                    else:
                        self.particleSpawnerTiles[particleStr] = [pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize)]

            for particleStr, blockList in self.particleTiles.items():
                for block in blockList:
                    for spawner in self.tilemap.extractAnyVariant(block, keep=True):
                        if particleStr in self.particleSpawnerTiles:
                            self.particleSpawnerTiles[particleStr].append(pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize))
                        else:
                            self.particleSpawnerTiles[particleStr] = [pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize)]

            logMSG("Loaded and generated particles, and their respective spawning tiles")
            logMSG(f"Currently {sum([len(rectList) for rectList in self.particleSpawnerTiles.values()])} tiles emit particles")
            
        except Exception as e:
            logError(f"An error occurred during initialization: {e}")
            sys.exit(1)

    def exitApp(self) -> None:
        """Exit the application."""
        logSuccess("Successfully ran program")
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
                    self.player.jump()
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
        self.scroll[0] += (self.player.pos[0] + self.player.width / 2  - self.STGS["windowWidth"] / 2 - self.scroll[0]) / self.STGS["FPS"] * 2
        self.scroll[1] += (self.player.pos[1] + self.player.height / 2  - self.STGS["windowHeight"] / 2 - self.scroll[1]) / self.STGS["FPS"] * 2
        self.renderScroll: tuple[int] = (int(self.scroll[0]), int(self.scroll[1]))

        # Background
        self.clouds.update(windSpeed = self.windSpeed)

        # Particles
        # Spawn particles
        rectsOnWindow: list[pygame.Rect] = self.tilemap.getRectsOnWindow(self.WINDOW, self.renderScroll)
        for rect in rectsOnWindow:
            for particleStr, rects in self.particleSpawnerTiles.items():
                if rect in rects:
                    if random.random() * 49999  * 2< rect.width * rect.height:
                        pos: tuple[float] = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(
                            assets = self.assets["particle"],
                            species = particleStr,
                            pos = pos,
                            velocity = [
                                (self.windSpeed if particleStr == "leaf" else random.random()) * 0.2,
                                random.random() * 0.4],
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
        self.WINDOW.fill(self.color["pink"])

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

            self.clock.tick(self.STGS["FPS"])
            pygame.display.update()

GAME: Main = Main()
GAME.run()
