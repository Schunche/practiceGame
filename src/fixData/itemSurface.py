from src.script.loader import loadImage, loadIcon
from src.script.item import *

ITEM_ICON: dict = {
    0: loadIcon("tool/copperPickaxe"),
    1: loadIcon("tool/copperAxe"),
    2: loadIcon("tile/dirt/0"),
    3: loadIcon("tile/oakLog/0")
}

ITEM_IMAGE: dict = {
    0: loadImage("src/img/tool/copperPickaxe.png"),
    1: loadImage("src/img/tool/copperAxe.png"),
    2: loadImage("src/img/tile/dirt/0.png"),
    3: loadImage("src/img/tile/oakLog/0.png")
}
