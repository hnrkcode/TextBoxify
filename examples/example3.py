"""Simple example to illustrate how TextBoxify can be implemented."""

import random

import numpy
import pygame
from pygame import locals

from textboxify import Text, TextBoxFrame

# Imports from the textboxify package.
from textboxify.borders import BARBER_POLE
from textboxify.util import load_image

WIDTH, HEIGHT = 640, 360


def random_color():
    """Return random RGB value."""

    r = random.choice(range(255))
    g = random.choice(range(255))
    b = random.choice(range(255))

    return (r, g, b)


def draw_background(surface):
    """Draw checkered pattern with random colors as background."""

    x, y, size = 0, 0, 100
    block = numpy.zeros((WIDTH, HEIGHT, 3))

    for h in range(HEIGHT // size + 1):
        for w in range(WIDTH // size + 1):
            block[x : x + size, y : y + size :] = random_color()
            x += size
        x = 0
        y += size

    pygame.surfarray.blit_array(surface, block)


def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface(screen.get_size())

    draw_background(background)

    header_text = "TEXTBOXIFY"
    dialog_text = "Example of a textbox with animated borders!"

    # Create simple text with textboxify.
    header = Text(
        text=header_text,
        font="Source Code Pro",
        size=65,
        color=(255, 255, 255),
        background=random_color(),
    )

    # Customize and initialize a new dialog box.
    dialog_box = TextBoxFrame(
        text=dialog_text,
        text_width=320,
        lines=4,
        pos=(50, 120),
        padding=(150, 100),
        font_size=16,
        font_name="Source Code Pro",
        bg_color=(50, 50, 50),
        # Uses 'BARBER_POLE' border which is an animated border.
        border=BARBER_POLE,
        # Alpha argument take a value from 0 (transparent) to 255 (opaque),
        # which sets the degree of transparency the boxes background should have.
        alpha=200,
    )

    # Optionally: add an animated or static image to indicate that the box is
    # waiting for user input before it continue to do anything else.
    # This uses the default indicator, but custom sprites can be used too.
    dialog_box.set_indicator()

    # Optionally: add a animated portrait or a static image to represent who is
    # talking. The portrait is adjusted to be the same height as the total line
    # height in the box.
    # This uses the default portrait, but custom sprites can be used too.
    dialog_box.set_portrait()

    # Create sprite group for the dialog boxes.
    dialog_group = pygame.sprite.LayeredDirty()
    dialog_group.clear(screen, background)

    while True:

        pygame.time.Clock().tick(60)

        # Draw textboxify text object to the screen.
        background.blit(header.image, (130, 30))

        for event in pygame.event.get():
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    raise SystemExit()

                # Event that activates the dialog box.
                if event.key == locals.K_s:
                    if not dialog_group:
                        dialog_group.add(dialog_box)

                # Event that let the user tell the box to print next lines of
                # text or close when finished printing the whole message.
                if event.key == locals.K_RETURN:

                    # Cleans the text box to be able to go on printing text
                    # that didn't fit, as long as there are text to print out.
                    if dialog_box.words:
                        dialog_box.reset()

                    # Whole message has been printed and the box can now reset
                    # to default values, set a new text to print out and close
                    # down itself.
                    else:
                        dialog_box.reset(hard=True)
                        dialog_box.set_text("Happy coding!")
                        dialog_box.kill()

        # Update the changes so the user sees the text.
        dialog_group.update()
        rects = dialog_group.draw(screen)
        pygame.display.update(rects)


if __name__ == "__main__":
    main()
