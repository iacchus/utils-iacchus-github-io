#!/usr/bin/env python

from utils.colorize import Colorize
#from utils.colorize import colorize

a = Colorize()
a.add_palette(name='blue', foreground='#ffffff', background="#333366")
a.add_palette(name='normal', foreground='#ffffff', background="#000000")
a.add_palette(name='bold', foreground='#ffffff', background="#333366",
              attrs=['bold'])
a.add_palette(name='italic', foreground='#ffffff', background="#333366",
              attrs=['italic'])

b = a.from_palette('this is a test', 'blue')
c = a.from_palette('this is a test', 'normal')
d = a.from_palette('this is a test', 'bold')
e = a.from_palette('this is a test', 'italic')

print(a.palettes['bold'])

print(b)
print(c)
print(d)
print(e)

a.list_palettes(use_pprint=True)
