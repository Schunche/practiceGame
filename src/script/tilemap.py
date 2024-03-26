import pygame
import json

from src.script.log import logMSG, logError, logSuccess

NEIGHBOR_OFFSETS: list[tuple[int]] = [(i, j) for j in range(-2, 3) for i in range(-2, 3)]
PHYSICS_TILES: set[str] = {'dirt', 'stone', 'iron'}

class Tilemap:
    """
    A class representing a tilemap in a game.

    Attributes:
        assets (dict[str, dict[int, pygame.Surface]]): A dictionary mapping block names to dictionaries containing variant numbers and corresponding pygame.Surface objects.
        tileSize (int): The size of each tile in pixels.
        tilemap (dict[tuple[int], dict[str, str | int]]): A dictionary representing the tilemap, where keys are tuple coordinates and values are dictionaries containing block and variant information.
    """
    def __init__(self, assets: dict[str, dict[int, pygame.Surface]], tileSize: int = 32) -> None:
        """
        Initialize a Tilemap object.

        Args:
            assets (dict[str, dict[int, pygame.Surface]]): A dictionary mapping block names to dictionaries containing variant numbers and corresponding pygame.Surface objects.
            tileSize (int, optional): The size of each tile in pixels. Defaults to 32.
        """
        self.assets: dict[str, dict[int, pygame.Surface]] = assets
        self.tileSize: int = tileSize
        self.tilemap: dict[tuple[int], dict[str, str | int]] = {}

        self.loadMap(alias = "map1")

    def extract(self, id_pairs: tuple[str | int], keep: bool = False) -> list[list[int] | dict[str, str | int]]: # id_pairs:(block:str, variant:int)
        """
        Extract tiles matching specified block and variant pairs from the tilemap.

        Args:
            id_pairs (tuple[str | int]): A tuple containing block and variant pairs to match.
            keep (bool, optional): Flag indicating whether to keep extracted tiles in the tilemap. Defaults to False.

        Returns:
            list[list[int] | dict[str, str | int]]: A list of matched tiles, where each tile is represented as a list containing position coordinates and tile information.
        """
        matches: list[list[int] | dict[str, str | int]] = []
        for loc in self.tilemap:
            tile: dict[str, str | int] = self.tilemap[loc]
            if (tile['block'], tile['variant']) in id_pairs:
                matches.append([list(loc), tile.copy()])
                matches[-1][0] = matches[-1][0]
                matches[-1][0][0] *= self.tileSize
                matches[-1][0][1] *= self.tileSize
                if not keep:
                    del self.tilemap[loc]
        
        return matches

    def insertTile(self, pos: tuple[int], tile: dict[str, str | int]) -> None:
        """
        Insert a tile into the tilemap.

        Args:
            pos (tuple[int]): The position to insert the tile.
            tile (dict[str, str | int]): The tile information containing block and variant.
        """
        self.tilemap[pos] = tile

    def isTileAt(self, pos: tuple[int]) -> bool:
        """
        Check if there is a tile at the specified position.

        Args:
            pos (tuple[int]): The position to check.

        Returns:
            bool: True if there is a tile at the position, False otherwise.
        """
        return (pos in self.tilemap)
    
    def deleteTile(self, pos: tuple[int]) -> None:
        """
        Delete a tile from the tilemap.

        Args:
            pos (tuple[int]): The position of the tile to delete.
        """
        del self.tilemap[pos]

    def loadMap(self, alias: str = "map1") -> None:
        """
        Load a tilemap from a JSON file.

        Args:
            alias (str, optional): The alias of the tilemap to load. Defaults to "map1".
        """
        try:
            with open(f"src/data/map/{alias}.json", mode = "r") as file:
                strKeysTilemap: dict[str, dict[str, str | int]] = json.load(file)
        
            tupleKeysTilemap: dict[tuple[int], dict[str, str | int]] = {}
            for strKey, value in strKeysTilemap.items():
                keyParts: list[str] = strKey.split(";")
                key: tuple[int] = (int(keyParts[0]), int(keyParts[1]))
                tupleKeysTilemap[key] = value

            self.tilemap = tupleKeysTilemap

            logSuccess(f"\'{alias}.json\' found and loaded as map")
            logMSG(f"It currently has {len(self.tilemap)} tiles")
        
        except FileNotFoundError as e:
            logError(f"File \'{alias}.json\' not found.")
        
        except Exception as e:
            logError(f"Failed to decode JSON data in \'{alias}.json\'.")

    def saveMap(self, alias: str = "map1") -> None:
        """
        Save the current tilemap to a JSON file.

        Args:
            alias (str, optional): The alias of the tilemap to save. Defaults to "map1".
        """
        strKeysTilemap: dict[str, dict[str, str | int]] = {f"{key[0]};{key[1]}": value for key, value in self.tilemap.items()}

        with open(f"src/data/map/{alias}.json", mode = "w") as file:
            json.dump(strKeysTilemap, file, indent = 4)
    
    def tilesAround(self, pos: tuple[int]) -> list[dict[tuple[int], dict[str, str | int]]]:
        """
        Get tiles around the specified position.

        Args:
            pos (tuple[int]): The position to check.

        Returns:
            list[dict[tuple[int], dict[str, str | int]]]: A list of tiles around the specified position.
        """
        tiles: list[dict[tuple[int], dict[str, str | int]]] = []
        tileLocation: tuple[int] = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))
        for offset in NEIGHBOR_OFFSETS:
            checkLocation: tuple[int] = (tileLocation[0] + offset[0], tileLocation[1] + offset[1])
            if checkLocation in self.tilemap:
                tiles.append((checkLocation, self.tilemap[checkLocation]))
        return tiles
    
    def physicsRectsAround(self, pos: tuple[int]) -> list[dict[tuple[int], dict[str, str | int]]]:
        """
        Get physics rectangles around the specified position.

        Args:
            pos (tuple[int]): The position to check.

        Returns:
            list[dict[tuple[int], dict[str, str | int]]]: A list of physics rectangles around the specified position.
        """
        rects: list[pygame.Rect] = []
        for tile in self.tilesAround(pos):
            if tile[1]["block"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile[0][0] * self.tileSize, tile[0][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        """
        Render the tilemap on the given surface with an optional offset.

        Args:
            surface (pygame.Surface): The surface to render the tilemap on.
            offset (tuple[float], optional): The offset to apply to the tilemap's position. Defaults to (0, 0).
        """
        for x in range(offset[0] // self.tileSize - 1, (offset[0] + surface.get_width()) // self.tileSize + 1):
            for y in range(offset[1] // self.tileSize - 1, (offset[1] + surface.get_height()) // self.tileSize + 1):
                location: tuple[int] = (x, y)
                if location in self.tilemap:
                    tile: dict[str, str | int] = self.tilemap[location]
                    surface.blit(self.assets[tile["block"]][tile["variant"]], (location[0] * self.tileSize - offset[0], location[1] * self.tileSize - offset[1]))

    def getRectsOnWindow(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> dict[tuple[int], dict[str, str | int]]:
        """
        Get the rects of tiles visible on the given surface window.

        Args:
            surface (pygame.Surface): The surface representing the window.
            offset (tuple[float], optional): The offset position. Defaults to (0, 0).

        Returns:
            list[pygame.Rect]: A list of pygame.Rect objects representing the tiles visible on the window.
        """
        rects: list[pygame.Rect] = []
        for x in range(offset[0] // self.tileSize - 3, (offset[0] + surface.get_width()) // self.tileSize + 3):
            for y in range(offset[1] // self.tileSize - 3, (offset[1] + surface.get_height()) // self.tileSize + 3):
                location: tuple[int] = (x, y)
                if location in self.tilemap:
                    rects.append(pygame.Rect(
                        x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize
                    ))
        return rects
