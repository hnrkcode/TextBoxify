import pygame
from pygame import locals
from textboxify.text import Text
from textboxify.textbox import TextBox, TextBoxFrame


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
        TextBoxFrame(message, text_width=500, lines=6, pos=(100, 100), padding=(200, 150), bg_color=(23,23,23)),
        TextBox(message, text_width=500, lines=6, pos=(700, 500), bg_color=(23,23,23), transparent=False),
    ]

    all = pygame.sprite.LayeredDirty(boxes)
    all.clear(screen, background)

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
                    for box in all.sprites():
                        if box.words:
                            box.reset()
                        else:
                            box.kill()

        all.update()
        rects = all.draw(screen)
        pygame.display.update(rects)


if __name__ == "__main__":
    main()
