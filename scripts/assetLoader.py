import os
import pygame

def loadImage(path) -> pygame.Surface:
    """
    Load an image from a file.

    Args:
        path (str): The path to the image file.

    Returns:
        pygame.Surface: The loaded image.
    """
    image: pygame.Surface = pygame.image.load(path)
    image.set_colorkey([23, 23, 32])
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
        images[imageName] = loadImage(os.path.join(path, imageName))
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
