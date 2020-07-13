#!/usr/bin/env python

from utils import Colorize
from utils import colorize

a = Colorize()
a.add_palette(name='blue', foreground='#ffffff', background="#333366")
a.add_palette(name='normal', foreground='#ffffff', background="#000000")

b = a.from_palette('this is a test', 'blue')
c = a.from_palette('this is a test', 'normal')

#print(b)

#print(colorize('HELLO BUDDY',0, fg='ffffff', bg='663333'))
#print(colorize('HELLO BUDDY',0, fg='ffffff', bg='000000'))

for i in range(0, 108):
    #print(colorize("HELLO WORLD!", i))
    #print(colorize('HELLO BUDDY', i, fg='ffffff', bg='663333'))
    print(colorize('HELLO BUDDY', i, fg='ffffff', bg='000000'))
