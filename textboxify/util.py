import pygame


def fix_corners(surface, corner_size, bg_color, colorkey):
    """Remove pixels outside rounded corners."""

    pixels = []
    w, h = corner_size

    if colorkey:
        colorkey = (*colorkey, 0)

    # Upper left corner.
    for y in range(h):
        for x in range(w):
            if surface.get_at((x, y)) == bg_color:
                pixels.append((x, y))
                continue
            break

    # Bottom left corner.
    for y in range(surface.get_height() - h, surface.get_height()):
        for x in range(w):
            if surface.get_at((x, y)) == bg_color:
                pixels.append((x, y))
                continue
            break

    # Upper right corner.
    for y in range(h):
        for x in reversed(range(surface.get_width() - w, surface.get_width())):
            if surface.get_at((x, y)) == bg_color:
                pixels.append((x, y))
                continue
            break

    # Bottom right corner.
    for y in range(surface.get_height() - h, surface.get_height()):
        for x in reversed(range(surface.get_width() - w, surface.get_width())):
            if surface.get_at((x, y)) == bg_color:
                pixels.append((x, y))
                continue
            break

    for pixel in pixels:
        surface.set_at(pixel, colorkey)

    # Removes pixels outside corners when background is opaque.
    surface.set_colorkey(colorkey)

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
            scale = int(scale[0]), int(scale[1])
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

    @property
    def size(self):
        return self.image.get_size()

    def update(self):
        self.dirty = 1
