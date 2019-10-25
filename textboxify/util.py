import pygame


def load_image(file, colorkey):
    """Load image file."""

    try:
        image = pygame.image.load(file)
    except pygame.error as e:
        raise SystemExit(e)

    if colorkey:
        image.set_colorkey(colorkey)
        image = image.convert()

    return image


def sprite_slice(file, size, colorkey=None, scale=None):
    """Slice image into smaller images."""

    frames = []
    frame_width, frame_height = size

    # Full image.
    master_image = load_image(file, colorkey)
    master_width, master_height = master_image.get_size()

    # Slice image from left to right.
    for i in range(int(master_width / frame_width)):
        left = i * frame_width

        if not scale:
            frame = master_image.subsurface((left, 0, frame_width, frame_height))
        else:
            frame = master_image.subsurface((left, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, scale)
        frames.append(frame)

    return frames


class AnimateSprite(pygame.sprite.DirtySprite):
    """Implement animated sprites."""

    def __init__(self):
        super().__init__()

        self._images = None
        self._fps = 15
        self._delay = 1500 / self._fps
        self._last_update = 0
        self._frame = 0

    def animate(self, t):
        """Switch the current image with another to create animations."""

        if t - self._last_update > self._delay:
            self._frame += 1

            if self._frame >= len(self._images):
                self._frame = 0

            self.image = self._images[self._frame]
            self._last_update = t


class IdleBoxSymbol(AnimateSprite):
    """Implement symbol that indicate box is idle."""

    def __init__(self, file, size, colorkey=None):
        super().__init__()
        self._images = sprite_slice(file, size, colorkey)
        self.image = self._images[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.dirty = 1


class CharacterPortrait(AnimateSprite):
    """Implement symbol that indicate box is idle."""

    def __init__(self, file, size, colorkey=None, scale=None):
        super().__init__()
        self._images = sprite_slice(file, size, colorkey, scale=scale)
        self.image = self._images[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.dirty = 1
