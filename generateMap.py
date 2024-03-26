import json
import random

def generate_map(numTiles) -> dict[str, dict[str, str | int]]:
    tilemap: dict[str, dict[str, str | int]] = {}
    
    base_tiles = {'stone', 'dirt'}
    while len(tilemap) < numTiles:
        block: str = random.choice(list(base_tiles))
        x: int = random.randint(-50, 40)
        y: int = random.randint(-20, 130)
        variant: int = random.randint(0, 1)
        if f"{x};{y}" not in tilemap:
            tilemap[f"{x};{y}"] = {"block": block, "variant": variant}
    
    numClusters = 20
    for _ in range(numClusters):
        cluster_x = random.randint(-40, 30)
        cluster_y = random.randint(-10, 120)
        for _ in range(10):  # Adjust the cluster size as needed
            x = cluster_x + random.randint(-2, 2)
            y = cluster_y + random.randint(-2, 2)
            if f"{x};{y}" not in tilemap:
                tilemap[f"{x};{y}"] = {"block": "iron", "variant": 0}
    
    return tilemap

def save_map(tilemap: dict[str, dict[str, str | int]], alias: str) -> None:
    with open(f"src/data/map/{alias}.json", mode = "w") as file:
        json.dump(tilemap, file, indent = 4)

if __name__ == "__main__":
    numTiles: int = 500
    filename: str = "map2"

    save_map(generate_map(numTiles), filename)
    print(f"Map saved to {filename}")
