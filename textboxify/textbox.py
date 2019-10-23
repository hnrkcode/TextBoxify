import pygame
import string

from .text import Text


class TextBoxFrame(pygame.sprite.DirtySprite):
    def __init__(self, text, text_width, lines, pos, padding=(100, 50), bg_color=(0, 0, 0)):
        super().__init__()

        # Background color.
        self.bg_color = bg_color

        # Space between text and text box border.
        self.padding = padding

        # Text content.
        self.textbox = TextBox(text, text_width, lines, pos, bg_color)
        self.words = self.textbox.words
        self.reset = self.textbox.reset

        # Text box size including the frame.
        self.size = (text_width + padding[0], self.textbox.linesize * lines + padding[1])

        self.image = pygame.Surface(self.size).convert()
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        """Update the text box."""

        # Update the text.
        self.textbox.update()
        self.words = self.textbox.words
        self.image.fill(self.bg_color)

        # Set box padding.
        padding = (self.padding[0] // 2, self.padding[1] // 2)

        # Draw the new text.
        self.image.blit(self.textbox.image, padding)
        self.dirty = 1


class TextBox(pygame.sprite.DirtySprite):
    def __init__(self, text, text_width, lines, pos, bg_color=(0, 0, 0), transparent=True):
        super().__init__()

        self.bg_color = bg_color
        self.full_box = False
        self.words = self.convert_text(text)
        self.linesize = Text(self.words[0]).linesize

        # Text cursor position.
        self.x, self.y = 0, 0
        # Box dimensions.
        self.w, self.h = (text_width, self.linesize * lines)

        self.image = pygame.Surface((self.w, self.h)).convert()

        if transparent:
            self.image.set_colorkey(bg_color)

        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Find the widest character.
        chars = {char: Text(char).width for char in string.printable}
        self.widest_char = chars[max(chars, key=chars.get)]

        # Calculate how many character that can fit on one line.
        # Use the widest character to be sure that everything will fits.
        self.max = self.w // self.widest_char

    def convert_text(self, msg):
        """Convert string into list with words and characters to print."""

        # Split text into words and remove any '\n' and spaces.
        words = list(filter(("").__ne__, msg.replace("\n", " ").split(" ")))
        # Insert space between every second word.
        words = list(v + " " * (i % 1 == 0) for i, v in enumerate(words))

        return words

    def split_long_word(self, word):
        """Split up long words into characters to be able to fit inside box."""

        if len(word) > self.max:
            # Insert characters of too long words into the list.
            self.words = list(word) + self.words
            return self.words.pop(0)

        return word

    def reset(self):
        """Reset the filled box and continue with the remaining words."""

        if self.full_box:
            self.image.fill(self.bg_color)
            self.x, self.y = 0, 0
            self.full_box = False
            self.dirty = 1

    def update(self):
        """Update the text box."""

        # Print as long as there are words and text box isn't full.
        if self.words and not self.full_box:

            word_string = self.split_long_word(self.words.pop(0))
            word_surface = Text(word_string)

            # Print new words until all lines in the box are filled.
            if self.y < self.h - self.linesize:

                # Print new words until the current line is filled.
                if self.x + word_surface.width < self.w:
                    self.image.blit(word_surface.image, (self.x, self.y))
                    self.x += word_surface.width
                    self.dirty = 1

                # Go to next the line.
                else:
                    self.x = 0
                    self.y += word_surface.height
                    self.words.insert(0, word_string)
                    self.dirty = 1

            # All lines in the box are filled with words.
            else:
                self.full_box = True
                self.words.insert(0, word_string)

        # Stuff to do while box is idle.
        else:
            pass
