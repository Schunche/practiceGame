class Animation:
    def __init__(self, images, imageDuration: int = 5, loop: bool = True) -> None:
        self.images = images
        self.loop: bool = loop
        self.imageDuration: int = imageDuration

        self.done: bool = False
        self.frame: int = 0

    def copy(self):
        return Animation(self.images, self.imageDuration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.imageDuration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.imageDuration * len(self.images) - 1)
            if self.frame >= self.imageDuration * len(self.images) - 1:
                self.done = True
    def img(self):
        return self.images[int(self.frame / self.imageDuration)]
