class Mob:
    """
    Represents a mobile entity in the game, such as a player or an enemy.

    Note: This class is intended to be subclassed to create specific types of mobile entities.
    Direct instantiation of this class is discouraged.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the Mob class.

        Attributes:
            pos (list[float]): The position of the mob on the game screen. Default is [72, 0].
            width (int): The width of the mob's sprite. Default is 48.
            height (int): The height of the mob's sprite. Default is 48.
            pivot (tuple[int]): The offset from the top-left corner of the sprite to the top-left corner of its hitbox. Default is [0, 0].
            hitBoxWidth (int): The width of the mob's hitbox. Default is 48.
            hitBoxHeight (int): The height of the mob's hitbox. Default is 48.
        """
        self.pos: list[float] = [72, 0]
        self.width: int = 48
        self.height: int = 48

        self.pivot: tuple[int] = (0, 0)  # Vector from TopLeft of posxy to TopLeft of hitboxWH
        self.hitBoxWidth: int = 48
        self.hitBoxHeight: int = 48
