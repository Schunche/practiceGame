import pygame
import json
from scripts.log import logMSG
from scripts.log import logError

NEIGHBOR_OFFSETS: list[tuple[int]] = [(i, j) for j in range(-2, 3) for i in range(-2, 3)]
PHYSICS_TILES: dict[str] = {'dirt', 'stone', 'iron'}

class Tilemap:
    """
    A class representing the tilemap of the game world.

    Attributes:
        assets (dict[str, pygame.Surface]): Dictionary mapping tile names to their corresponding pygame surfaces.
        tileSize (int): The size of each tile in pixels.
        tilemap (dict[tuple[int], dict[str, str | int]]): Dictionary representing the tilemap data.
    """
    def __init__(self, assets: dict[str, pygame.Surface], tileSize: int = 32) -> None:
        """
        Initialize the Tilemap object.

        Args:
            assets (dict[str, pygame.Surface]): Dictionary of tile assets.
            tileSize (int, optional): Size of each tile in pixels. Defaults to 32.
        """
        self.assets: dict[str, dict[int, pygame.Surface]] = assets
        self.tileSize: int = tileSize
        self.tilemap: dict[tuple[int], dict[str, str | int]] = {}

        self.loadMap(alias = "map1")

    def extract(self, id_pairs, keep=False):
        matches = []
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['block'], tile['variant']) in id_pairs:
                matches.append([list(loc), tile.copy()])
                matches[-1][0] = matches[-1][0]
                matches[-1][0][0] *= self.tileSize
                matches[-1][0][1] *= self.tileSize
                if not keep:
                    del self.tilemap[loc]
        
        return matches

    def insertTile(self, pos: tuple[int], tile: dict[str, str | int]) -> None:
        self.tilemap[pos] = tile

    def isTileAt(self, pos: tuple[int]) -> bool:
        return (pos in self.tilemap)
    
    def deleteTile(self, pos: tuple[int]) -> None:
        del self.tilemap[pos]

    def loadMap(self, alias: str = "map1") -> None:
        """
        Load the tilemap data from a JSON file.

        Args:
            alias (str, optional): The alias of the map file. Defaults to "map1".
        """
        try:
            with open(f"src/map/{alias}.json", mode = "r") as file:
                strKeysTilemap: dict[str, dict[str, str | int]] = json.load(file)
        
            tupleKeysTilemap: dict[tuple[int], dict[str, str | int]] = {}
            for strKey, value in strKeysTilemap.items():
                keyParts: list[str] = strKey.split(";")
                key: tuple[int] = (int(keyParts[0]), int(keyParts[1]))
                tupleKeysTilemap[key] = value

            self.tilemap = tupleKeysTilemap

            logMSG(f"\'{alias}.json\' loaded")
        
        except FileNotFoundError as e:
            logError(f"File \'{alias}.json\' not found.")
        
        except Exception as e:
            logError(f"Failed to decode JSON data in \'{alias}.json\'.")

    def saveMap(self, alias: str = "map1") -> None:
        """
        Save the tilemap data to a JSON file.

        Args:
            alias (str, optional): The alias of the map file. Defaults to "map1".
        """
        strKeysTilemap: dict[str, dict[str, str | int]] = {f"{key[0]};{key[1]}": value for key, value in self.tilemap.items()}

        with open(f"src/map/{alias}.json", mode = "w") as file:
            json.dump(strKeysTilemap, file, indent = 4)
    
    def tilesAround(self, pos: tuple[int]) -> list[tuple[tuple[int], dict[str, str | int]]]:
        """
        Get tiles around a given position.

        Args:
            pos (tuple[int]): The position for which neighboring tiles are to be found.

        Returns:
            list[tuple[tuple[int], dict[str, str | int]]]: List of neighboring tiles.
        """
        tiles: list[tuple[tuple[int], dict[str, str | int]]] = []
        tileLocation: tuple[int] = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))
        for offset in NEIGHBOR_OFFSETS:
            checkLocation: tuple[int] = (tileLocation[0] + offset[0], tileLocation[1] + offset[1])
            if checkLocation in self.tilemap:
                tiles.append((checkLocation, self.tilemap[checkLocation]))
        return tiles
    
    def physicsRectsAround(self, pos) -> list[tuple[tuple[int], dict[str, str | int]]]:
        """
        Get collision rectangles around a given position.

        Args:
            pos: The position for which collision rectangles are to be found.

        Returns:
            list[pygame.Rect]: List of collision rectangles.
        """
        rects: list[pygame.Rect] = []
        for tile in self.tilesAround(pos):
            if tile[1]["block"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile[0][0] * self.tileSize, tile[0][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects

    def render(self, surface: pygame.Surface, offset: list[float] = [0, 0]) -> None:
        """
        Render the tilemap on a given surface.

        Args:
            surface (pygame.Surface): The surface onto which the tilemap will be rendered.
            offset (list[float], optional): The offset from the top-left corner of the surface. Defaults to [0, 0].
        """
        for x in range(offset[0] // self.tileSize - 1, (offset[0] + surface.get_width()) // self.tileSize + 1):
            for y in range(offset[1] // self.tileSize - 1, (offset[1] + surface.get_height()) // self.tileSize + 1):
                location: tuple[int] = (x, y)
                if location in self.tilemap:
                    tile: dict[str, str | int] = self.tilemap[location]
                    surface.blit(self.assets[tile["block"]][tile["variant"]], (location[0] * self.tileSize - offset[0], location[1] * self.tileSize - offset[1]))
