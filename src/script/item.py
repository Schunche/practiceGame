import pygame
import math

from dataclasses import dataclass, field

from src.script.loader import loadSysFont, NAME_SPACE, STGS
from src.fixData.itemSurface import ITEM_ICON, ITEM_IMAGE

@dataclass(repr = False)
class Item:
    """Basic item class"""
    id: int
    name: str
    description: str | None = field(default = None)
    useTime: int = field(default = int(STGS["FPS"] // 2))
    amount: int = field(default = 1)
    maxAmount: int = field(default = 2 ** 10)

    def getName(self) -> str:
        return self.name.title()
    
    def renderIcon(self, surface: pygame.Surface, pos: tuple[int]) -> None:
        surface.blit(ITEM_ICON[self.id], pos)

        # The amount number
        if self.maxAmount != 1:
            font: pygame.font = loadSysFont("arial")
            
            textRendered = font.render(str(self.amount), True, NAME_SPACE["color"]["mainText"])
            textRect: pygame.Rect = textRendered.get_rect()
            textRect.bottomright = (pos[0] + ITEM_ICON[self.id].get_width(), pos[1] + ITEM_ICON[self.id].get_height())

            surface.blit(textRendered, textRect)

@dataclass
class Weapon(Item):

    damage: int = field(default = 5) # This is strange
    knockback: int | None = field(default = 5)

@dataclass
class ReforgeableItem(Item):

    reforge: str | None = field(default = None)

    def __post_init__(self) -> None:
        self.amount: int = 1
        self.maxAmount: int = 1

    def getName(self) -> str:
        if self.reforge is None:
            return super().getName()
        return f"{self.reforge.title()} {super().getName()}"

@dataclass
class Tool(Item):

    toolType: dict[str, int] = field(default_factory = {"pickaxe": 5})

@dataclass
class SwingWeapon(Weapon, ReforgeableItem):

    def __post_init__(self) -> None:
        super().__post_init__()

        self.frame: int | None = None
        self.minAngle: float = math.pi * 2 / 3
        self.maxAngle: float = math.pi * 2 / 3 - math.pi

        """
        if self.frame is None:
            self.angle = None
        else:
            self.angle = self.minAngle + (self.maxAngle - self.minAngle) * self.frame
        """

@dataclass(kw_only = True)
class SwingTool(SwingWeapon, Tool):
    pass

@dataclass
class PlaceableItem(Item):
    def getName(self) -> str:
        return f"{super().getName()} (x{str(self.amount)})"

@dataclass(kw_only = True)
class Block(PlaceableItem):
    pass
