class Settings:
    """
    A class to store game settings.

    Attributes:
        winWidth (int): The width of the game window. Defaults to 1280.
        winHeight (int): The height of the game window. Defaults to 720.
        FPS (int): The frames per second (FPS) of the game. Defaults to 60.
    """

    def __init__(self, winWidth: int = 1280, winHeight: int = 720, FPS: int = 60) -> None:
        """
        Initialize game settings.

        Args:
            winWidth (int, optional): The width of the game window. Defaults to 1280.
            winHeight (int, optional): The height of the game window. Defaults to 720.
            FPS (int, optional): The frames per second (FPS) of the game. Defaults to 60.
        """
        self.winWidth: int = winWidth
        self.winHeight: int = winHeight
        self.FPS: int = FPS
