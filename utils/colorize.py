import re

CSI = '\x1b['  # Control Sequence Indicator

CODES = {
    'normal': 0,
    'bold': 1,
    'faint': 2,
    'italic': 3,
    'underline': 4,
    'slowblink': 5,
    'rapidblink': 6,
    'reversevideo': 7,
    'conceal': 8,
    'crossedout': 9,
    'defaultfont': 10,
    'alternatefont1': 11,
    'alternatefont2': 12,
    'alternatefont3': 13,
    'alternatefont4': 14,
    'alternatefont5': 15,
    'alternatefont6': 16,
    'alternatefont7': 17,
    'alternatefont8': 18,
    'alternatefont9': 19,
    'fraktur': 20,
    'boldoffordoubleunderline': 21,
    'normalcolororintensity': 22,
    'notitalic': 23,
    'underlineoff': 24,
    'blinkoff': 25,
    'inverseoff': 27,
    'reveal': 28,
    'notcrossedout': 29,
    'fgcolor1': 30,
    'fgcolor2': 31,
    'fgcolor3': 32,
    'fgcolor4': 33,
    'fgcolor5': 34,
    'fgcolor6': 35,
    'fgcolor7': 36,
    'fgcolor8': 37,
    'setforegroundcolor': 38,
    'defaultforegroundcolor': 39,
    'bgcolor1': 40,
    'bgcolor2': 41,
    'bgcolor3': 42,
    'bgcolor4': 43,
    'bgcolor5': 44,
    'bgcolor6': 45,
    'bgcolor7': 46,
    'bgcolor8': 47,
    'setbackgroundcolor': 48,
    'defaultbackgroundcolor': 49,
    'framed': 51,
    'encircled': 52,
    'overlined': 53,
    'notframedoorencircled': 54,
    'notoverlined': 55,
    'ideogramunderline': 60,
    'ideogramdoubleunderline': 61,
    'ideogramoverline': 62,
    'ideogramdoubleoverline': 63,
    'ideogramstress marking': 64,
    'ideogramattributesoff': 65,
    'brightfgcolor1': 90,
    'brightfgcolor2': 91,
    'brightfgcolor3': 92,
    'brightfgcolor4': 93,
    'brightfgcolor5': 94,
    'brightfgcolor6': 95,
    'brightfgcolor7': 96,
    'brightfgcolor8': 97,
    'brightbgcolor1': 100,
    'brightbgcolor2': 101,
    'brightbgcolor3': 102,
    'brightbgcolor4': 103,
    'brightbgcolor5': 104,
    'brightbgcolor6': 105,
    'brightbgcolor7': 106,
    'brightbgcolor8': 107,
}

FG_CODE = CODES['setforegroundcolor']
BG_CODE = CODES['setbackgroundcolor']

ATTRIBUTES = CODES.keys()

#RESET = '\033[0m'
#BOLD = '\033[1m'
#FAINT = '\033[2m'
#ITALIC = '\033[3m'
#UNDERLINE = '\033[4m'
#SLOW_BLINK = '\033[5m'

# This can be .format()'ted or used as f-string.
# "\x1b[{code}m":
ENCODE_ATTR = '{csi}{{code}}m'.format(csi=CSI)

# these are so to be used as f-strings:
#
# "\x1b[{fg_or_bg_code};{r};{g};{b}m":
ENCODE_RGB = '{csi}{{fg_or_bg_code}};{{r}};{{g}};{{b}}m'.format(csi=CSI)

# "\x1b[38;{r};{g};{b}m":
ENCODE_RGB_FG = ('{csi}{fg_or_bg};{{r}};{{g}};{{b}}m'
                 .format(csi=CSI, fg_or_bg_code=FG_CODE))

# "\x1b[48;{r};{g};{b}m":
ENCODE_RGB_BG = ('{csi}{fg_or_bg};{{r}};{{g}};{{b}}m'
                 .format(csi=CSI, fg_or_bg_code=BG_CODE))

# matches as much as `#f3f3f3` as `f3f3f3` returning three hex groups, r, g, b.
HEX_COLOR_PATTERN = '^#?([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})$'

#R, G, B = (0, 1, 2)
#
#def _escape(r, g, b, background=False):
#
#    #return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
#    fg_or_bg = 48 if background else 38
#
#    escaped = f'\033[{fg_or_bg};2;{r};{g};{b}m'
#
#    return escaped

def hexcolor_to_rgb(hex_color):
    """Converts hex color to rgb.

    It converts hexadecimal color in the format `#ffffff` or `ffffff` and
    returns a (r, g, b) tuple in a format like (255, 255, 255)

    Args:
        hex_color (str): A rgb color in hexadecimal format, like #ffffff or
            ffffff.
    """

    hex_tuple = re.match(HEX_COLOR_PATTERN, hex_color).groups()
    rgb = tuple(map(lambda x: int(x, base=16), hex_tuple))

    return rgb

def colorize(data, frk, fg='FFFFFF', bg='000000'):

    foreground, background = (map(lambda x: hexcolor_to_rgb(x), (fg, bg)))

    #print(foreground, background)

    if foreground and background:
        colorized = (f" {frk:03} — " + _escape(*foreground) + _escape(*background, True)
                     + data +  f'\033[{frk}m ' + data + RESET)

    else:
        return data

    return colorized

# https://github.com/simplegadget512/Truecolor/blob/master/truecolor.py
# https://unix.stackexchange.com/questions/404414/print-true-color-24-bit-test-pattern
# https://mudhalla.net/tintin/info/truecolor/
# https://gist.github.com/XVilka/8346728
# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# http://ascii-table.com/ansi-escape-sequences-vt-100.php
# https://wiki.bash-hackers.org/scripting/terminalcodes
class Colorize:

    def __init__(self):

        self.palette = dict()

    # def add_palette(self, name, foreground, background, *attrs, **other):
    def add_palette(self, name, foreground, background, *attrs):

        attributes = [attr for attr in attrs if attr in ATTRIBUTES]

        fg, bg = (hexcolor_to_rgb(foreground), hexcolor_to_rgb(background))

        if fg and bg:
            self.palette.update({name: (fg, bg, attributes)})

    def from_palette(self, data, palette):

        if palette in self.palette.keys():

            fg, bg = self.palette[palette]
            escaped_attrs = encode_attributes(attributes)
            colorized = _escape(*fg) + _escape(*bg, True) + data + RESET

            return colorized

    def _encode_attributes(self, attrs):

        escaped_attrs = str()
        for attr in attrs:
            escaped_attrs += ENCODE.format(sci=SCI, code=CODES[attr])

        return escaped_attrs


    def _encode_fg_bg(self, palette, fg=True, bg=True):

        encoded = str()

        if fg:
            r, g, b =
            encoded = ENCODE_RGB_FG.format()
            pass
        if bg:
            pass

        return encoded
