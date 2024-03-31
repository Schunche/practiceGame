import json
import os
import pygame

from typing import Any

def loadJson(path: str) -> Any:
    """
    Arguments:
        path (str): directory path from 'src/' to '.json' WITHOUT the said
    
    Returns:
        Any: the json file
    """
    with open(f"src/{path}.json", "r") as file:
        returnFile = json.load(file)
    return returnFile

NAME_SPACE = loadJson("fixData/nameSpace")
TRANSPARENT_COLOR: list[int] = NAME_SPACE["color"]["toBeTransparent"]

def loadImage(path: str) -> pygame.Surface:
    """
    Load an image from a file.

    Args:
        path (str): The path to the image file.

    Returns:
        pygame.Surface: The loaded image.
    """
    image: pygame.Surface = pygame.image.load(path)
    image.set_colorkey(TRANSPARENT_COLOR)
    return image

def loadImageResized(path: str, tileSize: int) -> pygame.Surface:
    """
    Load an image from a file.

    Args:
        path (str): The path to the image file.

    Returns:
        pygame.Surface: The loaded image.
    """
    image: pygame.Surface = pygame.image.load(path)
    returnImage: pygame.Surface = pygame.transform.scale(image, (tileSize, tileSize))
    returnImage.set_colorkey(TRANSPARENT_COLOR)
    return returnImage

def loadDirectory(path: str) -> dict[str, pygame.Surface]:
    """
    Load images from a directory.

    Args:
        path (str): The path to the directory containing images.

    Returns:
        dict[str, pygame.Surface]: A dictionary containing image names and their corresponding surfaces.
    """
    images: dict[str, pygame.Surface] = {}
    for imageName in os.listdir(path):
        images[imageName] = loadImage(f"{path}/{imageName}")#loadImage(os.path.join(path, imageName))
    return images

def loadImagesAsList(path: str) -> list[pygame.Surface]:
    """
    Load images from a directory into a list of pygame Surface objects.

    Args:
        path (str): The directory path containing the images.

    Returns:
        list[pygame.Surface]: A list of pygame Surface objects representing the loaded images.
    """
    images: list[pygame.Surface] = []
    for imageName in sorted(os.listdir(path)):
        images.append(loadImage(path + "/" + imageName))
    return images

def loadTiles(path: str) -> dict[int, pygame.Surface]:
    """
    Load tiles from a directory structure into a dictionary of pygame Surface objects.

    Args:
        path (str): The directory path containing the tile images organized by block and variant.

    Returns:
        dict[str, dict[int, pygame.Surface]]: A dictionary mapping block names or variant numbers to pygame Surface objects representing the loaded tiles.
    """
    tiles: dict[str, dict[int, pygame.Surface]] = {}
    for block in os.listdir(path):
        if not (block in tiles):
            tiles[block] = {}
        for variant in os.listdir(f"{path}/{block}"):
            tiles[block][int(variant[:variant.index('.')])] = loadImage(f"{path}/{block}/{variant}")
    return tiles

def loadTilesResized(path: str, tileSize: int) -> dict[str, pygame.Surface]:
    """
    Load tiles from a directory structure into a dictionary of pygame Surface objects.

    Args:
        path (str): The directory path containing the tile images organized by block and variant.

    Returns:
        dict[str, dict[int, pygame.Surface]]: A dictionary mapping block names or variant numbers to pygame Surface objects representing the loaded tiles.
    """
    tiles: dict[str, dict[int, pygame.Surface]] = {}
    for block in os.listdir(path):
        tiles[block[:block.index('.')]] = loadImageResized(f"{path}/{block}", tileSize = tileSize)
    return tiles

def getBit(block: str = "_") -> str:
    if block == "_":
        return "_"
    for key, value in NAME_SPACE["bitForm"].items():
        if block in value:
            return key
    return "_"
