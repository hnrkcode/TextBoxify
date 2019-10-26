import string

import pygame

from .text import Text
from .util import IdleBoxSymbol, CharacterPortrait, load_image


class TextBoxFrame(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text,
        text_width,
        lines,
        pos,
        padding=(50, 50),
        font_color=(255, 255, 255),
        font_type=None,
        font_size=35,
        bg_color=(0, 0, 0),
        corner=None,
        side=None,
        frame_colorkey=None,
        transparent=True,
    ):
        super().__init__()

        self.lines = lines

        # Initialize text content.
        self.textbox = TextBox(
            text=text,
            text_width=text_width,
            lines=lines,
            pos=pos,
            font_type=font_type,
            font_size=font_size,
            font_color=font_color,
            bg_color=bg_color,
            transparent=transparent,
        )

        self.text_width = text_width

        # Words to print.
        self.words = self.textbox.words

        # Idle box animation.
        self.idle_symbol = None

        # Portrait image.
        self.portrait = None

        # Background color.
        self.bg_color = bg_color

        # Space between text and text box border.
        self.padding = padding

        # Frame sprites.
        self.corner_sprite = load_image(corner, frame_colorkey)
        self.side_sprite = load_image(side, frame_colorkey)

        self.blocks = {
            "TOP_LEFT": self.corner_sprite,
            "TOP_RIGHT": pygame.transform.rotate(self.corner_sprite, -90),
            "BOTTOM_LEFT": pygame.transform.rotate(self.corner_sprite, 90),
            "BOTTOM_RIGHT": pygame.transform.rotate(self.corner_sprite, 180),
            "LEFT": self.side_sprite,
            "TOP": pygame.transform.rotate(self.side_sprite, -90),
            "BOTTOM": pygame.transform.rotate(self.side_sprite, 90),
            "RIGHT": pygame.transform.rotate(self.side_sprite, 180),
        }

        # Text box size including the frame.
        self.size = (
            text_width + padding[0],
            self.textbox.linesize * lines + padding[1],
        )

        # Size of thext box with frame.
        self.size = self.adjust_size(self.size)

        self.image = pygame.Surface(self.size).convert()
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def set_idle_animation(self, sprite, size, colorkey=None):
        """Initilize animated idle symbol."""

        self.idle_symbol = IdleBoxSymbol(sprite, size, colorkey)

    def set_portrait(self, sprite, size, colorkey=None):
        """Initilize picture of the character in the box."""

        # Portrait should have the same height as the text lines.
        text_height = self.textbox.linesize * self.lines
        scale = (text_height, text_height)

        self.portrait = CharacterPortrait(sprite, size, colorkey, scale)

        size = (
            self.portrait.image.get_width() + self.text_width + self.padding[0],
            self.size[1],
        )

        self.size = self.adjust_size(size)
        self.image = pygame.Surface(self.size).convert()
        self.image.fill(self.bg_color)
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def adjust_size(self, size):
        """Adjust the box size after the box border sprites."""

        w = size[0] - size[0] % self.side_sprite.get_width()
        h = size[1] - size[1] % self.side_sprite.get_height()

        return (w, h)

    def style_box(self, src, dest, blocks, type):
        """Draw the borders of the dialog box."""

        src_w, src_h = src.get_size()
        dest_w, dest_h = dest.get_size()

        if type == "CORNER":
            dest.blit(blocks["TOP_LEFT"], (0, 0))
            dest.blit(blocks["TOP_RIGHT"], (dest_w - src_w, 0))
            dest.blit(blocks["BOTTOM_LEFT"], (0, dest_h - src_h))
            dest.blit(blocks["BOTTOM_RIGHT"], (dest_w - src_w, dest_h - src_h))

        elif type == "SIDE":
            # Left & right side
            for block in range(1, dest_h // src_h - 1):
                dest.blit(blocks["LEFT"], (0, 0 + src_h * block))
                dest.blit(blocks["RIGHT"], (dest_w - src_w, 0 + src_h * block))

            # Top & bottom side
            for block in range(1, dest_w // src_h - 1):
                dest.blit(blocks["TOP"], (0 + src_w * block, 0))
                dest.blit(blocks["BOTTOM"], (0 + src_w * block, dest_h - src_h))

    def reset(self):
        """Reset the filled box and continue with the remaining words."""

        if self.textbox.full_box:

            self.textbox.reset()

            self.style_box(self.corner_sprite, self.image, self.blocks, "CORNER")
            self.style_box(self.side_sprite, self.image, self.blocks, "SIDE")

    def update(self):
        """Update the text box."""

        # Update the text.
        self.textbox.update()
        self.words = self.textbox.words
        self.image.fill(self.bg_color)

        # Set box padding.
        padding = (self.padding[0] // 2, self.padding[1] // 2)

        if self.portrait:
            self.portrait.animate(pygame.time.get_ticks())
            pos = (padding[0] - 10, padding[1])
            self.image.blit(self.portrait.image, pos)

            # Draw the new text.
            self.image.blit(
                self.textbox.image,
                (padding[0] + self.portrait.image.get_width(), padding[1]),
            )
        else:
            self.image.blit(self.textbox.image, padding)

        # Draw animated idling symbol.
        if self.textbox.idle and self.idle_symbol:
            self.idle_symbol.animate(pygame.time.get_ticks())
            pos = (
                self.size[0] - padding[0],
                padding[1] + self.textbox.h - self.textbox.linesize,
            )
            self.image.blit(self.idle_symbol.image, pos)

        # Draw box border.
        self.style_box(self.corner_sprite, self.image, self.blocks, "CORNER")
        self.style_box(self.side_sprite, self.image, self.blocks, "SIDE")

        self.dirty = 1


class TextBox(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text,
        text_width,
        lines,
        pos,
        font_type=None,
        font_size=35,
        font_color=(255, 255, 255),
        bg_color=(0, 0, 0),
        transparent=True,
    ):
        super().__init__()

        self.font_type = font_type
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color
        self.full_box = False
        self.words = self.convert_text(text)
        self.linesize = Text(self.words[0], font=font_type, size=font_size).linesize

        # Offset have to be set to zero to be able to print one liners.
        if lines == 1:
            self.offset = 0
        else:
            self.offset = self.linesize

        self.indent = 0
        # Text cursor position.
        self.x, self.y = self.indent, 0
        # Box dimensions.
        self.w, self.h = (text_width, self.linesize * lines)

        self.image = pygame.Surface((self.w, self.h)).convert()

        if transparent:
            self.image.set_colorkey(bg_color)

        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Find the widest character.
        chars = {char: Text(char, font=font_type, size=font_size).width for char in string.printable}
        self.widest_char = chars[max(chars, key=chars.get)]

        # Calculate how many character that can fit on one line.
        # Use the widest character to be sure that everything will fits.
        self.max = self.w // self.widest_char

        self.idle = False

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
            self.x, self.y = self.indent, 0
            self.full_box = False
            self.idle = False
            self.dirty = 1

    def update(self):
        """Update the text box."""

        # Print as long as there are words and text box isn't full.
        if self.words and not self.full_box:

            word_string = self.split_long_word(self.words.pop(0))
            word_surface = Text(
                word_string, font=self.font_type, size=self.font_size, color=self.font_color, background=self.bg_color
            )

            # Print new words until all lines in the box are filled.
            if self.y < self.h - self.offset:

                # Print new words until the current line is filled.
                if self.x + word_surface.width < self.w:
                    self.image.blit(word_surface.image, (self.x, self.y))
                    self.x += word_surface.width
                    self.dirty = 1

                # Go to next the line.
                else:
                    self.x = self.indent
                    self.y += word_surface.height
                    self.words.insert(0, word_string)
                    self.dirty = 1

            # All lines in the box are filled with words.
            else:
                self.full_box = True
                self.words.insert(0, word_string)

        # Stuff to do while box is idle.
        else:
            self.idle = True
