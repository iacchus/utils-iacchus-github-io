import re

CSI = '\x1b['  # Control Sequence Indicator

dict CODES = {
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
    'foregroundcolor1': 30,
    'foregroundcolor2': 31,
    'foregroundcolor3': 32,
    'foregroundcolor4': 33,
    'foregroundcolor5': 34,
    'foregroundcolor6': 35,
    'foregroundcolor7': 36,
    'foregroundcolor8': 37,
    'setforegroundcolor': 38,
    'defaultforegroundcolor': 39,
    'backgroundcolor1': 40,
    'backgroundcolor2': 41,
    'backgroundcolor3': 42,
    'backgroundcolor4': 43,
    'backgroundcolor5': 44,
    'backgroundcolor6': 45,
    'backgroundcolor7': 46,
    'backgroundcolor8': 47,
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
    'brightforegroundcolor1': 90,
    'brightforegroundcolor2': 91,
    'brightforegroundcolor3': 92,
    'brightforegroundcolor4': 93,
    'brightforegroundcolor5': 94,
    'brightforegroundcolor6': 95,
    'brightforegroundcolor7': 96,
    'brightforegroundcolor8': 97,
    'brightbackgroundcolor1': 100,
    'brightbackgroundcolor2': 101,
    'brightbackgroundcolor3': 102,
    'brightbackgroundcolor4': 103,
    'brightbackgroundcolor5': 104,
    'brightbackgroundcolor6': 105,
    'brightbackgroundcolor7': 106,
    'brightbackgroundcolor8': 107,
}




RESET = '\033[0m'
BOLD = '\033[1m'
FAINT = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
SLOW_BLINK = '\033[5m'

ENCODE = '{CSI}{code}m'

HEX_COLOR_PATTERN = '^#?([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})$'

R, G, B = (0, 1, 2)

def _escape(r, g, b, background=False):

    #return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
    fg_or_bg = 48 if background else 38

    escaped = f'\033[{fg_or_bg};2;{r};{g};{b}m'

    return escaped

def hexcolor_to_rgb(hex_color):

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

    def add_palette(self, name, foreground, background):

        fg, bg = (hexcolor_to_rgb(foreground), hexcolor_to_rgb(background))

        if fg and bg:
            self.palette.update({name: (fg, bg)})

    def from_palette(self, data, palette):

        if palette in self.palette.keys():

            fg, bg = self.palette[palette]
            colorized = _escape(*fg) + _escape(*bg, True) + data + RESET

            return colorized
