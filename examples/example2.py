"""Simple example to illustrate how TextBoxify can be implemented."""

import pygame
from pygame import locals

# Import the textboxify package.
import textboxify


def main():
    pygame.init()
    w, h = (640, 360)
    screen = pygame.display.set_mode((w, h))
    background = pygame.Surface(screen.get_size())
    background.fill((92, 53, 102), rect=(0, 0, w // 2, h))

    info_1 = "TEXTBOXIFY EXAMPLE 2"
    info_2 = "Left click anywhere to activate the dialog box."

    # Create simple text with textboxify.
    info_text_1 = textboxify.Text(text=info_1, color=(0, 0, 0), background=(92, 53, 102))
    info_text_2 = textboxify.Text(text=info_2, color=(0, 0, 0), size=25, background=(92, 53, 102))

    # Customize and initialize a new dialog box.
    dialog_box = textboxify.TextBox(
        text_width=100,
        pos=(80, 180),
        font_size=20,
    )

    # Create sprite group for the dialog boxes.
    dialog_group = pygame.sprite.LayeredDirty()
    dialog_group.clear(screen, background)

    while True:

        pygame.time.Clock().tick(60)

        # Draw textboxify text object to the screen.
        background.blit(info_text_1.image, (180,50))
        background.blit(info_text_2.image, (130,120))

        for event in pygame.event.get():

            # Open the text box at the location of the mouse click.
            if event.type == locals.MOUSEBUTTONDOWN:

                # Left mouse button is clicked.
                if event.button == 1:
                    if not dialog_group:
                        if event.pos[0] < w // 2:
                            dialog_box.set_text("left side")
                        else:
                            dialog_box.set_text("right side")

                        # Draw the text box at this position.
                        dialog_box.rect.topleft = event.pos
                        dialog_group.add(dialog_box)

                    # Event that let the user tell the box to print next lines of
                    # text or close when finished printing the whole message.
                    else:
                        # Cleans the text box to be able to go on printing text
                        # that didn't fit, as long as there are text to print out.
                        if dialog_box.words:
                            dialog_box.reset()

                        # Whole message has been printed and the box can now reset
                        # to default values, set a new text to print out and close
                        # down itself.
                        else:
                            dialog_box.hard_reset()
                            dialog_box.kill()

            if event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    raise SystemExit()

        # Update the changes so the user sees the text.
        dialog_group.update()
        rects = dialog_group.draw(screen)
        pygame.display.update(rects)


if __name__ == "__main__":
    main()
