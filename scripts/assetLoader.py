import os
import pygame

TRANSPARENT_COLOR = [255, 0, 254]

def loadImage(path) -> pygame.Surface:
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

def loadDirectory(path) -> dict[str, pygame.Surface]:
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

def loadImagesAsList(path) -> list[pygame.Surface]:
    """AKA potato mode"""
    images = []
    for imageName in sorted(os.listdir(path)):
        images.append(loadImage(path + "/" + imageName))
    return images

def loadTiles(path) -> dict[str | int, pygame.Surface]:
    """
    Load images from a directory.

    Args:
        path (str): The path to the directory containing images.

    Returns:
        dict[str, pygame.Surface]: A dictionary containing image names and their corresponding surfaces.
    """
    tiles: dict[str, dict[int, pygame.Surface]] = {}
    for block in os.listdir(path):
        if not block in tiles:
            tiles[block] = {}
        for variant in os.listdir(f"{path}/{block}"):
            tiles[block][int(variant[:variant.index('.')])] = loadImage(f"{path}/{block}/{variant}")
    return tiles
