import pygame
from pygame import locals

from textboxify.text import Text
from textboxify.textbox import TextBox, TextBoxFrame
from textboxify.util import sprite_slice

WIDTH, HEIGHT = 1280, 720


def main():
    pygame.init()
    fps = 60
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.Surface(screen.get_size()).convert()
    # background.fill((85, 87, 83))
    background.blit(pygame.image.load("assets/color.jpg"), (0, 0))

    with open("assets/texts/sample.txt", "r") as f:
        message = f.read()

    boxes = [
        TextBoxFrame(
            message,
            text_width=350,
            lines=4,
            pos=(10, 10),
            font_size=25,
            padding=(175, 100),
            bg_color=(23, 23, 23),
            corner="assets/border/corner_white.png",
            side="assets/border/side_white.png",
        ),
        TextBoxFrame(
            text=message,
            text_width=500,
            lines=3,
            pos=(10, 300),
            padding=(100, 70),
            font_color=(255, 255, 255),
            font_name=None,
            font_size=20,
            bg_color=(100, 50, 0),
            corner="assets/border/corner_white.png",
            side="assets/border/side_white.png",
            border_colorkey=None,
            transparent=True,
        ),
        TextBox(
            text=message, text_width=300, lines=3, pos=(10, 400), transparent=False
        ),
    ]

    boxes[0].set_indicator("assets/idle/arrow2.png", (25, 17), (0, 0, 0))
    boxes[0].set_portrait("assets/character1.png", (66, 66), (0, 0, 0))

    boxes[1].set_indicator("assets/idle/arrow2.png", (25, 17), (0, 0, 0), (31, 7))
    boxes[1].set_portrait("assets/character1.png", (66, 66), (0, 0, 0))

    box_group = pygame.sprite.LayeredDirty()
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
                # Activate textbox.
                if event.key == locals.K_s:
                    if not box_group and boxes:
                        box_group.add(boxes)

                if event.key == locals.K_RETURN:
                    for box in box_group.sprites():
                        if box.words:
                            box.reset()
                        else:
                            box.kill()

        if box_group:
            box_group.update()
            rects = box_group.draw(screen)
            pygame.display.update(rects)
        else:
            box_group.draw(screen)
            pygame.display.update()


if __name__ == "__main__":
    main()
