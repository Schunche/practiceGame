from src.script.loader import loadImage, loadIcon, loadImageResized, STGS
from src.script.item import *

ITEM_ICON: dict = {
    0: loadIcon("tool/copperPickaxe"),
    1: loadIcon("tool/copperAxe"),
    2: loadIcon("tile/dirt/0"),
    3: loadIcon("tile/oakLog/0")
}

ITEM_IMAGE: dict = {
    0: loadImage("tool/copperPickaxe"),
    1: loadImage("tool/copperAxe"),
    2: loadImageResized("tile/dirt/0", (int(STGS["tileSize"] * 0.5), int(STGS["tileSize"] * 0.5))),
    3: loadImageResized("tile/oakLog/0", (int(STGS["tileSize"] * 0.5), int(STGS["tileSize"] * 0.5)))
}
