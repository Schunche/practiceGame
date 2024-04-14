import pygame

from src.script.log import logMSG
from src.script.loader import loadSysFont, NAME_SPACE, loadJson, STGS

from src.script.item import Item
from src.fixData.itemSurface import ITEM_ICON

# https://fonts.google.com/specimen/Pixelify+Sans?query=pixel

def renderText(surface: pygame.Surface, pos: tuple[int], text: str, color: str = "mainText", fontName: str = "arial", fontSize: int = 16) -> None:
    """
    Renders text to the specified surface.
    """
    font: pygame.font = loadSysFont(fontName, size = fontSize)

    textRendered: pygame.Surface = font.render(text, True, NAME_SPACE["color"][color])
    textRect: pygame.Rect = textRendered.get_rect()
    textRect.center = (pos[0], pos[1])
    surface.blit(textRendered, textRect)

class Button:
    def __init__(self, pos: tuple[int], size: tuple[int], text: str, solid: bool, *, bgColor: str = "mainButton", textColor: str = "mainText", hoverColor: str = "mainButtonHover", borderColor: str = "mainButtonBorder", font: pygame.font = loadSysFont("arial"), borderWidth: int = 4, borderRadius: int = 4) -> None:
        """ TODO: solid
        Initializes a new instance of the `Button` class.
        
        Args:
            pos (tuple[int]): The position of the button on the screen.
            size (tuple[int]): The size of the button.
            text (str): The text to display on the button.
            bgColor (str, optional): The background color of the button. Defaults to (255, 255, 255).
            textColor (str, optional): The color of the text on the button. Defaults to (0, 0, 0).
            hoverColor (str, optional): The color of the button when the mouse hovers over it. Defaults to (100, 100, 100).
        """
        if bgColor not in NAME_SPACE["color"]:
            raise ValueError(f"Invalid background color: {bgColor}")
        if textColor not in NAME_SPACE["color"]:
            raise ValueError(f"Invalid text color: {textColor}")
        if hoverColor not in NAME_SPACE["color"]:
            raise ValueError(f"Invalid hover color: {hoverColor}")
        
        self.pos: tuple[int] = pos
        self.size: tuple[int] = size
        self.text: str  = text.title()
        self.bgColor: str = bgColor
        self.textColor: str = textColor
        self.borderColor: str = borderColor
        self.hoverColor: str = hoverColor
        self.font: pygame.font = font

        self.borderWidth: int = borderWidth
        self.borderRadius: int = borderRadius

        isHovered: bool = False

        self.innerRect = pygame.Rect(
            self.pos[0] + self.borderRadius,
            self.pos[1] + self.borderRadius,
            self.size[0] - self.borderWidth * 2,
            self.size[1] - self.borderWidth * 2,)
        self.baseRect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.textRendered = self.font.render(self.text, True, NAME_SPACE["color"][self.textColor])
        self.textRect = self.textRendered.get_rect()
        self.textRect.center = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)

    def push(self, mousePos: tuple[int]) -> bool:
        """
        Pushes the button.
        """
        if not self.baseRect.collidepoint(*mousePos):
            return False
        
        # Actual functionality here

        return True
        
    def render(self, surface: pygame.Surface, mousePos: tuple[int]) -> None:
        """
        Render the button to the specified surface.
        """


        isHovered = False
        if self.baseRect.collidepoint(*mousePos):
            isHovered = True

        if isHovered:
            pygame.draw.rect(surface, NAME_SPACE["color"][self.hoverColor], self.innerRect)
            pygame.draw.rect(surface, NAME_SPACE["color"][self.borderColor], self.baseRect,
                width = self.borderWidth, border_radius = self.borderRadius)
        else:
            pygame.draw.rect(surface, NAME_SPACE["color"][self.bgColor], self.innerRect)
            pygame.draw.rect(surface, NAME_SPACE["color"][self.borderColor], self.baseRect,
                width = self.borderWidth, border_radius = self.borderRadius)
        surface.blit(self.textRendered, self.textRect)

class Inventory:
    def __init__(self, *args) -> None:

        self.inventory: dict[int, Item] = {
            i: None for i in range(10 * 5)}
        for index, item in enumerate(args):
            self.inventory[index] = item

        innerRectSize: int = STGS["guiSize"] * 1.5 - STGS["border"]
        self.innerRects: list = [pygame.Rect(
            int(STGS["border"] * 1.5 + (i % 10) * (innerRectSize + STGS["border"] * 2)),
            int(STGS["border"] * 1.5 + (i // 10) * (innerRectSize + STGS["border"] * 2)),
            innerRectSize,
            innerRectSize) for i in range(len(self.inventory))]
        self.baseRects: list = [pygame.Rect(
            int(STGS["border"] + (i % 10) * (STGS["guiSize"] * 1.5 + STGS["border"])),
            int(STGS["border"] + (i // 10) * (STGS["guiSize"] * 1.5 + STGS["border"])),
            STGS["guiSize"] * 1.5 - 2 // STGS["border"],
            STGS["guiSize"] * 1.5 - 2 // STGS["border"]) for i in range(len(self.inventory))]

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
        
    def renderHotbar(self, surface: pygame.Surface, hotbarNum, mousePos: tuple[int]) -> None:
        # Actual inventory
        for slotNum in range(10): # The number of slots in a row
            if not self.innerRects[slotNum].collidepoint(mousePos):
                pygame.draw.rect(surface, NAME_SPACE["color"]["mainButton"], self.innerRects[slotNum])
            else:
                pygame.draw.rect(surface, NAME_SPACE["color"]["mainButtonHover"], self.innerRects[slotNum])

            pygame.draw.rect(surface, NAME_SPACE["color"]["mainButtonBorder"], self.baseRects[slotNum],
                width = int(STGS["border"] // 2), border_radius = int(STGS["border"]))
            if slotNum == hotbarNum:
                pygame.draw.rect(surface, NAME_SPACE["color"]["hotbarItemSelected"], self.baseRects[slotNum],
                    width = int(STGS["border"] // 2), border_radius = int(STGS["border"]))
            
            item = self.inventory[slotNum]
            if item is not None:
                item.renderIcon(surface,
                    (int(self.innerRects[slotNum].x + self.innerRects[slotNum].w * 0.5 - ITEM_ICON[item.id].get_width() * 0.5),
                    int(self.innerRects[slotNum].y + self.innerRects[slotNum].h * 0.5 - ITEM_ICON[item.id].get_height() * 0.5)))

    def renderFullInventory(self, surface: pygame.Surface, hotbarNum, mousePos: tuple[int]) -> None:
        # Actual inventory
        for slotNum, item in self.inventory.items():
            if not self.innerRects[slotNum].collidepoint(mousePos):
                pygame.draw.rect(surface, NAME_SPACE["color"]["mainButton"], self.innerRects[slotNum])
            else:
                pygame.draw.rect(surface, NAME_SPACE["color"]["mainButtonHover"], self.innerRects[slotNum])

            pygame.draw.rect(surface, NAME_SPACE["color"]["mainButtonBorder"], self.baseRects[slotNum],
                width = int(STGS["border"] // 2), border_radius = int(STGS["border"]))
            
            if item is not None:
                item.renderIcon(surface,
                    (int(self.innerRects[slotNum].x + self.innerRects[slotNum].w * 0.5 - ITEM_ICON[item.id].get_width() * 0.5),
                    int(self.innerRects[slotNum].y + self.innerRects[slotNum].h * 0.5 - ITEM_ICON[item.id].get_height() * 0.5)))
                
    def doesHover(self, mousePos: tuple[int]) -> bool:
        for slotNum, item in self.inventory.items():
            if self.innerRects[slotNum].collidepoint(mousePos):
                return True
        return False
    
    def getSlotNum(self, mousePos: tuple[int]) -> int | None:
        for slotNum, item in self.inventory.items():
            if self.innerRects[slotNum].collidepoint(mousePos):
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

        logMSG("Not all cases have been covered")

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
                (int(mousePos[0] - ITEM_ICON[item.id].get_width() * 0.5),
                int(mousePos[1] - ITEM_ICON[item.id].get_height() * 0.5)))
