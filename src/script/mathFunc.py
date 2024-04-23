import math

def getHyp(side1: float, side2: float) -> float:
    """Returns the hypotenuse of a right triangle given two sides."""
    return math.sqrt(side1**2 + side2**2)

def playerMagnetFunc(distance: tuple[float]) -> tuple[float]:
    """
    Accepts float from the range [-1; 1]

    Returns:
        tuple[float]: (x, y) E [-1; 1]
    """
    x, y = distance
    return (
        (math.cos(math.pi * x)**2 - 1) * ((-1) if x > 0 else (0 if x == 0 else 1)),
        (math.cos(math.pi * y)**2 - 1) * ((-1) if y > 0 else (0 if y == 0 else 1))
    )