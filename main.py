import sys

if __name__ != '__main__':
    sys.exit()

import random
import math

from src.data.color import color as COLOR

import pygame

pygame.init()

from src.data.settings import Settings
from src.script.tilemap import Tilemap
from src.script.cloud import Clouds
from src.script.animation import Animation
from src.script.particle import Particle
from src.mobType.player import Player
from src.script.log import logMSG, logError, logSuccess
from src.script.assetLoader import loadImage, loadDirectory, loadTiles, loadImagesAsList

logSuccess("Program started")
logMSG("Initialized pygame")
logMSG("Loaded all local dependency from script")

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

            # tile/dirt/int:0
            self.assets: dict[str, dict[str, dict[str | int, pygame.Surface | Animation] | Animation]] = {
                "mob": {
                    "player": {"player":loadImage("src/img/mob/player.png")}
                },
                "particle": {}
            }
            self.assets["tile"] = loadTiles("src/img/tile")
            logMSG("Loaded tile assets")

            self.assets["cloud"] = loadImagesAsList("src/img/cloud")

            self.assets["mob"]["player"]["idle"] = Animation(loadImagesAsList("src/img/mob/player/idle"), imageDuration = 6)
            self.assets["mob"]["player"]["run"] = Animation(loadImagesAsList("src/img/mob/player/run"), imageDuration = 4)
            self.assets["mob"]["player"]["jump"] = Animation(loadImagesAsList("src/img/mob/player/jump"))
            self.assets["mob"]["player"]["slide"] = Animation(loadImagesAsList("src/img/mob/player/slide"))
            self.assets["mob"]["player"]["wallSlide"] = Animation(loadImagesAsList("src/img/mob/player/wallSlide"))

            self.assets["particle"]["leaf"] = Animation(loadImagesAsList("src/img/particle/leaf"), imageDuration = self.STGS.FPS // 3, loop = False)

            self.tilemap: Tilemap = Tilemap(assets = self.assets["tile"], tileSize = self.tileSize)
            logMSG("Created tilemap")

            self.player: Player = Player(self.assets["mob"], pos = [self.STGS.winWidth / 2, self.STGS.winHeight / 2])
            logMSG("Created player")

            self.clouds = Clouds(self.assets["cloud"], count = 2^4)
            logMSG("Clouds generated")

            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.WINDOW: pygame.Surface = pygame.display.set_mode([self.STGS.winWidth, self.STGS.winHeight])
            pygame.display.set_caption('Das Spielplatz')
            self.scroll: list[float] = [0, 0]

            self.LEAF_SPAWNERS: list[pygame.Rect] = []
            for spawner in self.tilemap.extract([("oakLeaf", 0)], keep=True):
                self.LEAF_SPAWNERS.append(pygame.Rect(spawner[0][0], spawner[0][1], self.tileSize, self.tileSize))
            self.particles: list[Particle] = []
            
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

        self.clouds.update()

        for rect in self.LEAF_SPAWNERS: # Should be optimized
            if random.random() * 49999 < rect.width * rect.height:
                pos: tuple[float] = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                self.particles.append(Particle(self.assets["particle"], "leaf", pos, [random.random() * 0.2, random.random() * 0.4], frame = random.randint(0, len(self.assets["particle"]["leaf"].images))))

        for particle in self.particles.copy():
            kill = particle.update()
            if particle.species in ["leaf"]:
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.25
            if kill:
                self.particles.remove(particle)

        # Camera movement
        self.scroll[0] += (self.player.pos[0] + self.player.width / 2  - self.STGS.winWidth / 2 - self.scroll[0]) / self.STGS.FPS * 2
        self.scroll[1] += (self.player.pos[1] + self.player.height / 2  - self.STGS.winHeight / 2 - self.scroll[1]) / self.STGS.FPS * 2
        self.renderScroll: tuple[int] = (int(self.scroll[0]), int(self.scroll[1]))

        # Player movement
        self.player.update(self.tilemap,
            (self.player.movementInput["right"] - self.player.movementInput["left"],
            0))
    
    def handleRender(self) -> None:
        """Render game elements."""
        self.WINDOW.fill(COLOR["pink"])

        self.clouds.render(self.WINDOW, offset = self.renderScroll)

        self.tilemap.render(self.WINDOW, offset = self.renderScroll)
            
        self.player.render(self.WINDOW, offset = self.renderScroll)
        
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
