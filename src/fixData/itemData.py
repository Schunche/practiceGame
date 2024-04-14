from src.script.loader import loadImage
from src.script.item import *

ITEM_DATA: dict[int, Item] = {
    0: SwingTool(
        id = 0,
        name = "Copper Pickaxe",
        useTime = 25,
        toolType = {"pickaxe": 25},
        damage = 3,
        knockback = 2
    ), 1: SwingTool(
        id = 1,
        name = "Copper Axe",
        useTime = 40,
        toolType = {"axe": 30},
        damage = 4,
        knockback = 3
    ), 2: Block(
        id = 2,
        name = "Dirt Block"
    ), 3: Block(
        id = 3,
        name = "Oak Log"
    )
}
