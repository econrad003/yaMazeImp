#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# detab.py - replace tabs with spaces
# Eric Conrad
# Copyright ©2020 by Eric Conrad
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################
# Maintenance History:
#     16 May 2020 - Initial version
##############################################################################
"""
detab.py - replace tabs with spaces
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A utility to replace tabs in a file with spaces.

The default tab length is 8, the usual default for popular command line
shells (for example: bash, sh, MS-DOS command, or Windows cmd).
"""

default_tab = 8
epilog = "Do not use I/O redirection.  If INPUT and OUTPUT are the same" \
  + ", input will be copied to INPUT~ before detabbing."

def savecopy(src):
    """save a copy of the source file before detabbing
    
    If src~ exists, it will be overwritten."""
    import shutil
    
    dest = src + "~"
    shutil.copyfile(src, dest)
    return dest

def detab_line(line, tab):
    """replaces tabs by spaces in the given line"""
    detabbed = ""
    for i in range(len(line)):
        if line[i] == "\t":
            n = len(detabbed)         # current length
            m = n % tab               #   modulo tab length TL
            spaces = ' ' * (tab - m)  # from 1 to TL spaces
            detabbed += spaces
        else:
            detabbed += line[i]
    return detabbed

def detab(src, dest, tab):
    """detab source to destination
    
    Warning:
        If files src and dest have the same paths, the result depends on
        the operating system.  Note that function 'main' excludes this
        possibility."""
    import sys
    infile = open(src) if src else sys.stdin
    outfile = open(dest, 'w') if dest else sys.stdout
    for line in infile:
        detabbed = detab_line(line, tab)
        outfile.write(detabbed)
    if dest:
        outfile.close()
    if src:
        infile.close()

def main(args):
    """entry point for detab"""
    src = args.input
    dest = args.output
    tab = args.tab
    if src == dest and src is not None:
        src = savecopy(src)
    detab(src, dest, tab)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(epilog=epilog)
    parser.add_argument('-t', '--tab', metavar=('TABSTOP'),
                        default=default_tab, type=int,
                        help='tab length (default: %d)' % default_tab)
    parser.add_argument('-i', '--input', metavar='INPUT',
                        default=None,
                        help='the input file (default: stdin)')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
                        default=None,
                        help='the output file (default: stdout)')
    args = parser.parse_args()

    main(args)

# END: detab.py
