import pygame


def load_image(file, colorkey=None):
    """Load image file."""

    try:
        image = pygame.image.load(file)
    except pygame.error as e:
        raise SystemExit(f"load_image: {e}")

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

    def __init__(self, fps, delay):
        super().__init__()

        self._images = None
        self._fps = fps
        self._delay = delay / self._fps
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


class CustomSprite(AnimateSprite):
    def __init__(self, file, size, colorkey=None, scale=None, fps=15, delay=1500):
        super().__init__(fps, delay)

        self._images = sprite_slice(file, size, colorkey, scale)
        self.image = self._images[0]
        self.rect = self.image.get_rect()

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def update(self):
        self.dirty = 1


class Text(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text,
        pos=(0, 0),
        color=(255, 255, 255),
        font=None,
        size=35,
        antialias=1,
        background=None,
    ):
        super().__init__()

        try:
            self._font = pygame.font.Font(font, size)
        except FileNotFoundError as e:
            print(e, "uses default pygame font instead.")
            self._font = pygame.font.Font(None, size)

        self.image = self._font.render(text, antialias, color, background)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    @property
    def position(self):
        """Return text position."""
        return self.rect.topleft

    @position.setter
    def position(self, pos):
        """Update text position."""
        self.rect.topleft = pos

    @property
    def linesize(self):
        """Return linesize for text with this font."""
        return self._font.get_linesize()

    @property
    def size(self):
        """Return text surface size."""
        return self.rect.size

    @property
    def width(self):
        """Return text surface width."""
        return self.rect.width

    @property
    def height(self):
        """Return text surface height."""
        return self.rect.height

    def update(self):
        self.dirty = 1
