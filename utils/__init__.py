import re

from . import fzf
from . import colorize

# http://code.activestate.com/recipes/134892/
class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):

        import tty
        import sys

    def __call__(self):

        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

