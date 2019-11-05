"""This module contains classes for creating text boxes.

Both TextBox and TextBoxFrame are the same when it comes to print out
text inside a box on the screen. However, TextBox has less features than
TextBoxFrame.

TextBox is useful if you only want to print out text on the
screen without much configurations.

TextBoxFrame is useful if you want to design unique dialog boxes with certain
borders, backgrounds, portraits, indication symbols and animations.
"""


import string

import pygame

from . import settings
from .text import Text
from .util import CustomSprite, fix_corners, load_image


class TextBoxFrame(pygame.sprite.DirtySprite):
    """Class for creating customizable dialog boxes.

    Args:
        text_width (int): max with of the printed text (required).
        pos (tuple): x & y coordinates to place the topleft corner of the box (required).
        lines (int): number of printed lines.
        text (str): Text to print.
        padding (tuple): space between text and border.
        font_color (tuple): text color, RGB value.
        font_name (str): name of a installed font or path to a font file.
        font_size (int): size of the text font.
        bg_color (tuple): background color, RGB value.
        border (dict): border sprite settings.
        alpha (int): value from 0 to 255, were 0-254 is transparent and 255 is opaque.

    """

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
        border=None,
        alpha=255,
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
            transparent=False if alpha == 255 else True,
        )

        self.__alpha = alpha
        self.__lines = lines
        self.__text_width = text_width
        self.__bg_color = (*bg_color, alpha)
        self.__padding = padding
        self.__indicator = None
        self.__portrait = None
        self.__border = border

        # Always check if border evaluate to true because corner and side
        # doesn't get created when there isn't any border to draw.
        if self.__border:

            # Create topleft corner sprite.
            self.__corner = CustomSprite(
                self.__border["corner"],
                self.__border["size"],
                self.__border["colorkey"],
            )

            # Create left side sprite.
            self.__side = CustomSprite(
                self.__border["side"],
                self.__border["size"],
                self.__border["colorkey"]
            )

        # Text box size including the frame.
        w = text_width + padding[0]
        h = self.__textbox.linesize * lines + padding[1]

        self.size = self._adjust((w, h), self.__side) if self.__border else (w, h)
        self.image = pygame.Surface(self.size).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    @property
    def words(self):
        """list: Return list with all words not yet printed."""

        return self.__textbox.words

    @words.setter
    def words(self, words):
        self.__words = words

    def set_indicator(self, sprite=None, size=None, colorkey=None, scale=None):
        """Initilize animated idle symbol.

        Note:
            If sprite is ommited, the default indicator
            will be used and all other arguments will be ignored.

        Args:
            sprite (str): path to sprite file.
            size (tuple): width, height of sprite frame.
            colorkey (tuple): color to remove from sprite, RGB value.
            scale (tuple): new width, height to scale sprite to.
        """

        if sprite:
            self.__indicator = CustomSprite(sprite, size, colorkey, scale)
        else:
            self.__indicator = CustomSprite(
                settings.DEFAULT_INDICATOR["file"],
                settings.DEFAULT_INDICATOR["size"],
                (0, 0, 0),
            )

    def set_portrait(self, sprite=None, size=None, colorkey=None):
        """Initilize portrait image on the left side of the text.

        Note:
            The sprite will be scaled to be the same size as the total
            height of the text line limit.

        Note:
            If sprite is ommited, a default placeholder animation
            will be used and all other arguments will be ignored.

        Args:
            sprite (str): path to sprite file.
            size (tuple): width, height of sprite frame.
            colorkey (tuple): color to remove from sprite, RGB value.
            scale (tuple): new width, height to scale sprite to.

        """

        # Set portrait to have the same height as the text lines.
        scale = [self.__textbox.linesize * self.__lines] * 2

        # Set custom sprite for portrait.
        if sprite:

            # Shut down if no size.
            if not size:
                raise SystemExit("Error: Need to give a size for the portrait sprite.")

            self.__portrait = CustomSprite(sprite, size, colorkey, scale)

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
        self.size = self._adjust(size, self.__side) if self.__border else size
        self.image = pygame.Surface(self.size).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def set_text(self, text):
        """Set new text message to print out.

        Args:
            words (str): new text to print.

        """

        self.__textbox.set_text(text)

    def reset(self, hard=False):
        """Reset dialog box.

        Args:
            hard (bool): False only cleans the box before moving to the next
                page to print the remaining words. True resets the entire class
                to default values to prepare to print new text from the beginning.
        """

        if hard:
            # Reset to default values.
            self.__textbox.reset(hard)
        else:
            # Reset the filled box and continue with the remaining words.
            if self.__textbox.full:
                self.__textbox.reset()

                if self.__border:
                    self._draw_border(
                        self.image,
                        self.__border,
                        self.__corner,
                        self.__side,
                        self.__bg_color,
                    )

    def update(self):
        """Update all changes that has been made to the text box."""

        # Update the text.
        self.__textbox.update()
        self.words = self.__textbox.words

        # Draw background with transparency.
        self.image = self._draw_background(self.image, self.__bg_color, self.__alpha)

        # Set box padding.
        padding = (self.__padding[0] // 2, self.__padding[1] // 2)

        # Draw text with or without a portrait.
        self._draw_content(self.image, self.__textbox, self.__portrait, padding)

        # Draw animated idling symbol.
        self._draw_indicator(
            self.image, self.__textbox, self.__indicator, self.__lines, padding
        )

        # Draw box border.
        if self.__border:
            self._draw_border(
                self.image,
                self.__border,
                self.__corner,
                self.__side,
                self.__bg_color,
            )

        self.dirty = 1

    def _adjust(self, size, side):
        """Adjust the box size after the box border sprites."""

        w = size[0] - size[0] % side.width
        h = size[1] - size[1] % side.height

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

    def _draw_background(self, surface, color, alpha):
        """Draw box background."""

        # Draw background with transparency.
        if 0 <= alpha < 255:
            surface = surface.convert_alpha()
            surface.fill(color)

        # Draw background with no transparency.
        else:
            surface.fill(color)

        return surface

    def _draw_content(self, surface, text, portrait, padding):
        """Draw box text and portrait."""

        if portrait:
            portrait.animate(pygame.time.get_ticks())
            pos = (padding[0] - 10, padding[1])
            surface.blit(portrait.image, pos)

            # Draw new text.
            surface.blit(text.image, (padding[0] + portrait.width, padding[1]))
        else:
            surface.blit(text.image, padding)

    def _draw_indicator(self, surface, text, indicator, lines, padding):
        """Draw animated idling symbol"""

        if text.idle and indicator:
            x = surface.get_width() - padding[0]
            y = text.linesize * lines + padding[1] - indicator.height
            indicator.animate(pygame.time.get_ticks())
            surface.blit(indicator.image, (x, y))

    def _draw_border(self, surface, border, corner, side, bg_color):
        """Draws the border and then fixes the corners if needed."""

        blocks = self._rotate_border_blocks(corner, side)

        # Animation is turned on.
        if border["animate"]:
            corner.animate(pygame.time.get_ticks())
            side.animate(pygame.time.get_ticks())
            self._blit_border(corner.image, surface, blocks, "CORNER")
            self._blit_border(side.image, surface, blocks, "SIDE")

        # Border is not going to have animation.
        else:
            self._blit_border(corner.image, surface, blocks, "CORNER")
            self._blit_border(side.image, surface, blocks, "SIDE")

        # Make pixels outside rounded corners transparent.
        fix_corners(
            surface=surface,
            corner_size=corner.size,
            bg_color=bg_color,
            colorkey=border["colorkey"],
        )

    def _rotate_border_blocks(self, corner, side):
        """Return dictionary with rotated border sprites."""

        blocks = {
            "TOP_LEFT": corner.image,
            "TOP_RIGHT": pygame.transform.rotate(corner.image, -90),
            "BOTTOM_LEFT": pygame.transform.rotate(corner.image, 90),
            "BOTTOM_RIGHT": pygame.transform.rotate(corner.image, 180),
            "LEFT": side.image,
            "TOP": pygame.transform.rotate(side.image, -90),
            "BOTTOM": pygame.transform.rotate(side.image, 90),
            "RIGHT": pygame.transform.rotate(side.image, 180),
        }

        return blocks


class TextBox(pygame.sprite.DirtySprite):
    """Class for creating simple text boxes.

    Args:
        text_width (int): max with of the printed text (required).
        pos (tuple): x & y coordinates to place the topleft corner of the box (required).
        text (str): Text to print.
        lines (int): number of printed lines.
        font_name (str): name of a installed font or path to a font file.
        font_size (int): size of the text font.
        font_color (tuple): text color, RGB value.
        bg_color (tuple): background color, RGB value.
        transparent (bool): if the box should be transparent or have a background color.

    """

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

        self.linesize = Text(text=" ", font=font_name, size=font_size).linesize

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
        """Set new text message to print out.

        Args:
            words (str): new text to print.

        """

        self.words = self._to_list(text)

    def reset(self, hard=False):
        """Reset dialog box.

        Args:
            hard (bool): False only cleans the box before moving to the next
                page to print the remaining words. True resets the entire class
                to default values to prepare to print new text from the beginning.
        """

        # Reset box to default values when whole message has been printed.
        if hard:
            self.__x, self.__y = 0, 0
            self.full = False
            self.idle = False
            self.image = pygame.Surface((self.__w, self.__h)).convert()
            self.image.fill(self.__bg_color)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.__pos

            if self.__transparent:
                self.image.set_colorkey(self.__bg_color)

        # Reset the filled box and continue with the remaining words.
        else:
            if self.full:
                self.image.fill(self.__bg_color)
                self.__x, self.__y = 0, 0
                self.full = False
                self.idle = False

    def update(self):
        """Update all changes that has been made to the text box."""

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
