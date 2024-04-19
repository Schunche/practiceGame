import pygame

from src.script.log import logMSG, logError, logSuccess
from src.script.loader import loadSysFont, NAME_SPACE, loadJson, STGS, FIX_STGS

from src.script.item import Item
from src.fixData.itemSurface import ITEM_ICON

# https://fonts.google.com/specimen/Pixelify+Sans?query=pixel

def renderText(surface: pygame.Surface, pos: tuple[int], text: str, color: str = "text", fontName: str = "arial", fontSize: int = 16) -> None:
    """
    Renders text to the specified surface.
    """
    font: pygame.font = loadSysFont(
        fontName,
        size = fontSize
    )
    textRendered: pygame.Surface = font.render(
        text,
        True,
        NAME_SPACE["color"][color]
    )
    textRect: pygame.Rect = textRendered.get_rect()
    textRect.center = (
        pos[0],
        pos[1]
    )
    surface.blit(
        textRendered,
        textRect
    )

class Button:
    def __init__(
        self,
        pos: tuple[int],
        text: str,
        *,
        size: tuple[int] = (FIX_STGS["GUI"]["standardButtonWidth"], FIX_STGS["GUI"]["standardButtonHeight"]),
        alignBy: str = "topLeft",
        solid: bool = True,
        innerColor: str = "buttonInner",
        textColor: str = "text",
        hoverColor: str = "buttonHover",
        borderColor: str = "buttonBorder",
        font: pygame.font = loadSysFont("arial"),
        borderWidth: int = FIX_STGS["GUI"]["buttonBorderWidth"],
        borderRadius: int = FIX_STGS["GUI"]["buttonBorderRadius"],
        ) -> None:
        
        """ TODO: solid
        Initializes a new instance of the `Button` class.
        """
        assert innerColor in NAME_SPACE["color"], f"Invalid background color: {innerColor}"
        assert textColor in NAME_SPACE["color"], f"Invalid text color: {textColor}"
        assert hoverColor in NAME_SPACE["color"], f"Invalid hover color: {hoverColor}"
        
        self.pos: tuple[int] = pos
        self.size: tuple[int] = size
        self.text: str  = text.title()
        self.innerColor: str = innerColor
        self.textColor: str = textColor
        self.borderColor: str = borderColor
        self.hoverColor: str = hoverColor
        self.font: pygame.font = font

        self.borderWidth: int = borderWidth
        self.borderRadius: int = borderRadius

        if alignBy == "topLeft":
            self.innerRect = pygame.Rect(
                self.pos[0],
                self.pos[1],
                self.size[0],
                self.size[1])
            self.borderRect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            self.textRendered = self.font.render(self.text, True, NAME_SPACE["color"][self.textColor])
            self.textRect = self.textRendered.get_rect()
            self.textRect.center = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

        elif alignBy == "center":
            self.innerRect = pygame.Rect(
                self.pos[0] - int(self.size[0] / 2),
                self.pos[1] - int(self.size[1] / 2),
                self.size[0] - self.borderWidth * 2,
                self.size[1] - self.borderWidth * 2
            )
            self.borderRect = pygame.Rect(
                self.pos[0] - self.borderWidth - int(self.size[0] / 2),
                self.pos[1] - self.borderWidth - int(self.size[1] / 2),
                self.size[0],
                self.size[1]
            )
            self.textRendered: pygame.Surface = self.font.render(
                self.text,
                True,
                NAME_SPACE["color"][self.textColor]
            )
            self.textRect: pygame.Rect = self.textRendered.get_rect()
            self.textRect.center = (
                self.pos[0],
                self.pos[1] - FIX_STGS["GUI"]["buttonTextVerticalOffError"]
            )

        elif alignBy == "bottomRight":
            self.innerRect = pygame.Rect(
                self.pos[0] - self.borderWidth - int(self.size[0] / 2),
                self.pos[1] - self.borderWidth - int(self.size[1] / 2),
                self.size[0] - self.borderWidth * 2,
                self.size[1] - self.borderWidth * 2
            )
            self.borderRect = pygame.Rect(
                self.pos[0] + self.borderWidth - int(self.size[0] / 2),
                self.pos[1] + self.borderWidth - int(self.size[1] / 2),
                self.size[0],
                self.size[1]
            )
            self.textRendered: pygame.Surface = self.font.render(
                self.text,
                True,
                NAME_SPACE["color"][self.textColor]
            )
            self.textRect: pygame.Rect = self.textRendered.get_rect()
            self.textRect.center = (
                self.pos[0],
                self.pos[1]
            )

        else:
            # Not implemented possibility will raise error
            raise ValueError("Invalid alignBy value")

    def push(self, mousePos: tuple[int]) -> bool:
        """
        Pushes the button.
        """
        if not self.borderRect.collidepoint(*mousePos):
            return False
        
        # Actual functionality here

        return True
        
    def render(self, surface: pygame.Surface, mousePos: tuple[int]) -> None:
        """
        Render the button to the specified surface.
        """

        isHovered: bool = False
        if self.borderRect.collidepoint(*mousePos):
            isHovered = True

        # Buttons inner color
        pygame.draw.rect(
            surface,
            NAME_SPACE["color"][self.hoverColor if isHovered else self.innerColor],
            self.innerRect
        )
        # Buttons border
        pygame.draw.rect(
            surface,
            NAME_SPACE["color"][self.borderColor],
            self.borderRect,
            width = self.borderWidth,
            border_radius = self.borderRadius
        )
        # Buttons text
        surface.blit(
            self.textRendered,
            self.textRect
        )

class Inventory:
    def __init__(self, *args) -> None:

        self.inventory: dict[int, Item] = {
            i: None for i in range(
                FIX_STGS["inventoryCol"] * FIX_STGS["inventoryRow"]
            )
        }
        for index, item in enumerate(args):
            self.inventory[index] = item

        innerRectSize: int = STGS["guiSize"] * 1.5
        self.innerRects: list[pygame.Rect] = [pygame.Rect(
            FIX_STGS["GUI"]["outerWindowPadding"] + (i % FIX_STGS["inventoryCol"]) * (innerRectSize + FIX_STGS["GUI"]["slotPadding"]),
            FIX_STGS["GUI"]["outerWindowPadding"] + (i // FIX_STGS["inventoryCol"]) * (innerRectSize + FIX_STGS["GUI"]["slotPadding"]),
            innerRectSize,
            innerRectSize
            ) for i in range(len(self.inventory))
        ]
        self.notHoveredInner = pygame.Surface((innerRectSize, innerRectSize), pygame.SRCALPHA)
        self.notHoveredInner.fill((*NAME_SPACE["color"]["buttonInner"], FIX_STGS["GUI"]["slotTransparency"]))

        self.hoveredInner = pygame.Surface((innerRectSize, innerRectSize), pygame.SRCALPHA)
        self.hoveredInner.fill((*NAME_SPACE["color"]["buttonHover"], FIX_STGS["GUI"]["slotTransparency"]))

        self.borderRects: list = [pygame.Rect(
            FIX_STGS["GUI"]["outerWindowPadding"] - FIX_STGS["GUI"]["slotBorderWidth"] + (i % FIX_STGS["inventoryCol"]) * (innerRectSize + FIX_STGS["GUI"]["slotPadding"]),
            FIX_STGS["GUI"]["outerWindowPadding"] - FIX_STGS["GUI"]["slotBorderWidth"] + (i // FIX_STGS["inventoryCol"]) * (innerRectSize + FIX_STGS["GUI"]["slotPadding"]),
            innerRectSize + 2 * FIX_STGS["GUI"]["slotBorderWidth"],
            innerRectSize + 2 * FIX_STGS["GUI"]["slotBorderWidth"]
            ) for i in range(len(self.inventory))
        ]

    def click(self, mousePos: tuple[int]) -> bool:
        # Placeholder
        if True:
            return False
        
        # Actual functionality here
        print("clicked")

        return True
    
    def getItemByNum(self, slotNum: int) -> Item | None:
        return self.inventory[slotNum]
    
    def isFull(self) -> bool:
        """Returns whether the  inventory is full"""
        if None in self.inventory.values():
            return False
        return True
        
    def renderHotbar(self, surface: pygame.Surface, hotbarNum: int, mousePos: tuple[int]) -> None:
        # Actual inventory
        for slotNum in range(10): # The number of slots in a row

            surface.blit(
                self.hoveredInner if self.borderRects[slotNum].collidepoint(mousePos) else self.notHoveredInner,
                self.innerRects[slotNum].topleft
            )
            #pygame.draw.rect(
            #    surface,
            #    NAME_SPACE["color"]["buttonHover" if self.borderRects[slotNum].collidepoint(mousePos) else "buttonInner"],
            #    self.innerRects[slotNum]
            #)
            pygame.draw.rect(
                surface,
                NAME_SPACE["color"]["hotbarSelectedBorder" if slotNum == hotbarNum else "buttonBorder"],
                self.borderRects[slotNum],
                width = FIX_STGS["GUI"]["buttonBorderWidth"],
                border_radius = FIX_STGS["GUI"]["buttonBorderRadius"]
            )
            
            item = self.inventory[slotNum]
            if item is not None:
                item.renderIcon(surface,
                    (int(self.innerRects[slotNum].x + self.innerRects[slotNum].w * 0.5 - STGS["guiSize"] * 0.5),
                    int(self.innerRects[slotNum].y + self.innerRects[slotNum].h * 0.5 - STGS["guiSize"] * 0.5))
                )

    def renderFullInventory(self, surface: pygame.Surface, hotbarNum: int, mousePos: tuple[int]) -> None:
        # Actual inventory
        for slotNum, item in self.inventory.items():
            pygame.draw.rect(
                surface,
                NAME_SPACE["color"]["buttonHover" if self.borderRects[slotNum].collidepoint(mousePos) else "buttonInner"],
                self.innerRects[slotNum]
            )
            pygame.draw.rect(
                surface,
                NAME_SPACE["color"]["hotbarSelectedBorder" if slotNum == hotbarNum else "buttonBorder"],
                self.borderRects[slotNum],
                width = FIX_STGS["GUI"]["buttonBorderWidth"],
                border_radius = FIX_STGS["GUI"]["buttonBorderRadius"]
            )
            
            item = self.inventory[slotNum]
            if item is not None:
                item.renderIcon(surface,
                    (int(self.innerRects[slotNum].x + self.innerRects[slotNum].w * 0.5 - STGS["guiSize"] * 0.5),
                    int(self.innerRects[slotNum].y + self.innerRects[slotNum].h * 0.5 - STGS["guiSize"] * 0.5))
                )
                
    def doesHover(self, mousePos: tuple[int]) -> bool:
        for slotNum, item in self.inventory.items():
            if self.borderRects[slotNum].collidepoint(mousePos):
                return True
        return False
    
    def getSlotNum(self, mousePos: tuple[int]) -> int | None:
        for slotNum, item in self.inventory.items():
            if self.borderRects[slotNum].collidepoint(mousePos):
                return slotNum
            
    def addItem(self, item: Item) -> Item | None:
        if item.maxAmount == 1:
            if self.isFull():
                return item
            else:
                for key, slot in self.inventory.items():
                    if slot is None:
                        self.inventory[item] = item
                        return None
        else: # Max amount > 1
            if not self.isFull():
                for key, slot in self.inventory.items():
                    if slot is None:
                        continue
                    if slot.id == item.id:
                        if slot.amount == slot.maxAmount:
                            continue

                        if slot.amount + item.amount <= slot.maxAmount:
                            slot.amount += item.amount
                            return None
                        else:
                            diff: int = slot.maxAmount - slot.amount
                            slot.amount = item.maxAmount
                            item.amount -= diff   
                # To this point filled up all duplicants

                # If it has no empty slots return item
                if self.isFull():
                    return item
                # So it has empty slots

                for key, slot in self.inventory.items():
                    if slot is None:
                        self.inventory[key] = item
                        return None
                # Put it to the empty slot

            else:
                # Inventory is full
                for key, slot in self.inventory.items():
                    if slot.id == item.id:
                        # Slot is full
                        if slot.amount == slot.maxAmount:
                            continue

                        # The rest can be put there
                        if slot.amount + item.amount <= slot.maxAmount:
                            slot.amount += item.amount
                            return None
                        else:
                            # Decrease with some amount
                            diff: int = slot.maxAmount - slot.amount
                            slot.amount = item.maxAmount
                            item.amount -= diff   
                # To this point filled up all duplicants

                # So there is some bonus amount
                return item
                # So it has empty slots

        logError("Not all cases have been covered, in inventory adding")

class CursorSlot:
    def __init__(self, item: Item | None = None) -> None:
        self.slot = item
    
    def isFull(self) -> bool:
        """Returns whether the slot has an item"""
        if self.slot is not None:
            return True
        return False
    
    def getItem(self) -> Item | None:
        """Returns the item the cursor contains"""
        return self.slot

    def renderItemAtCursor(self, surface: pygame.Surface, mousePos: tuple[int]) -> None:
        item = self.slot
        if item is not None:
            item.renderIcon(surface,
                (int(mousePos[0] - STGS["guiSize"] * 0.5),
                int(mousePos[1] - STGS["guiSize"] * 0.5)))
