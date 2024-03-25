import random
import pygame

class Cloud:
    """
    A class representing a cloud in a side-scrolling game.

    Attributes:
        pos (list[float]): The position of the cloud as a list containing x and y coordinates.
        img (pygame.Surface): The image representing the cloud.
        speed (float): The speed at which the cloud moves horizontally.
        depth (float): The depth of the cloud, affecting its parallax scrolling effect.
    """
    def __init__(self, pos: list[float], img: pygame.Surface, speed: float, depth: float) -> None:
        """
        Initialize a Cloud object.

        Args:
            pos (list[float]): The position of the cloud as a list containing x and y coordinates.
            img (pygame.Surface): The image representing the cloud.
            speed (float): The speed at which the cloud moves horizontally.
            depth (float): The depth of the cloud, affecting its parallax scrolling effect.
        """
        self.pos: list[float] = list(pos)
        self.img: pygame.Surface = img
        self.speed: float = speed
        self.depth: float = depth

    def update(self) -> None:
        """Update the position of the cloud based on its speed."""
        self.pos[0] += self.speed

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        """
        Render the cloud on the given surface with optional offset.

        Args:
            surface (pygame.Surface): The pygame surface to render the cloud on.
            offset (tuple[float], optional): The offset to apply to the cloud's position. Defaults to (0, 0).
        """
        renderPos: tuple[float] = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surface.blit(self.img, (renderPos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(), renderPos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    """
    A class representing a collection of clouds in a side-scrolling game.

    Attributes:
        clouds (list[Cloud]): List of Cloud objects representing the clouds in the scene.
    """
    def __init__(self, cloudImages: list[pygame.Surface], count: int = 2^4) -> None:
        """
        Initialize Clouds object with random clouds.

        Args:
            cloudImages (list[pygame.Surface]): List of pygame Surface objects representing different cloud images.
            count (int, optional): The number of clouds to generate. Defaults to 16.
        """
        self.clouds: list[Cloud] = []

        for _ in range(count):
            self.clouds.append(Cloud(
                (random.random() * 99999, random.random() * 99999),
                random.choice(cloudImages),
                random.random() * 0.05 + 0.05,
                random.random() * 0.6 + 0.2))
            
        self.clouds.sort(key = lambda x: x.depth)

    def update(self) -> None:
        """Update the position of all clouds."""
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface: pygame.Surface, offset: tuple[float] = (0, 0)) -> None:
        """
        Render all clouds on the given surface with optional offset.

        Args:
            surface (pygame.Surface): The pygame surface to render the clouds on.
            offset (tuple[float], optional): The offset to apply to the clouds' positions. Defaults to (0, 0).
        """
        for cloud in self.clouds:
            cloud.render(surface, offset = offset)
