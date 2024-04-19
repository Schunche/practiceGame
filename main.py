import sys

if __name__ != '__main__':
    sys.exit()

import random
import math
from copy import deepcopy

from src.script.log import *
logSuccess("Program started")

import pygame
pygame.init()
logMSG("Initialized pygame")

from src.script.loader import loadImage, STGS, FIX_STGS, loadDirectory, loadImagesAsList, loadTiles, resizeImage, loadImageResized
from src.script.gui import Button, renderText

from src.script.tilemap import Tilemap
from src.script.cloud import Clouds
from src.script.animation import Animation
from src.script.particle import Particle
from src.script.item import *
from src.script.floatingItem import FloatingItem
from src.fixData.table import SAME_LOOT_TILE
from src.script.mobType.player import Player
logMSG("Loaded local dependency from script")

### INITIAL INPUTS HERE
GAME_MODE: str = "admin"

class Main:
    """Main class responsible for managing the game."""
    def __init__(self) -> None:
        """Initialize the game with specified tile size and settings.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            # Base initialization
            self.frame = 0

            # State
            self.state = "mainMenu"
            pygame.mouse.set_visible(False)

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
                   "main": loadImage("icon/main"),
                   "cursor": loadImage("icon/cursor")
                    }
            }
            
            # Main window, timer, camera offset
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.WINDOW: pygame.Surface = pygame.display.set_mode([STGS["windowWidth"], STGS["windowHeight"]])
            pygame.display.set_caption(FIX_STGS["windowName"])
            pygame.display.set_icon(self.assets["icon"]["main"])
            self.scroll: list[float] = [0, 0]
            logMSG("Created main window")

            # Tilemap
            self.assets["tile"] = loadTiles("tile")
            self.assets["tileBreakage"] = {int(key): resizeImage(surf, (STGS["tileSize"], STGS["tileSize"])) for key, surf in loadDirectory("tileBreakage").items()}
            logMSG("Loaded tile assets")

            self.tilemap: Tilemap = Tilemap(
                assets = self.assets,
                mapName = "map1")
            logMSG("Created tilemap")
            self.floatingItems: list[FloatingItem] = []

            # Clouds
            self.assets["cloud"] = loadImagesAsList("cloud")

            self.windSpeed: float = random.random() * 2 - 1
            logMSG(f"Starting wind speed: {round(self.windSpeed, 2)}")
            logMSG(f"Starting wind direction: {'west' if self.windSpeed < 0 else 'east'}")
            self.clouds = Clouds(self.assets["cloud"], count = 2 ** 4)
            logMSG("Generated clouds")

            # Player
            self.assets["mob"]["player"]["idle"] = Animation(loadImagesAsList("mob/player/idle"), imageDuration = 6)
            self.assets["mob"]["player"]["run"] = Animation(loadImagesAsList("mob/player/run"), imageDuration = 4)
            self.assets["mob"]["player"]["jump"] = Animation(loadImagesAsList("mob/player/jump"), imageDuration = STGS["FPS"] / 6)
            self.assets["mob"]["player"]["slide"] = Animation(loadImagesAsList("mob/player/slide"))
            self.assets["mob"]["player"]["wallSlide"] = Animation(loadImagesAsList("mob/player/wallSlide"))

            self.player: Player = Player(
                self.assets["mob"],
                pos = [STGS["windowWidth"] / 2, STGS["windowHeight"] / 2],
                gameMode = GAME_MODE)
            logMSG("Created player")

            # Particles
            self.assets["particle"]["leaf"] = Animation(loadImagesAsList("particle/leaf"), imageDuration = STGS["FPS"] // 2, loop = False)
            self.particles: list[Particle] = [] # List of all existing particles at a given moment

            # Any tile that spawns particles
            self.particleTilePairs: dict[str, list[tuple[str | int]]] = NAME_SPACE["idPairParticleSpawners"]

            # Any tile thats any variant spawns particles
            self.particleTiles: dict[str, list[str]] = NAME_SPACE["anyVariantParticleSpawners"]
            
            # Format: {"leaf": [rects], "": [rects]} ~ dict[particle] = rectsOfTilesThatEmit{particle}
            # This contains all the rects of tiles, that emit particles
            self.particleSpawnerTiles: dict[str, list[pygame.Rect]] = {}
            
            for particleStr, spawnerPairs in self.particleTilePairs.items():
                for spawner in self.tilemap.extract(spawnerPairs, keep=True):
                    if particleStr in self.particleSpawnerTiles:
                        self.particleSpawnerTiles[particleStr].append(pygame.Rect(spawner[0][0], spawner[0][1], STGS["tileSize"], STGS["tileSize"]))
                    else:
                        self.particleSpawnerTiles[particleStr] = [pygame.Rect(spawner[0][0], spawner[0][1], STGS["tileSize"], STGS["tileSize"])]

            for particleStr, blockList in self.particleTiles.items():
                for block in blockList:
                    for spawner in self.tilemap.extractAnyVariant(block, keep=True):
                        if particleStr in self.particleSpawnerTiles:
                            self.particleSpawnerTiles[particleStr].append(pygame.Rect(spawner[0][0], spawner[0][1], STGS["tileSize"], STGS["tileSize"]))
                        else:
                            self.particleSpawnerTiles[particleStr] = [pygame.Rect(spawner[0][0], spawner[0][1], STGS["tileSize"], STGS["tileSize"])]

            logMSG("Loaded and generated particles, and their respective spawning tiles")
            logMSG(f"Currently {sum([len(rectList) for rectList in self.particleSpawnerTiles.values()])} tiles emit particles")

            self.clicking: dict[str, bool] = {
                "left": False,
                "middle": False,
                "right": False,
                "up": False,
                "down": False
                }
            
            self.buttons: dict[str, dict[str, Button]] = {
                "mainGame": {
                    # Nothing here lol
                }, "mainGameInventory": {
                    "settings": Button(
                        pos = (STGS["windowWidth"] - FIX_STGS["GUI"]["outerWindowPadding"],
                            STGS["windowHeight"] - FIX_STGS["GUI"]["outerWindowPadding"]),
                        text = "Settings",
                        alignBy = "bottomRight"
                    )
                }, "mainMenu": {
                    "play": Button(
                        pos = (int(STGS["windowWidth"] * 0.5),
                            int(STGS["windowHeight"] * 0.5)),
                        text = "Play",
                        alignBy = "center"
                    ), "settings": Button(
                        pos = (int(STGS["windowWidth"] * 0.5),
                            int(STGS["windowHeight"] * 0.5) + FIX_STGS["GUI"]["mainMenu"]["buttonPadding"]),
                        text = "Settings",
                        alignBy = "center"
                    ), "exit": Button(
                        pos = (int(STGS["windowWidth"] * 0.5),
                            int(STGS["windowHeight"] * 0.5) + FIX_STGS["GUI"]["mainMenu"]["buttonPadding"] * 2),
                        text = "Exit",
                        alignBy = "center"
                    )
                }, "settings": {

                }, "mainGameSettings": {

                }
            }
            
        except Exception as e:
            logError(f"An error occurred during initialization: {e}")
            sys.exit(1)

    @staticmethod
    def exitApp() -> None:
        """Exit the application."""
        logSuccess("Successfully ran program")
        pygame.quit()
        sys.exit()

    def spawnFloatingItem(self, item: Item) -> None:
        """Spawn a floating item."""
        self.floatingItems.append(
            FloatingItem(
                [STGS["tileSize"] * (self.tilePosAtMouse[0] + 0.25),
                STGS["tileSize"] * (self.tilePosAtMouse[1] + 0.25)],
            item))
        # Set .velocity to a bit side so it has a curve TODO using random
        self.floatingItems[-1].velocity[1] = 0.2 + random.random() * 0.2
        self.floatingItems[-1].velocity[0] = (random.random() * 2 - 1)

    def setState(self, state: str) -> None:
        """Set the current state of the game."""
        self.state = state
        logMSG(f"Set state to \'{state}\'")

    def handleEvents(self) -> None:
        """Handle input game events."""
        self.mousePos: tuple[int] = pygame.mouse.get_pos()
        # pygame.key.get_pressed()[pygame.K_q]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitApp()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking["left"] = True

                    # Slot changing in inventory
                    if self.state == "mainGameInventory":
                        if self.player.inventory.doesHover(self.mousePos):
                            slotNum = self.player.inventory.getSlotNum(self.mousePos)

                            # This block of code is for when the player clicks on an item in the inventory
                            # In case the items are stackable in both the inventory slot and the cursor slot, and they have the same itemID:
                            # Put more stuff onto the cursor slot, so later the swapping puts it to the inventory slot
                            # Otherwise swapping is enough
                            if self.player.inventory.getItemByNum(slotNum) is not None:
                                if self.player.cursorSlot.getItem() is not None:
                                    if self.player.inventory.getItemByNum(slotNum).maxAmount != 1:
                                        if self.player.cursorSlot.getItem().maxAmount != 1:
                                            if self.player.cursorSlot.getItem().id == self.player.inventory.getItemByNum(slotNum).id:
                                                # Items are the same, they are stackable
                                                # So put the difference of # max amount ad slot amount # to the inventory slot
                                                #     In the end swapping, so it reverses the swap at the end

                                                diffToMaxInSlot: int = self.player.inventory.getItemByNum(slotNum).maxAmount - self.player.inventory.getItemByNum(slotNum).amount

                                                if diffToMaxInSlot >= self.player.cursorSlot.getItem().amount:
                                                    self.player.inventory.getItemByNum(slotNum).amount += self.player.cursorSlot.getItem().amount
                                                    self.player.cursorSlot.slot = None
                                                else:
                                                    self.player.inventory.getItemByNum(slotNum).amount = self.player.inventory.getItemByNum(slotNum).maxAmount
                                                    self.player.cursorSlot.slot.amount -= diffToMaxInSlot

                                                # Cursor item and slot item swich places
                                                self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)

                            # Cursor item and slot item swich places
                            self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)

                    # Changing states via buttons
                    for name, button in self.buttons[self.state].items():
                        if button.push(self.mousePos):
                            match self.state:
                                case "mainMenu":
                                    match name:
                                        case "play": self.setState("mainGame")
                                        case "settings": self.setState("settings")
                                        case "exit": self.exitApp()
                                        case _: logError("Unknow button fount in existing state: Ignoring this will have consequences")
                                case "mainGameInventory":
                                    match name:
                                        case "settings": self.setState("mainGameSettings")
                                        case _: logError("Unknow button fount in existing state: Ignoring this will have consequences")
                                case _:
                                    logError("Unknown button found in unknown state: Ignoring this may have consequences")

                if event.button == 2:
                    self.clicking["middle"] = True
                if event.button == 3:
                    self.clicking["right"] = True

                    # Slot changing in inventory
                    if self.state == "mainGameInventory":
                        if self.player.inventory.doesHover(self.mousePos):
                            slotNum = self.player.inventory.getSlotNum(self.mousePos)

                            if self.player.cursorSlot.getItem() is None:

                                if self.player.inventory.getItemByNum(slotNum) is None:
                                    logMSG("\'None\' with \'None\' lol")

                                elif self.player.inventory.getItemByNum(slotNum).maxAmount == 1:
                                    # Cursor item and slot item swich places
                                    self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)
                                    logMSG("Picked up \'non-stackable\' item")

                                else:
                                    if self.player.inventory.getItemByNum(slotNum).amount % 2 == 0:
                                        self.player.getInventory()[slotNum].amount = int(self.player.inventory.getItemByNum(slotNum).amount // 2)
                                        self.player.cursorSlot.slot = deepcopy(self.player.inventory.getItemByNum(slotNum))
                                    else:
                                        self.player.getInventory()[slotNum].amount = int(self.player.inventory.getItemByNum(slotNum).amount // 2) + 1
                                        self.player.cursorSlot.slot = deepcopy(self.player.inventory.getItemByNum(slotNum))
                                        self.player.cursorSlot.getItem().amount -= 1
                                        if self.player.cursorSlot.getItem().amount == 0:
                                            self.player.cursorSlot.slot = None
                                    logMSG("Picked up half of \'stackable\' item")
                            
                            elif self.player.cursorSlot.getItem().maxAmount == 1:

                                if self.player.inventory.getItemByNum(slotNum) is None:
                                    self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)
                                    logMSG("Put down \'non-stackable\' item")

                                elif self.player.inventory.getItemByNum(slotNum).maxAmount == 1:
                                    self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)
                                    logMSG("Swapped \'non-stackable\' items")

                                else:
                                    self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)
                                    logMSG("Put \'non-stackable\' itemin the place of \'stackable\' item")

                            else:

                                if self.player.inventory.getItemByNum(slotNum) is None:
                                    self.player.getInventory()[slotNum] = deepcopy(self.player.cursorSlot.slot)
                                    self.player.getInventory()[slotNum].amount = 1
                                    self.player.cursorSlot.slot.amount -= 1
                                    if self.player.cursorSlot.slot.amount == 0:
                                        self.player.cursorSlot.slot = None

                                    logMSG("Put down 1 \'stackable\' item to empty slot")

                                elif self.player.inventory.getItemByNum(slotNum).maxAmount == 1:
                                    self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)
                                    logMSG("Swapped \'non-stackable\' item with \'stackable\' items")

                                else:
                                    if self.player.inventory.getItemByNum(slotNum).id != self.player.cursorSlot.getItem().id:
                                        self.player.getInventory()[slotNum], self.player.cursorSlot.slot = self.player.cursorSlot.getItem(), self.player.inventory.getItemByNum(slotNum)
                                        logMSG("Swapped \'stackable\' items")
                                    else:
                                        # ItemIDs are the same

                                        if self.player.inventory.getItemByNum(slotNum).amount == self.player.inventory.getItemByNum(slotNum).maxAmount:
                                            # Item in inventpry is at max stack
                                            logMSG("Swapped \'stackable\' items")
                                        else:
                                            self.player.getInventory()[slotNum].amount += 1
                                            self.player.cursorSlot.slot.amount -= 1
                                            if self.player.cursorSlot.slot.amount == 0:
                                                self.player.cursorSlot.slot = None
                                            logMSG("Put 1 \'stackable\' item to inventory")

                if event.button == 4:
                    self.clicking["up"] = True

                    if self.state == "mainGame":
                        # Hotbar #Index# changing
                        self.player.hotbarNum = (self.player.hotbarNum - 1) % 10
                if event.button == 5:
                    self.clicking["down"] = True

                    if self.state == "mainGame":
                        # Hotbar #Index# changing
                        self.player.hotbarNum = (self.player.hotbarNum + 1) % 10

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
                    if self.state == "mainMenu":
                        self.exitApp()
                    elif self.state in ["mainGame", "mainGameInventory"]:
                        pass # Intentional
                    elif self.state == "settings":
                        self.setState("mainMenu")

                if event.key == pygame.K_a:
                    self.player.movementInput["left"] = True
                if event.key == pygame.K_d:
                    self.player.movementInput["right"] = True
                if event.key == pygame.K_w:
                    self.player.movementInput["up"] = True
                if event.key == pygame.K_s:
                    self.player.movementInput["down"] = True
                if event.key == pygame.K_SPACE:
                    if self.state in ["mainGame", "mainGameInventory"]:
                        self.player.jump()
                if event.key == pygame.K_TAB:
                    if self.state == "mainGameInventory":
                        self.setState("mainGame")
                    elif self.state == "mainGame":
                        self.setState("mainGameInventory")
                
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

        # Mouse movement based events
        if self.state in ["mainGame", "mainGameInventory"]:
            self.tilePosAtMouse = (int(self.mousePos[0] + self.scroll[0]) // STGS["tileSize"], int(self.mousePos[1] + self.scroll[1]) // STGS["tileSize"])
        
    def handleUpdates(self) -> None:
        """Update game state."""
        if self.state in ["mainGame", "mainGameInventory"]:

            # Camera movement
            self.scroll[0] += (self.player.pos[0] + self.player.width / 2  - STGS["windowWidth"] / 2 - self.scroll[0]) / STGS["FPS"] * 2
            self.scroll[1] += (self.player.pos[1] + self.player.height / 2  - STGS["windowHeight"] / 2 - self.scroll[1]) / STGS["FPS"] * 2
            self.renderScroll: tuple[int] = (int(self.scroll[0]), int(self.scroll[1]))

            # Player breaking tiles
            self.player.toolUsePenalty += 1

            if self.clicking["left"]:
                if self.tilemap.isTileAt(self.tilePosAtMouse):
                    if isinstance(self.player.getItemInHand(), Tool): # Tool in hand
                        if self.player.toolUsePenalty >= self.player.getItemInHand().useTime:

                            tile = self.tilemap.getTileAt(self.tilePosAtMouse)

                            if self.player.isAbleToBreak(block = tile["block"]): 
                                # Currenty you have the correct tool in hand

                                hitTileRect = pygame.Rect(self.tilePosAtMouse[0] * STGS["tileSize"], self.tilePosAtMouse[1] * STGS["tileSize"], STGS["tileSize"], STGS["tileSize"])

                                if tile["block"] in NAME_SPACE["instantMinedBlocks"]:
                                    tile["durability"] = 0

                                elif "durability" in tile:
                                    powerType = self.player.breakTileWith(block = tile["block"])

                                    # Already hit tile
                                    tile["durability"] -= self.player.getItemInHand().toolType[powerType]

                                else:
                                    powerType = self.player.breakTileWith(block = tile["block"])

                                    # Tile has full durability
                                    if tile["block"] in NAME_SPACE["durabilityOfTile"].keys():
                                        tile["durability"] = NAME_SPACE["durabilityOfTile"][tile["block"]]
                                    else:
                                        tile["durability"] = NAME_SPACE["durabilityOfTile"]["_"]
                                    tile["durability"] -= self.player.getItemInHand().toolType[powerType]

                                if tile["durability"] <= 0:
                                    self.tilemap.breakTile(self.tilePosAtMouse)

                                    # Spawn particles TODO

                                    # Pop an item TODO other cases
                                    if tile["block"] in SAME_LOOT_TILE.keys():
                                        self.spawnFloatingItem(deepcopy(SAME_LOOT_TILE[tile["block"]]))

                                    # Remove the tile formed as rect from particle spawners
                                    for key, rectList in self.particleSpawnerTiles.items():
                                        if hitTileRect in rectList:
                                            rectList.remove(hitTileRect)
                                    
                                    # Check for tile below/ at the broken tile TODO if it would spawn particles, and then append it accordingly

                                self.player.toolUsePenalty = 0
                            else:
                                if not self.frame % 10:
                                    logMSG("Other tool is required to break this tile")

            # Background
            self.clouds.update(windSpeed = self.windSpeed)

            # Particles
            # Spawn particles
            rectsOnWindow: list[pygame.Rect] = self.tilemap.getRectsOnWindow(self.WINDOW, self.renderScroll)
            for rect in rectsOnWindow:
                for particleStr, rects in self.particleSpawnerTiles.items():
                    if rect in rects:
                        if random.random() * 49999  * 4 < rect.width * rect.height:
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
            
            # Floating items
            for index, floatingItem in enumerate(self.floatingItems):
                floatingItem.update(self.tilemap, (self.player.pos[0] + self.player.pivot[0]+ self.player.hitBoxWidth / 2, self.player.pos[1] + self.player.pivot[1]+ self.player.hitBoxHeight / 2))
                if floatingItem.rect().colliderect(self.player.rect()):
                    item = self.player.inventory.addItem(floatingItem.item)
                    if item is None:
                        self.floatingItems.remove(floatingItem)
                    else:
                        self.floatingItems[index] = item

    def handleRender(self) -> None:
        """Render game elements."""
        if self.state == "mainMenu":
            # Background
            self.WINDOW.fill(NAME_SPACE["color"]["mainTheme"])
            self.WINDOW.blit(loadImageResized("icon/lolBG", (STGS["windowWidth"], STGS["windowHeight"])), (0, 0))
        
        elif self.state in ["mainGame", "mainGameInventory"]:
            # Background
            self.WINDOW.fill(NAME_SPACE["color"]["pink"])

            self.clouds.render(self.WINDOW, offset = self.renderScroll)

            # Tilemap
            self.tilemap.render(self.WINDOW, offset = self.renderScroll)

            # Mobs
            self.player.render(self.WINDOW, offset = self.renderScroll)

            # Particles
            for particle in self.particles:
                particle.render(self.WINDOW, offset = self.renderScroll)

            # Floating items
            for item in self.floatingItems:
                item.render(self.WINDOW, offset = self.renderScroll)

            # Inventory
            if self.state == "mainGame":
                self.player.inventory.renderHotbar(self.WINDOW, self.player.hotbarNum, mousePos = self.mousePos)

            elif self.state == "mainGameInventory":
                self.player.inventory.renderFullInventory(self.WINDOW, self.player.hotbarNum, mousePos = self.mousePos)
                self.player.cursorSlot.renderItemAtCursor(self.WINDOW, self.mousePos)

        else:
            # Unknown state
            self.WINDOW.fill(NAME_SPACE["color"]["mainTheme"])

            # Render das text
            renderText(
                self.WINDOW,
                (int(STGS["windowWidth"] // 2),
                int(STGS["windowHeight"] // 2)),
                "Unknown state",
                fontName = "arial",
                fontSize = 48)

        # Buttons
        for name, button in self.buttons[self.state].items():
            button.render(self.WINDOW, self.mousePos)

        # Cursor
        self.WINDOW.blit(self.assets["icon"]["cursor"], self.mousePos)
    
    def run(self) -> None:
        """Main game loop."""
        while True:
            self.handleEvents()
            self.handleUpdates()
            self.handleRender()

            self.clock.tick(STGS["FPS"])
            pygame.display.update()
            self.frame += 1

GAME: Main = Main()
GAME.run()
