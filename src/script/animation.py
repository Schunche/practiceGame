import pygame

from typing import Self

class Animation:
    """
    A class to represent an animation consisting of a sequence of images.

    Attributes:
        images (List[pygame.Surface]): List of pygame Surface objects representing each frame of the animation.
        imageDuration (int): Duration (in frames) each image is displayed. Defaults to 5 frames.
        loop (bool): Determines if the animation should loop. Defaults to True.
        done (bool): Flag indicating if the animation has finished playing.
        frame (int): Current frame of the animation.
    """
    def __init__(self, images: list[pygame.Surface], imageDuration: int = 5, loop: bool = True) -> None:
        """
        Initialize the Animation object.

        Args:
            images (List[pygame.Surface]): List of pygame Surface objects representing each frame of the animation.
            imageDuration (int, optional): Duration (in frames) each image is displayed. Defaults to 5 frames.
            loop (bool, optional): Determines if the animation should loop. Defaults to True.
        """
        self.images = images
        self.imageDuration: int = imageDuration
        self.loop: bool = loop

        self.done: bool = False
        self.frame: int = 0

    def copy(self) -> Self: # -> Animation
        """
        Create a copy of the Animation object.

        Returns:
            Animation: A new Animation object with the same attributes as the original.
        """
        return Animation(self.images, self.imageDuration, self.loop)
    
    def update(self) -> None:
        """
        Update the animation frame.

        If loop is True, the animation loops continuously.
        If loop is False, the animation stops when it reaches the last frame.
        """
        if self.loop:
            self.frame = (self.frame + 1) % (self.imageDuration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.imageDuration * len(self.images) - 1)
            if self.frame >= self.imageDuration * len(self.images) - 1:
                self.done = True

    def img(self) -> pygame.Surface:
        """
        Get the current frame of the animation.

        Returns:
            pygame.Surface: The pygame Surface representing the current frame of the animation.
        """
        return self.images[int(self.frame / self.imageDuration)]
