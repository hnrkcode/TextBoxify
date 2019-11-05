"""Borders included by default in the package.

This module contains borders that you can use to customize your
dialog boxes appearances with.

You can also create your own borders by creating python dictionaries that
contains same keys, but with values to your own sprite settings and pass it as
an argument to the TextBoxFrame class.

Note:
    Border variables are python dictionaries and contains five key, value pairs.

    - "corner" is the top left corner sprite.
    - "side" is the left side sprite.
    - "size" is a list that contains the sprites width and height.
    - "colorkey" is a tuple with an RGB value that can be removed from the sprite.
    - "animate" is a boolean value that tells if the border is animated.

Attributes:
    DEFAULT (dict):
    DARK (dict):
    LIGHT (dict):
    BLINK (dict): this is an animated border.
    BARBER_POLE (dict): this is an animated border.

"""


import os.path

from .settings import BORDER_DIR


# Border sprites.
DEFAULT = {
    "corner": os.path.join(BORDER_DIR, "default", "corner.png"),
    "side": os.path.join(BORDER_DIR, "default", "side.png"),
    "size": [10, 10],
    "colorkey": None,
    "animate": False,
}
DARK = {
    "corner": os.path.join(BORDER_DIR, "dark", "corner.png"),
    "side": os.path.join(BORDER_DIR, "dark", "side.png"),
    "size": [10, 10],
    "colorkey": (0, 255, 38),
    "animate": False,
}
LIGHT = {
    "corner": os.path.join(BORDER_DIR, "light", "corner.png"),
    "side": os.path.join(BORDER_DIR, "light", "side.png"),
    "size": [5, 5],
    "colorkey": (0, 255, 38),
    "animate": False,
}
BLINK = {
    "corner": os.path.join(BORDER_DIR, "blink", "corner.png"),
    "side": os.path.join(BORDER_DIR, "blink", "side.png"),
    "size": [15, 15],
    "colorkey": (11, 219, 6),
    "animate": True,
}
BARBER_POLE = {
    "corner": os.path.join(BORDER_DIR, "barber_pole", "corner.png"),
    "side": os.path.join(BORDER_DIR, "barber_pole", "side.png"),
    "size": [20, 20],
    "colorkey": (11, 219, 6),
    "animate": True,
}
