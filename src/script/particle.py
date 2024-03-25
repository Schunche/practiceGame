import pygame
class Particle:
    def __init__(self, assets, species: str, pos: list[float], velocity: list[float] = [0, 0], frame: int = 0) -> None:
        self.species = species
        self.pos = list(pos)
        self.velocity = velocity
        self.frame = frame

        self.animation = assets[species].copy()
        self.animation.frame = frame

    def update(self) -> bool:
        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill
    
    def render(self, surface: pygame.Surface, offset: list[int] = (0, 0)):
        image = self.animation.img()
        surface.blit(image, (self.pos[0] - offset[0] - image.get_width() // 2, self.pos[1] - offset[1] - image.get_height() // 2))
