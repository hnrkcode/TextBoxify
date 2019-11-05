import pygame


class Text(pygame.sprite.DirtySprite):
    """Class for creating surfaces with text.

    Args:
        text (str): text on the surface (required).
        pos (tuple): x, y position.
        color (tuple): text color, RGB value.
        font (str): name of font or path to font file.
        size (int): size of text.
        antialias (bool): if true the characters will have smooth edges.
        background (tuple): color of background, RGB value.

    """

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
            try:
                self._font = pygame.font.Font(font, size)
            except FileNotFoundError:
                self._font = pygame.font.SysFont(font, size)
        except FileNotFoundError as e:
            print(e, "uses default pygame font instead.")
            self._font = pygame.font.Font(None, size)

        # Make background transparent if no background color is set.
        if not background:
            self.image = self._font.render(text, antialias, color)
            self.image = self.image.convert_alpha()
        else:
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
        """Update text."""

        self.dirty = 1
