import re

from . import fzf

RESET = '\033[0m'
HEX_COLOR_PATTERN = '^#?([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})$'

R, G, B = (0, 1, 2)

def _escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def hexcolor_to_rgb(hex_color):

    hex_tuple = re.match(HEX_COLOR_PATTERN, hex_color).groups()
    rgb = tuple(map(lambda x: int(x, base=16), hex_tuple))

    return rgb

def colorize(data, fg='FFFFFF', bg='000000'):

    foreground = hexcolor_to_rgb(fg)
    background = hexcolor_to_rgb(bg)

    print(foreground, background)

    if foreground and background:
        colorized = (_get_color_escape(foreground[R], foreground[G], foreground[B])
                  + _get_color_escape(background[R], background[G], background[B], True)
                  + data
                  + RESET)

    else:
        return data

    return colorized

class Colorize:

    def __init__(self):

        self.palette = tuple()

    def add_palette(self, name, foreground, background):

        fg, bg = (hexcolor_to_rgb(foreground), hexcolor_to_rgb(background))

        if fg and bg:
            self.palette.update({name: (fg, bg)})

    def from_palette(self, data, palette):

        if palette in self.palette.keys():

            fg, bg = self.palette[palette]
            colorized = _escape(*fg) + _escape(*bg) + data + RESET

