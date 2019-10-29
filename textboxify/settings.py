import os.path

# Paths to package data files.
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
BORDER_DIR = os.path.join(DATA_DIR, "border")
INDICATOR_DIR = os.path.join(DATA_DIR, "indicator")
PORTRAIT_DIR = os.path.join(DATA_DIR, "portrait")

# Default sprite files.
DEFAULT_CORNER = os.path.join(BORDER_DIR, "default", "corner.png")
DEFAULT_SIDE = os.path.join(BORDER_DIR, "default", "side.png")
DEFAULT_INDICATOR = os.path.join(INDICATOR_DIR, "idle.png")
DEFAULT_PORTRAIT = os.path.join(PORTRAIT_DIR, "placeholder.png")