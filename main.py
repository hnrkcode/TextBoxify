import pygame
from pygame import locals

from textboxify.text import Text
from textboxify.textbox import TextBox, TextBoxFrame
from textboxify.util import sprite_slice


def main():
    pygame.init()
    fps = 60
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280, 720))
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((85, 87, 83))

    with open("assets/texts/sample.txt", "r") as f:
        message = f.read()

    boxes = [
        TextBoxFrame(
            message,
            text_width=450,
            lines=4,
            pos=(10, 10),
            padding=(200, 150),
            bg_color=(23, 23, 23),
            corner="assets/frames/corner_white.png",
            side="assets/frames/side_white.png",
        ),
        TextBoxFrame(
            message,
            text_width=550,
            lines=3,
            pos=(10, 300),
            padding=(100, 50),
            bg_color=(117, 80, 123),
            corner="assets/frames/pink_corner.png",
            side="assets/frames/pink_side.png",
            frame_colorkey=(255, 255, 255),
        ),
        TextBox(
            message,
            text_width=800,
            lines=1,
            pos=(10, 450),
            bg_color=(23, 23, 23),
            transparent=True,
        ),
        TextBox(
            message,
            text_width=500,
            lines=6,
            pos=(10, 500),
            bg_color=(23, 23, 23),
            transparent=False,
        ),
    ]

    boxes[0].set_idle_animation("assets/idle/arrow.png", (25, 25), (0, 0, 0))

    box_group = pygame.sprite.LayeredDirty(boxes)
    box_group.clear(screen, background)

    while True:
        # Limit frame rate.
        clock.tick(fps)

        # Handle user inputs.
        for event in pygame.event.get():
            if event.type == locals.KEYDOWN:
                # Exit game when ESC is pressed.
                if event.key == locals.K_ESCAPE:
                    raise SystemExit()
                if event.key == locals.K_RETURN:
                    for box in box_group.sprites():
                        if box.words:
                            box.reset()
                        else:
                            box.kill()

        box_group.update()
        rects = box_group.draw(screen)
        pygame.display.update(rects)


if __name__ == "__main__":
    main()
