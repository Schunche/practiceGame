import pygame
import json

NEIGHBOR_OFFSETS: list[tuple[int]] = [(i, j) for j in range(-2, 3) for i in range(-2, 3)]
PHYSICS_TILES: dict[str] = {'dirt', 'stone'}

class Tilemap:
    def __init__(self, tileAssets: dict[str, pygame.Surface], tileSize: int = 32) -> None:
        self.tileAssets: dict[str, pygame.Surface] = tileAssets
        self.tileSize: int = tileSize
        self.tilemap = {(0, 0) : {"block" : "dirt", "variant" : 0}, (0, 2) : {"block" : "dirt", "variant" : 0}, (1, 5) : {"block" : "dirt", "variant" : 0}, (0, 4) : {"block" : "dirt","variant" : 0 }, (0, 5) : {"block" : "dirt", "variant" : 0}, (0, 3) : {"block" : "dirt", "variant" : 0}, (2, 2) : {"block" : "dirt", "variant" : 0}, (3, 6) : {"block" : "dirt", "variant" : 0}, (9, 9) : {"block" : "dirt", "variant" : 0}}
        self.saveMap()

    def saveMap(self) -> None:
        strKeysTilemap: dict[str, dict[str, str | int]] = {f"{key[0]};{key[1]}": value for key, value in self.tilemap.items()}

        with open(f"src/map/map1.json", mode = "w") as file:
            json.dump(strKeysTilemap, file, indent = 4)
    
    def tilesAround(self, pos) -> list[tuple[tuple[int], dict[str, str | int]]]:
        tiles: list[tuple[tuple[int], dict[str, str | int]]] = []
        tileLocation: tuple[int] = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))
        for offset in NEIGHBOR_OFFSETS:
            checkLocation: tuple[int] = (tileLocation[0] + offset[0], tileLocation[1] + offset[1]) # Revise if edited tileSystem tuple-> str
            if checkLocation in self.tilemap:
                tiles.append((checkLocation, self.tilemap[checkLocation]))
        return tiles
    
    def physicsRectsAround(self, pos) -> list[tuple[tuple[int], dict[str, str | int]]]:
        rects: list[pygame.Rect] = []
        for tile in self.tilesAround(pos):
            if tile[1]["block"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile[0][0] * self.tileSize, tile[0][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects

    def render(self, surface: pygame.Surface) -> None:
        # Not efficient render
        for location in self.tilemap:
            tile: dict[str, str | int] = self.tilemap[location]
            surface.blit(self.tileAssets[tile["block"] + str(tile["variant"]) + '.png'], (location[0] * self.tileSize, location[1] * self.tileSize))
