import os.path

from .settings import BORDER_DIR


# Border sprites.
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
