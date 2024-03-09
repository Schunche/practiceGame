class Mob: # Player, Enemies # Hopefully not used directly
    def __init__(self) -> None:
        self.pos: list[float] = [72, 0]

        self.width: int = 48
        self.height: int = 48
        self.pivot: list[int] = [0, 0] # Vector from TopLeft of posxy to TopLeft of hitboxWH
        self.hitBoxWidth: int = 48
        self.hitBoxHeight: int = 48
