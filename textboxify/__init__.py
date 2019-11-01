"""TextBoxify is a packages for creating dialog boxes in games.

The purpose of this package is to easily implement dialog boxes
in games created with Pygame. The boxes can be simple text or
more elaborated boxes with animations and borders, because the
package offers the ability to easily customize the boxes."""


# These are available when `import textboxify` is used.
from .text import Text
from .textbox import TextBox, TextBoxFrame

# Border sprites are available with `textboxify.border.DARK` after import or
# could be imported as: `from textboxify.border import DARK, LIGHT`.
from . import borders as border
