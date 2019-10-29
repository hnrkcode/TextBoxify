"""Simple example to illustrate how TextBoxify can be implemented."""

import pygame
from pygame import locals

# Import the textboxify package.
import textboxify


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 360))
    background = pygame.Surface(screen.get_size())
    background.fill((92, 53, 102))

    info_1 = "TEXTBOXIFY EXAMPLE"
    info_2 = "Press (S) to activate the dialog box."
    info_3 = "Press (Enter) to interact with the dialog box."
    dialog_text = "Hello! This is a simple example of how TextBoxify can be implemented in Pygame games."

    # Create simple text with textboxify.
    info_text_1 = textboxify.Text(text=info_1, color=(0, 0, 0), background=(92, 53, 102))
    info_text_2 = textboxify.Text(text=info_2, color=(0, 0, 0), size=25, background=(92, 53, 102))
    info_text_3 = textboxify.Text(text=info_3, color=(0, 0, 0), size=25, background=(92, 53, 102))

    # Customize and initialize a new dialog box.
    dialog_box = textboxify.TextBoxFrame(
        text=dialog_text,
        text_width=320,
        lines=2,
        pos=(80, 180),
        padding=(150, 100),
        font_color=(92, 53, 102),
        font_size=26,
        bg_color=(173, 127, 168),
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
        background.blit(info_text_1.image, (180,50))
        background.blit(info_text_2.image, (180,120))
        background.blit(info_text_3.image, (140,150))

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
