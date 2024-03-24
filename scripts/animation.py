class Animation:
    def __init__(self, images, imageDuration: int = 5, loop: bool = True) -> None:
        self.images = images
        self.loop: bool = loop
        self.imageDuration: int = imageDuration

        self.done: bool = False
        self.frame: int = 0
