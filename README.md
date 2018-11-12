# svg-organizer
Laser-cut storage box organizer for playing cards

This Python program creates SVG laser-cutter patterns for board game inserts.
The insert holds rows of cards.  The best example would be for drafting games
like Dominion, or CCGs/LCGs like Magic the Gathering or Lord of the Rings.

Compatible with both Python 2 and 3. Tested with Python 2.7.15 and 3.7.0.

## Installation
After cloning/downloading the repository, install python package requirements
using pip:

`pip install -r requirements.txt --user`

or with Python 3:

`pip3 install -r requirements.txt --user`

This will install the required version of the `pysvg` package for Python 2, or `pysvg-py3` for Python 3.

Alternatively, download the packages via PyPI - direct links available in the script.

## Usage

Execute the script with default parameters as follows:

`./svg-organiser.py`

This will use the default values to generate three files that can be cut on a laser cutter:

`front_and_back.svg`: cut two of these - one for the front, one for the back

`divider.svg`: cut n+1 of these, where n is the number of rows

Cut as many of these as you want:

`slot_full.svg`: slots with cut-outs on both sides that are the thickness of the material. These cannot sit next to each other in adjacent rows since they take up a whole cut-out in a divider.

`slot_inner.svg`: slots with cut-outs on both sides that are half of the thickness of the material. These can sit next to each other in adjacent rows and share a single cut-out in the divider, and should only be used in inner rows.

`slot_outer.svg`: slots where the cut-out on one side is the thickness of the material, but on the other it is half thickness. These are ideal for outside rows where the slot is adjacent to another slot in an inner row.

You can specify options to customise the dimensions of the organizer. For a full list of available options, run the script using the `-h` option:

`./svg-organiser.py -h`
