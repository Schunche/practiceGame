import json
import math
import random

from src.script.log import *

def saveMap(tilemap: dict[str, dict[str, str | int]], alias: str) -> None:
    with open(f"src/map/{alias}/tilemap.json", mode = "w") as file:
        json.dump(tilemap, file, indent = 4)

def roundUp(num: float) -> int:
    if num == int(num):
        return num
    return int(num) + 1

def diff25(num: float) -> float:
    return abs(num * (1 + math.sin(random.random() * 2 * math.pi) / 4))

def myMathFunc1(num: float) -> float:
    return (2 ** (5 * (2 * num - 1)))

def myMathFunc2(num: float) -> float:
    return (8 * ((1 - num) ** 3))

def randomSign(num: float) -> float:
    return (((random.randint(0, 1) * 2) - 1) * num)

def generateMap(xLeft: int = 0, xRight: int = 100, yTop: int = 0, yBottom: int = 100) -> dict[str, dict[str, str | int]]:
    tilemap: dict[str, dict[str, str | int]] = {}
    # Top half is filles with dirt
    # Bottom half with stone

    tilDirtY: int = int((yTop + yBottom) / 2)
    print(f"Dirt is generated until: y = {tilDirtY}")
    for x in range(xLeft, xRight):
        # Dirt
        for y in range(yTop, tilDirtY):
            tilemap[f"{x};{y}"] = {
                "block": "dirt",
                "variant": 0}
            
        # Stone
        for y in range(tilDirtY, yBottom):
            tilemap[f"{x};{y}"] = {
                "block": "stone",
                "variant": 0}

    # Draw strokes of dirt/stone
    def drawPatchStroke(
        point: tuple[int],
        block: str,
        count: int = 0,
        radius: float = int(random.randint(9, 50) / random.randint(9, 12)),
        patchesInStroke: int = 1
        ):
        if count == 0:
            if block == "stone":
                patchesInStroke: int = int(diff25(myMathFunc1((point[1] - yTop) / (tilDirtY - yTop))))
            elif block == "dirt":
                patchesInStroke: int = int(diff25(myMathFunc2((point[1] - tilDirtY) / (yBottom - tilDirtY))))
            patchesInStroke = min(max(patchesInStroke, 0), 32) # Capped between 0 and 32
        
        if patchesInStroke != 0:
            # Go thru the circle and draw it
            for x in range(int(point[0] - radius), int(point[0] + radius) + 1):
                for y in range(int(point[1] - radius), int(point[1] + radius) + 1):
                    # If not inside grid, go to next point
                    if not (xLeft <= x < xRight and yTop <= y < yBottom):
                        continue
                    
                    # Place the block if inside the circle
                    if (x - point[0]) ** 2 + (y - point[1]) ** 2 <= roundUp(radius ** 2):
                        tilemap[f"{x};{y}"] = {
                            "block": block,
                            "variant": 0}

        if count < patchesInStroke:
            shiftDirection: float = math.pi * (1 + random.random())
            nextPoint: tuple[int] = (
                int(point[0] + randomSign(radius / 2 * math.cos(shiftDirection))),
                int(point[1] + radius / 2 * math.sin(shiftDirection))
            )
            # Change previous radious with a max of 25 %
            nextRadius: float = min(max(diff25(radius), 1), 5) # Capped between 1 and 5

            drawPatchStroke(nextPoint, block, count = count + 1, radius = nextRadius, patchesInStroke = patchesInStroke)
    
    # Stone patches in dirt
    numOfPatches: int = int(diff25((xRight - xLeft) * (tilDirtY - yTop) * 0.003))
    print(f"Stone strokes in dirt: {numOfPatches}")
    for _ in range(numOfPatches):
        point: tuple[int] = (xLeft + int(random.random() * (xRight - xLeft)), yTop + int(random.random() * (tilDirtY - yTop)))
        drawPatchStroke(point, "stone")

    # Dirt patches in stone
    numOfPatches: int = int(diff25((xRight - xLeft) * (yBottom - tilDirtY) * 0.004))
    print(f"Dirt strokes in stone: {numOfPatches}")
    for _ in range(numOfPatches):
        point: tuple[int] = (xLeft + int(random.random() * (xRight - xLeft)), tilDirtY + int(random.random() * (yBottom - tilDirtY)))
        drawPatchStroke(point, "dirt")

    ores: list[str] = [
        "copper", "tin",
        "iron", "lead",
        "silver", "tungsten",
        "gold", "platinum"
    ]

    worldOres: list[str] = [
        random.choice(ores[(2 * _):((_ + 1) * 2)]) for _ in range(int(len(ores) / 2))
    ]

    print(f"This world contains the ores: {', '.join(worldOres)}")

    return tilemap

if __name__ == "__main__":
    logMSG("Started making it")
    # X grows left to right
    # Y grows top to bottom

    # Advised size: the bigger the better
    # Don't go below 50 please
    mapLeft: int = 0
    mapRight: int = 300
    mapTop: int = 0
    mapBottom: int = 160
    logMSG(f"In range: x = ({mapLeft}; {mapRight}), y = ({mapTop}; {mapBottom})")

    filename: str = "procedural"

    generatedMap = generateMap(
        xLeft = mapLeft,
        xRight = mapRight,
        yTop = mapTop,
        yBottom = mapBottom)

    saveMap(generatedMap, filename)
    print(f"Map saved to \'{filename}\'")

else:
    logError("Did not do anything")