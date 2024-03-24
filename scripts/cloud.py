import random

class Cloud:
    def __init__(self, pos, img, speed, depth) -> None:
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self) -> None:
        self.pos[0] += self.speed

    def render(self, surface, offset = (0, 0)) -> None:
        renderPos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surface.blit(self.img, (renderPos[0] % (surface.get_width() + self.img.get_width()) - self.img.get_width(), renderPos[1] % (surface.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    def __init__(self, cloudImages, count: int = 2^4) -> None:
        self.clouds = []

        for _ in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloudImages), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
            
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset = (0, 0)) -> None:
        for cloud in self.clouds:
            cloud.render(surface, offset = offset)
