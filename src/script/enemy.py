from src.script.animation import Animation
from src.script.mob import Mob
from src.script.item import Weapon

class Enemy(Mob):
    def __init__(self, assets: dict[str, dict[str, Animation]], pos: list[float], weapon: Weapon | None = None) -> None:
        super().__init__(species = "enemy",
            assets = assets,
            pos = pos)
        self.weapon: Weapon = weapon
