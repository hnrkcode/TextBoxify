import os.path

# Paths to package data files.
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
BORDER_DIR = os.path.join(DATA_DIR, "border")
INDICATOR_DIR = os.path.join(DATA_DIR, "indicator")
PORTRAIT_DIR = os.path.join(DATA_DIR, "portrait")

# Default sprite files.
DEFAULT_INDICATOR = {
    "file": os.path.join(INDICATOR_DIR, "idle.png"),
    "size": (25, 17),
}
DEFAULT_PORTRAIT = {
    "file": os.path.join(PORTRAIT_DIR, "placeholder.png"),
    "size": (100, 100),
}
