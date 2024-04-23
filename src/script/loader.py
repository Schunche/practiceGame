import json
import os
import pygame
import math

from typing import Any

from src.script.log import logMSG, logError, logSuccess

def loadJson(path: str) -> Any:
    """
    Arguments:
        path (str): directory path from 'src/' to '.json' WITHOUT the said
    
    Returns:
        Any: the json file
    """
    try:
        with open(f"src/{path}.json", "r") as file:
            returnFile = json.load(file)
            logMSG(f"\'src/{path}.json\' found and loaded")
        return returnFile
    
    except FileNotFoundError as e:
        logError(f"\'src/{path}.json\' not found: {e}")
        return None
    
    except UnicodeDecodeError as e:
        logError(f"\'src/{path}.json\' is not a valid JSON file: {e}")
        return None
    
    except Exception as e:
        logError(f"\'src/{path}.json\' failed to load: {e}")
        return None

STGS = loadJson("data/settings")
FIX_STGS: dict = loadJson("fixData/fixSettings")

NAME_SPACE = loadJson("fixData/nameSpace")
TRANSPARENT_COLOR: list[int] = NAME_SPACE["color"]["toBeTransparent"]

def loadImage(path: str) -> pygame.Surface:
    """
    Loads a '.png' image from a file.

    Args:
        path (str): The path to the image file: from 'src/img/' to '.png' WITHOUT the said

    Returns:
        pygame.Surface: The loaded image.
    """
    try:
        img: pygame.Surface = pygame.image.load(f"src/img/{path}.png")
        img.set_colorkey(TRANSPARENT_COLOR)
        return img
    
    except FileNotFoundError as e:
        logError(f"\'src/img/{path}.png\' not found: {e}")
        return loadImage("icon/_")
    
    except Exception as e:
        logError(f"\'src/img/{path}.png\' failed to load: {e}")
        return loadImage("icon/_")
        
def loadImageResized(path: str, size: tuple[int]) -> pygame.Surface:
    """
    Load an image from a file, and resizes it.

    Args:
        path (str): The path to the image file.
        size (tuple[int]): The new size of the image file.

    Returns:
        pygame.Surface: The resized image.
    """
    assert size[0] > 0 and size[1] > 0, "The new size must be an integer greater than 0"

    img: pygame.Surface = loadImage(path)
    returnImage: pygame.Surface = pygame.transform.scale(
        img,
        (size[0],
        size[1])
    )
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
    for imageName in os.listdir(f"src/img/{path}"):
        images[imageName[:imageName.index('.')]] = loadImage(
            f"{path}/{imageName[:imageName.index('.')]}"
        )
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
    for imageName in sorted(os.listdir(f"src/img/{path}")):
        images.append(
            loadImage(
                f"{path}/{imageName[:imageName.index('.')]}"
            )
        )
    return images

def loadTiles(path: str) -> dict[int, pygame.Surface]:
    """
    Load tiles from a directory structure into a dictionary of pygame Surface objects.
    Resized by default

    Args:
        path (str): The directory path containing the tile images organized by block and variant.

    Returns:
        dict[str, dict[int, pygame.Surface]]: A dictionary mapping block names or variant numbers to pygame Surface objects representing the loaded tiles.
    """
    tiles: dict[str, dict[int, pygame.Surface]] = {}
    for block in os.listdir(f"src/img/{path}"):
        if block not in tiles:
            tiles[block] = {}
        for variant in os.listdir(f"src/img/{path}/{block}"):
            tiles[block][int(variant[:variant.index('.')])] = loadImageResized(
                f"{path}/{block}/{variant[:variant.index('.')]}",
                (STGS["tileSize"],
                STGS["tileSize"])
            )

    return tiles

def getBit(block: str = "_") -> str:
    # key <- value
    if block == "_":
        return "_"
    for key, value in NAME_SPACE["bitForm"].items():
        if block in value:
            return key
    return "_"

def loadSysFont(name: str, size: int = 16, bold: bool = False, italic: bool = False) -> pygame.font:
    return pygame.font.SysFont(
        name = name,
        size = size,
        bold = bold,
        italic = italic
    )

def loadIcon(path: str) -> pygame.Surface:
    """
    Load an icon from a file.
    """
    return loadImageResized(path, (STGS["guiSize"], STGS["guiSize"]))

def resizeImage(image: pygame.Surface, size: tuple[int]) -> pygame.Surface:
    """
    Resize an image.
    """
    return pygame.transform.scale(image, size)
