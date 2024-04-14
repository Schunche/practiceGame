from src.script.item import *
from src.fixData.itemData import ITEM_DATA

# Loot tables here

# Breaking a tile, which gives back the exact same thing
SAME_LOOT_TILE: dict[str, Item] = {
    "dirt": ITEM_DATA[2],
    "oakLog": ITEM_DATA[3]
}
