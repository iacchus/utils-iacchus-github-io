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
RESET_CODE = CODES['normal']

ATTRIBUTES = CODES.keys()

# This can be .format()'ted or used as f-string.
# "\x1b[{code}m":
ENCODE_ATTR = '{csi}{{code}}m'.format(csi=CSI)

# these are so to be used as f-strings:
#
# "\x1b[{fg_or_bg_code};2;{r};{g};{b}m":
ENCODE_RGB = '{csi}{{fg_or_bg_code}};2;{{r}};{{g}};{{b}}m'.format(csi=CSI)

# "\x1b[38;2;{r};{g};{b}m":
ENCODE_RGB_FG = ('{csi}{fg_or_bg_code};2;{{r}};{{g}};{{b}}m'
                 .format(csi=CSI, fg_or_bg_code=FG_CODE))

# "\x1b[48;2;{r};{g};{b}m":
ENCODE_RGB_BG = ('{csi}{fg_or_bg_code};2;{{r}};{{g}};{{b}}m'
                 .format(csi=CSI, fg_or_bg_code=BG_CODE))

# "\x1b[0m"
RESET = ENCODE_ATTR.format(code=RESET_CODE)

# matches as much as `#f3f3f3` as `f3f3f3` returning three hex groups, r, g, b.
HEX_COLOR_PATTERN = '^#?([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})$'

R_INDEX, G_INDEX, B_INDEX = (0, 1, 2)


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

def hex_to_hex(hex_color):
    """Converts hex color to rgb.

    It converts hexadecimal color in the format `#ffffff` or `ffffff` and
    returns a (r, g, b) tuple in a format like (255, 255, 255)

    Args:
        hex_color (str): A rgb color in hexadecimal format, like #ffffff or
            ffffff.
    """

    hex_tuple = re.match(HEX_COLOR_PATTERN, hex_color).groups()

    return "".join(hex_tuple)


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

        self.palettes = dict()


    def add_palette(self, name, foreground, background, *attrs):

        #
        # TODO: SANITIZE THESE ENTRIES. PEOPLE MAKE MISTAKES.
        #
        attributes = [attr for attr in attrs if attr in ATTRIBUTES]

        fg, bg = (hexcolor_to_rgb(foreground), hexcolor_to_rgb(background))

        if fg and bg:

            fg_seq = ENCODE_RGB_FG.format(r=fg[R_INDEX], g=fg[G_INDEX],
                                          b=fg[B_INDEX])

            bg_seq = ENCODE_RGB_BG.format(r=bg[R_INDEX], g=bg[G_INDEX],
                                          b=bg[B_INDEX])

            palette = dict()
            palette.update({
                'fg_rgb': hexcolor_to_rgb(foreground),
                'bg_rgb':hexcolor_to_rgb(background),
                'attrs': attributes,
                'fg_hex': hex_to_hex(foregroundd),
                'bg_hex': hex_to_hex(background),
                'fg_seq': fg_seq,
                'bg_seq': bg_seq,
                'attrs_seq':,
                'seq':,
                })

            self.palettes.update({name: (fg, bg, attributes)})


    def from_palette(self, data, palette):

        if palette in self.palettes.keys():

            fg, bg, attrs = self.palettes[palette]

            escaped_attrs = self._encode_attributes(attrs)
            escaped_fg_and_bg = self._encode_fg_bg(palette)

            colorized = str().join([escaped_attrs, escaped_fg_and_bg, data])

            return colorized


    def list_palettes(self):

        for key, value in self.palettes:
            pass


    def get_palette_escape_sequencies(self, palette):
        """Return the escape sequence for a palette.

        Escapes and returns the escape sequencies generated for a given
            palette.

        Args:
            palette (str): the palette name to get the sequences.
        """

        pass


    def delete_palette(self, pallete):
        """Deletes the palette."""

        if self.palettes.pop(palette, None):
            return True
        else:
            return False


    def _encode_attributes(self, attrs):

        escaped_attrs = str()

        for attr in attrs:
            escaped_attrs += ENCODE_ATTR.format(sci=SCI, code=CODES[attr])

        return escaped_attrs


    def _encode_fg_bg(self, palette, fg=True, bg=True):

        fg, bg, attrs = self.palettes[palette]

        encoded = str()

        if fg:
            r, g, b = fg
            encoded += ENCODE_RGB_FG.format(r=fg[R_INDEX], g=fg[G_INDEX],
                                            b=fg[B_INDEX])

        if bg:
            encoded += ENCODE_RGB_BG.format(r=bg[R_INDEX], g=bg[G_INDEX],
                                            b=bg[B_INDEX])

        return encoded
