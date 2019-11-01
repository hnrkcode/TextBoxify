"""Simple example to illustrate how TextBoxify can be implemented."""

import pygame
from pygame import locals

# Imports from the textboxify package.
from textboxify.borders import DARK, BLINK, LIGHT
from textboxify import Text, TextBoxFrame
#from textboxify.util import load_image

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    background = pygame.Surface(screen.get_size())
    #bg_img = load_image("../../bg.png")
    #background.blit(bg_img, (0, 0))


    info_1 = "TEXTBOXIFY"
    dialog_text = "Hello! This is a simple example of how TextBoxify can be implemented in Pygame games."

    # Create simple text with textboxify.
    info_text_1 = Text(text=info_1, font="Source Code Pro", size=65, color=(255, 255, 255))

    # Customize and initialize a new dialog box.
    dialog_box = TextBoxFrame(
        text=dialog_text,
        text_width=320,
        lines=4,
        pos=(50, 120),
        padding=(150, 100),
        font_size=16,
        font_name="Source Code Variable",
        bg_color=(80, 80, 80),
        border=BLINK,
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
        background.blit(info_text_1.image, (130,30))

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
                        dialog_box.hard_reset()
                        dialog_box.set_text("Happy coding!")
                        dialog_box.kill()

        # Update the changes so the user sees the text.
        dialog_group.update()
        rects = dialog_group.draw(screen)
        pygame.display.update(rects)


if __name__ == "__main__":
    main()
