#!/usr/bin/env python3

# This program creates a tray for storing playing cards.  The tray should be
# cut from wood or plastic on a laser cutter.

# Note that CorelDraw's SVG import feature assumes a page size of 8.5 x 11.

# This program requires either:
# Python 3: pysvg-py3 (http://codeboje.de/pysvg/), version
# 0.2.2.post2, which can be downloaded from
# https://pypi.org/project/pysvg-py3/
# Python 2: pysvg (http://codeboje.de/pysvg/), version 0.2.2
# or version 0.2.2b, which can be downloaded from
# https://pypi.python.org/pypi/pysvg
#

# Copyright 2013-2018 Timur Tabi
# Ported to Python 3 2018 Bruce Fuda
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# This software is provided by the copyright holders and contributors "as is"
# and any express or implied warranties, including, but not limited to, the
# implied warranties of merchantability and fitness for a particular purpose
# are disclaimed. In no event shall the copyright holder or contributors be
# liable for any direct, indirect, incidental, special, exemplary, or
# consequential damages (including, but not limited to, procurement of
# substitute goods or services; loss of use, data, or profits; or business
# interruption) however caused and on any theory of liability, whether in
# contract, strict liability, or tort (including negligence or otherwise)
# arising in any way out of the use of this software, even if advised of
# the possibility of such damage.

import sys
import math
import pysvg.structure
from pysvg.turtle import Turtle, Vector
from optparse import OptionParser, OptionGroup

# How CorelDraw defines a Hairline width
HAIRLINE = 0.01

class SVG(object):
    def __init__(self, width, height, filename, start = Vector(0, 0)):
        global o, a

        self.t = Turtle(stroke=o.color, strokeWidth=str(o.line))
        self.width = int(math.ceil(width))
        self.height = int(math.ceil(height))
        self.filename = filename
        self.t.moveTo(start)
        self.t.setOrientation(Vector(1, 0))
        self.t.penDown()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.t.finish()
        print(self.t.getXML())

        # Some versions of pysvg have ".Svg" and some have ".svg", so just
        # try one at a time until it works.
        try:
            self.svg = pysvg.structure.Svg(width='%smm' % self.width, height='%smm' % self.height)
        except AttributeError:
            self.svg = pysvg.structure.svg(width='%smm' % self.width, height='%smm' % self.height)
        self.svg.set_viewBox('0 0 %s %s' % (self.width, self.height))

        self.t.addTurtlePathToSVG(self.svg)
        print('Saving to %s (size: %umm x %umm)' % (self.filename, self.width, self.height))
        self.svg.save(self.filename)

    def r(self, before = None, after = None):
        if before:
            self.t.forward(before)
        self.t.right(90)
        if after:
            self.t.forward(after)

    def l(self, before = None, after = None):
        if before:
            self.t.forward(before)
        self.t.left(90)
        if after:
            self.t.forward(after)

    def f(self, length):
        self.t.forward(length)

    def v(self, x, y):
        return Vector(x, y)

    def here(self):
        return self.t.getPosition()

    def up(self):
        self.t.penUp()

    def down(self):
        self.t.penDown()

    # Move to a specific position
    def move(self, x = 0, y = 0, v = None):
        if not v:
            v = Vector(x, y)
        self.t.moveTo(v)

    # Move relative to the current position
    def shift(self, x = 0, y = 0, v = None):
        if not v:
            v = Vector(x, y)
        self.t.moveTo(self.t.getPosition() + v)

    # Move to a specific absolute position without drawing
    def relocate(self, x = 0, y = 0, v = None):
        if not v:
            v = Vector(x, y)
        self.t.penUp()
        self.t.moveTo(v)
        self.t.penDown()

    def east(self):
        self.t.setOrientation(Vector(1, 0))

    def north(self):
        self.t.setOrientation(Vector(0, -1))

    def west(self):
        self.t.setOrientation(Vector(-1, 0))

    def south(self):
        self.t.setOrientation(Vector(0, 1))

    def notch_l(self, width, length):
        self.t.left(90)
        self.t.forward(width)
        self.t.right(90)
        self.t.forward(length)
        self.t.right(90)
        self.t.forward(width)
        self.t.left(90)

    def notch_r(self, width, length):
        self.t.right(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.forward(length)
        self.t.left(90)
        self.t.forward(width)
        self.t.right(90)

    def rectangle_r(self, length, width):
        self.t.forward(length)
        self.t.right(90)
        self.t.forward(width)
        self.t.right(90)
        self.t.forward(length)
        self.t.right(90)
        self.t.forward(width)
        self.t.right(90)

    def rectangle_l(self, length, width):
        self.t.forward(length)
        self.t.left(90)
        self.t.forward(width)
        self.t.left(90)
        self.t.forward(length)
        self.t.left(90)
        self.t.forward(width)
        self.t.left(90)

    def semicircle_r(self, length, segments):
        theta = 180.0 / segments
        radius = length / 2
        segment = 2 * radius * math.sin(math.radians(theta / 2))

        direction = self.t.getOrientation()

        self.t.right(90 - theta / 2)
        for i in range(0, segments):
            self.t.forward(segment)
            self.t.left(theta)

        self.t.setOrientation(direction)


def front_and_back():
    global o, a

    with SVG(o.insert_width, o.h, 'front_and_back.svg') as t:
        # Top
        t.f(o.insert_width)
        t.r()

        # Right edge
        t.f(o.notch)
        t.notch_r(o.m, o.notch)
        t.f(o.notch)
        t.notch_r(o.m, o.notch)
        t.f(o.h - 4 * o.notch)
        t.r()

        # Bottom
        t.f(o.insert_width)
        t.r()

        # Left edge
        t.f(o.h - 4 * o.notch)
        t.notch_r(o.m, o.notch)
        t.f(o.notch)
        t.notch_r(o.m, o.notch)
        t.f(o.notch)
        t.r()

        # Holes in between each row

        t.south()
        for i in range(1, o.r):
            t.relocate((o.m + o.w) * i, o.notch)
            t.rectangle_l(o.notch, o.m)
            t.up()
            t.shift(y = 2 * o.notch)
            t.down()
            t.rectangle_l(o.notch, o.m)

def dividers():
    global o, a

    with SVG(o.insert_depth, o.h, 'divider.svg') as t:
        t.relocate(o.m, 0)

        for i in range(0, o.num_slots - 1):
            t.f(o.s)
            t.notch_r(o.h / 2, o.m)
        t.move(o.insert_depth - o.m, 0)
        t.r()

        t.f(o.notch)
        t.notch_l(o.m, o.notch)
        t.f(o.notch)
        t.notch_l(o.m, o.notch)
        t.f(o.notch)
        t.r()

        t.move(o.m, o.h)
        t.r()

        t.f(o.notch)
        t.notch_l(o.m, o.notch)
        t.f(o.notch)
        t.notch_l(o.m, o.notch)
        t.f(o.notch)

def slots():
    global o, a

    with SVG(o.w + 2 * o.m, o.h, 'slot_full.svg') as t:
        t.f(o.m + o.w / 3)
        t.r()
        t.f(o.h / 5)
        t.l()
        t.semicircle_r(o.w / 3, 20)
        t.l()
        t.f(o.h / 5)
        t.r()
        t.f(o.m + o.w / 3)
        t.r()

        t.f(o.h / 2)
        t.r()
        t.f(o.m)

        t.notch_l(o.h / 2, o.w)

        t.f(o.m)
        t.r()
        t.f(o.h / 2)

    with SVG(o.w + 2 * o.m, o.h, 'slot_inner.svg') as t:
        t.f(o.m + o.w / 3)
        t.r()
        t.f(o.h / 5)
        t.l()
        t.semicircle_r(o.w / 3, 20)
        t.l()
        t.f(o.h / 5)
        t.r()
        t.f(o.m + o.w / 3)
        t.r()

        t.f(o.h / 2)
        t.r()
        t.f(o.m / 2)

        t.notch_l(o.h / 2, o.w + o.m)

        t.f(o.m / 2)
        t.r()
        t.f(o.h / 2)

    with SVG(o.w + 2 * o.m, o.h, 'slot_outer.svg') as t:
        t.f(o.m + o.w / 3)
        t.r()
        t.f(o.h / 5)
        t.l()
        t.semicircle_r(o.w / 3, 20)
        t.l()
        t.f(o.h / 5)
        t.r()
        t.f(o.m + o.w / 3)
        t.r()

        t.f(o.h / 2)
        t.r()
        t.f(o.m)

        t.notch_l(o.h / 2, o.w + o.m / 2)

        t.f(o.m / 2)
        t.r()
        t.f(o.h / 2)

# Defaults for Dominion Victory cards
parser = OptionParser(usage="usage: %prog [options]")
group = OptionGroup(parser, "Box dimensions", "These options are used to validate the other options. "
    "They default to the Hobby Lobby All Media Artist's Supply Sketch Box (SKU: 125005).")
group.add_option("--box-height", dest="bh", help="interior box height in millimeters (default=%default)",
                  type="int", default = 66 + 42)
group.add_option("--box-width", dest="bw", help="interior box width in millimeters (default=%default)",
                  type="int", default = 400)
group.add_option("--box-depth", dest="bd", help="interior box depth in millimeters (default=%default)",
                  type="int", default = 306)
parser.add_option_group(group)

parser.add_option("-W", dest="w", help="divider width (0=calculate) (default=%default)",
                  type="int", default = 60)
parser.add_option("-H", dest="h", help="divider height (default=%default)",
                  type="int", default = 80)

parser.add_option("-m", dest="m", help="material thickness (default=%default)",
                  type="float", default = 3)
parser.add_option("-r", dest="r", help="number of rows (0=calculate) (default=%default)",
                  type="int", default = 0)
parser.add_option("-n", dest="n", help="max number of slots per row (0=calculate) (default=%default)",
                  type="int", default = 8)
parser.add_option("-s", dest="s", help="approximate slot size (0=calculate) (default=%default)",
                  type="int", default = 0)
parser.add_option('-c', dest='color', help='drawing color (default=%default)',
                  type='string', default = 'red')
parser.add_option('-l', dest='line', help='line width (default=%default)',
                  type='float', default = HAIRLINE)

(o, a) = parser.parse_args()

# Verify options

if o.h > o.bh:
    print('Error: divider height of %f is taller than box interior.' % o.h)
    sys.exit(1)

if o.r == 0 and o.w == 0:
    print('Error: -w and -r cannot both be zero')
    sys.exit(1)

if o.s == 0 and o.n == 0:
    print('Error: -n and -s cannot both be zero')
    sys.exit(1)

if o.s > 0 and o.n > 0:
    print('Error: One of -n or -s must be calculated. If using -s, set -n 0')
    sys.exit(1)

if o.r == 0:
    o.r = int(math.floor((o.bw - o.m) / (o.m + o.w)))

if o.w == 0:
    o.w = ((o.bw - o.m) / o.r) - o.m

o.insert_width = (o.w * o.r) + (o.m * (o.r + 1))
if (o.insert_width) > o.bw:
    print('Error: insert width of %f exceeds specified box interior width of %f' % (o.insert_width, o.bw))
    sys.exit(1)

# Because we always calculate the slot size, the insert as always exactly
# as deep as the box interior.
o.insert_depth = o.bd

print
print('Interior box height: %umm' % o.bh)
print('Interior box width: %umm' % o.bw)
print('Interior box depth: %umm' % o.bd)
print('Material thickness: %.2fmm' % o.m)
print('Number of rows: %u' % o.r)
print('Row width: %umm' % o.w)
if o.bw > o.insert_width:
    print('Gap between insert and box: %.2fmm' % (o.bw - o.insert_width))
# Calculate some values

# The notch height and also the spacing between the notches.  To avoid
# rounding errors, the spacing below the bottom notch is calculated
# separately as the remainder.
o.notch = math.floor(o.h / 5)
print('Notch height: %umm' % o.notch)

# Adjust the slot size.
inside_depth = o.bd - (2 * o.m)
if o.n > 0:
  num_slots = o.n
else:
  num_slots = round((inside_depth + o.m) / (o.s + o.m))
o.s = ((inside_depth + o.m) / num_slots) - o.m
o.num_slots = int(num_slots)
print('Number of slots: %u' % o.num_slots)
print('Adjusted slot size: %.2fmm' % o.s)
print

front_and_back()
dividers()
slots()
