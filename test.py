#!/usr/bin/env python

from utils.colorize import Colorize
#from utils.colorize import colorize

a = Colorize()
a.add_palette(name='blue', foreground='#ffffff', background="#333366")
a.add_palette(name='normal', foreground='#ffffff', background="#000000")

b = a.from_palette('this is a test', 'blue')
c = a.from_palette('this is a test', 'normal')

print(b)
print(c)
