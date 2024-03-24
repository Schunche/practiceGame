class Settings:
    """
    A class to store game settings.

    Attributes:
        winWidth (int): The width of the game window. Defaults to 1280.
        winHeight (int): The height of the game window. Defaults to 720.
        FPS (int): The frames per second (FPS) of the game. Defaults to 60.
    """

    def __init__(self, winW: int = 1280, winH: int = 720, FPS: int = 60) -> None:
        """
        Initialize game settings.

        Args:
            winW (int, optional): The width of the game window. Defaults to 1280.
            winH (int, optional): The height of the game window. Defaults to 720.
            FPS (int, optional): The frames per second (FPS) of the game. Defaults to 60.
        """
        self.winWidth: int = winW
        self.winHeight: int = winH
        self.FPS: int = FPS
