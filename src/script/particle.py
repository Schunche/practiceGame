import pygame

from src.script.animation import Animation

class Particle:
    """
    A class representing a particle in a game.

    Attributes:
        species (str): The species of the particle.
        pos (list[float]): The position of the particle as a list containing x and y coordinates.
        velocity (list[float]): The velocity of the particle in the x and y directions.
        frame (int): The current frame of the particle's animation.
        animation (Animation): The animation object representing the particle's appearance.
    """

    def __init__(self, assets: dict[str, Animation], species: str, pos: list[float], velocity: list[float] = [0, 0], frame: int = 0) -> None:
        """
        Initialize a Particle object.

        Args:
            assets (dict[str, Animation]): A dictionary mapping species names to Animation objects representing different particle animations.
            species (str): The species of the particle.
            pos (list[float]): The initial position of the particle as a list containing x and y coordinates.
            velocity (list[float], optional): The initial velocity of the particle in the x and y directions. Defaults to [0, 0].
            frame (int, optional): The initial frame of the particle's animation. Defaults to 0.
        """
        self.species: str = species
        self.pos: list[float] = list(pos)
        self.velocity: list[float] = velocity
        self.frame: int = frame

        self.animation: Animation = assets[species].copy()
        self.animation.frame = frame

    def update(self) -> bool:
        """
        Update the particle's position and animation.

        Returns:
            bool: True if the particle is to be removed, False otherwise.
        """
        kill: bool = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill
    
    def render(self, surface: pygame.Surface, offset: list[int] = (0, 0)):
        """
        Render the particle on the given surface with an optional offset.

        Args:
            surface (pygame.Surface): The surface to render the particle on.
            offset (list[int], optional): The offset to apply to the particle's position. Defaults to (0, 0).
        """
        image: pygame.Surface = self.animation.img()
        surface.blit(image, (self.pos[0] - offset[0] - image.get_width() // 2, self.pos[1] - offset[1] - image.get_height() // 2))
