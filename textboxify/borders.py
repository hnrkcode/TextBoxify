import os.path

from .settings import BORDER_DIR


# Border sprites.
DARK = {
    "corner": os.path.join(BORDER_DIR, "dark", "corner.png"),
    "side": os.path.join(BORDER_DIR, "dark", "side.png")
}
LIGHT = {
    "corner": os.path.join(BORDER_DIR, "light", "corner.png"),
    "side": os.path.join(BORDER_DIR, "light", "side.png")
}
