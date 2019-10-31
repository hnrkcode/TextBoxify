import string

import pygame

from . import settings
from .text import Text
from .util import CustomSprite, load_image, fix_corners


class TextBoxFrame(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text_width,
        pos,
        lines=1,
        text=None,
        padding=(50, 50),
        font_color=(255, 255, 255),
        font_name=None,
        font_size=35,
        bg_color=(0, 0, 0),
        corner=None,
        side=None,
        border_colorkey=None,
        transparent=False,
    ):
        super().__init__()

        # Initialize text content.
        self.__textbox = TextBox(
            text=text,
            text_width=text_width,
            lines=lines,
            pos=pos,
            font_name=font_name,
            font_size=font_size,
            font_color=font_color,
            bg_color=bg_color,
            transparent=transparent,
        )

        self.__lines = lines
        self.__text_width = text_width
        self.__bg_color = bg_color
        self.__padding = padding
        self.__indicator = None
        self.__portrait = None
        self.__border_colorkey = border_colorkey

        # Sprites of topleft and left corner that will be rotated and reused.
        if corner and side:
            self.__corner = load_image(corner, border_colorkey)
            self.__side = load_image(side, border_colorkey)
        # Use default border sprites.
        else:
            self.__corner = load_image(settings.DEFAULT_CORNER)
            self.__side = load_image(settings.DEFAULT_SIDE)

        self.__blocks = {
            "TOP_LEFT": self.__corner,
            "TOP_RIGHT": pygame.transform.rotate(self.__corner, -90),
            "BOTTOM_LEFT": pygame.transform.rotate(self.__corner, 90),
            "BOTTOM_RIGHT": pygame.transform.rotate(self.__corner, 180),
            "LEFT": self.__side,
            "TOP": pygame.transform.rotate(self.__side, -90),
            "BOTTOM": pygame.transform.rotate(self.__side, 90),
            "RIGHT": pygame.transform.rotate(self.__side, 180),
        }

        # Text box size including the frame.
        w = text_width + padding[0]
        h = self.__textbox.linesize * lines + padding[1]

        self.size = self._adjust((w, h))
        self.image = pygame.Surface(self.size).convert()
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    @property
    def words(self):
        return self.__textbox.words

    @words.setter
    def words(self, words):
        self.__words = words

    def set_indicator(self, sprite=None, size=None, colorkey=None, scale=None):
        """Initilize animated idle symbol."""

        if sprite:
            self.__indicator = CustomSprite(sprite, size, colorkey, scale)
        else:
            self.__indicator = CustomSprite(settings.DEFAULT_INDICATOR["file"], settings.DEFAULT_INDICATOR["size"], (0, 0, 0))

    def set_portrait(self, sprite=None, size=None, colorkey=None):
        """Initilize picture of the character in the box."""

        # Set portrait to have the same height as the text lines.
        scale = [self.__textbox.linesize * self.__lines] * 2

        # Set custom sprite for portrait.
        if sprite:

            # Shut down if no size.
            if not size:
                raise SystemExit("Error: Need to give a size for the portrait sprite.")

            self.__portrait = CustomSprite(
                file=sprite,
                size=size,
                colorkey=colorkey,
                scale=scale,
            )

        # Use default portrait sprite.
        else:
            self.__portrait = CustomSprite(
                file=settings.DEFAULT_PORTRAIT["file"],
                size=settings.DEFAULT_PORTRAIT["size"],
                colorkey=(241, 0, 217),
                scale=scale,
            )

        # Adjust box text to the portrait.
        w = self.__portrait.width + self.__text_width + self.__padding[0]
        h = self.size[1]
        size = (w, h)

        # Update textbox data with portrait implemented.
        pos = self.rect.topleft
        self.size = self._adjust(size)
        self.image = pygame.Surface(self.size).convert()
        self.image.fill(self.__bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def set_text(self, text):
        """Set new text message to print out."""

        self.__textbox.set_text(text)

    def reset(self):
        """Reset the filled box and continue with the remaining words."""

        if self.__textbox.full:
            self.__textbox.reset()
            self._draw_border()

    def hard_reset(self):
        """Reset box to default values when whole message has been printed."""

        self.__textbox.hard_reset()

    def update(self):
        """Update the text box."""

        # Update the text.
        self.__textbox.update()
        self.words = self.__textbox.words
        self.image.fill(self.__bg_color)

        # Set box padding.
        padding = (self.__padding[0] // 2, self.__padding[1] // 2)

        if self.__portrait:
            self.__portrait.animate(pygame.time.get_ticks())
            pos = (padding[0] - 10, padding[1])
            self.image.blit(self.__portrait.image, pos)

            # Draw the new text.
            self.image.blit(
                self.__textbox.image, (padding[0] + self.__portrait.width, padding[1])
            )
        else:
            self.image.blit(self.__textbox.image, padding)

        # Draw animated idling symbol.
        if self.__textbox.idle and self.__indicator:
            self.__indicator.animate(pygame.time.get_ticks())
            pos = (
                self.size[0] - padding[0],
                self.__textbox.linesize * self.__lines
                + padding[1]
                - self.__indicator.height,
            )
            self.image.blit(self.__indicator.image, pos)

        # Draw box border.
        self._draw_border()

        self.dirty = 1

    def _adjust(self, size):
        """Adjust the box size after the box border sprites."""

        w = size[0] - size[0] % self.__side.get_width()
        h = size[1] - size[1] % self.__side.get_height()

        return (w, h)

    def _blit_border(self, src, dest, blocks, type):
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

    def _draw_border(self):
        """Draws the border and then fixes the corners if needed."""

        self._blit_border(self.__corner, self.image, self.__blocks, "CORNER")
        self._blit_border(self.__side, self.image, self.__blocks, "SIDE")

        # Make pixels outside rounded corners transparent.
        fix_corners(
            surface=self.image,
            corner_size=self.__corner.get_size(),
            bg_color=self.__bg_color,
            colorkey=self.__border_colorkey
        )


class TextBox(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text_width,
        pos,
        text=None,
        lines=1,
        font_name=None,
        font_size=35,
        font_color=(255, 255, 255),
        bg_color=(0, 0, 0),
        transparent=False,
    ):
        super().__init__()

        self.full = False
        self.idle = False

        if text:
            self.words = self._to_list(text)
        else:
            self.words = ""

        self.linesize = Text(
            text=" ", font=font_name, size=font_size
        ).linesize

        self.__font_name = font_name
        self.__font_size = font_size
        self.__font_color = font_color
        self.__bg_color = bg_color
        self.__transparent = transparent
        self.__pos = pos

        # Offset have to be set to zero to be able to print one liners.
        self.__offset = 0 if lines == 1 else self.linesize

        # Text cursor position.
        self.__x, self.__y = 0, 0
        self.__w, self.__h = (text_width, self.linesize * lines)

        # Calculate how many character that can fit on one line.
        # Use the widest character to be sure that everything will fits.
        chars = {
            char: Text(char, font=font_name, size=font_size).width
            for char in string.printable
        }
        widest = chars[max(chars, key=chars.get)]
        self.__max = self.__w // widest

        self.image = pygame.Surface((self.__w, self.__h)).convert()
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        if transparent:
            self.image.set_colorkey(bg_color)

    def set_text(self, text):
        """Set new text message to print out."""

        self.words = self._to_list(text)

    def hard_reset(self):
        """Reset box to default values when whole message has been printed."""

        self.__x, self.__y = 0, 0
        self.full = False
        self.idle = False
        self.image = pygame.Surface((self.__w, self.__h)).convert()
        self.image.fill(self.__bg_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.__pos

        if self.__transparent:
            self.image.set_colorkey(self.__bg_color)

    def reset(self):
        """Reset the filled box and continue with the remaining words."""

        if self.full:
            self.image.fill(self.__bg_color)
            self.__x, self.__y = 0, 0
            self.full = False
            self.idle = False

    def update(self):
        """Update the text box."""

        # Print as long as there are words and text box isn't full.
        if self.words and not self.full:

            word_string = self._split_up(self.words.pop(0))
            word_surface = Text(
                text=word_string,
                font=self.__font_name,
                size=self.__font_size,
                color=self.__font_color,
                background=self.__bg_color,
            )

            # Print new words until all lines in the box are filled.
            if self.__y < self.__h - self.__offset:

                # Print new words until the current line is filled.
                if self.__x + word_surface.width < self.__w:
                    self.image.blit(word_surface.image, (self.__x, self.__y))
                    self.__x += word_surface.width
                    self.dirty = 1

                # Go to next the line.
                else:
                    self.__x = 0
                    self.__y += word_surface.height
                    self.words.insert(0, word_string)
                    self.dirty = 1

            # All lines in the box are filled with words.
            else:
                self.full = True
                self.words.insert(0, word_string)

        # Stuff to do while box is idle.
        else:
            self.idle = True

    def _to_list(self, msg):
        """Convert string into list with words and characters to print."""

        # Split text into words and remove any '\n' and spaces.
        words = list(filter(("").__ne__, msg.replace("\n", " ").split(" ")))
        # Insert space between every second word.
        words = list(v + " " * (i % 1 == 0) for i, v in enumerate(words))

        return words

    def _split_up(self, word):
        """Split up long words into characters to be able to fit inside box."""

        if len(word) > self.__max:
            # Insert characters of too long words into the list.
            self.words = list(word) + self.words
            return self.words.pop(0)

        return word
