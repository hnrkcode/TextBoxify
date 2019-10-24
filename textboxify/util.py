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
