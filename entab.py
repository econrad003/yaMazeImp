#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# entab.py - replace spaces with tabs
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
detab.py - replace spaces with tabs
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A utility to replace two or more spaces in a file with tabs, when
appropriate.  If there are tabs in the file, they will be temporarily
detabbed, i.e, replaced by cached spaces.

Note that while the results of detabbing are necessarily unique, there
is more than one way to entab a file.  Detabbing a file and entabbing
the output will not necessarily yield identical files.  But entabbing
the output of entab will not yield any changes.

The default tab stop is 8, consistent with the usual tab stop setting in
a command shell (for example: bash, sh, MS-DOS command or Windows cmd).
"""

default_tab = 8
epilog = "Do not use I/O redirection.  If INPUT and OUTPUT are the same" \
  + ", input will be copied to INPUT~ before detabbing."

def savecopy(src):
    """save a copy of the source file before entabbing
    
    If src~ exists, it will be overwritten."""
    import shutil
    
    dest = src + "~"
    shutil.copyfile(src, dest)
    return dest

def entab_line(line, tab):
    """replaces spaces by tabs in the given line"""
    entabbed = ""
    spaces = ""             # cache for spaces
    n = 0
    for i in range(len(line)):
        if n % tab is 0 and spaces:
            entabbed += " " if len(spaces) is 1 else "\t"
            spaces = ""
        if line[i] == "\t":       # cache with spaces
            m = n % tab
            spaces += " " * (tab - m)
            n += tab - m
        elif line[i] == " ":
            spaces += " "         # cache
            n += 1
        else:                     # neither space nor tab
            if spaces:
                entabbed += spaces
                spaces = ""
            entabbed += line[i]
            n += 1
    return entabbed

def entab(src, dest, tab):
    """entab source to destination
    
    Warning:
        If files src and dest have the same paths, the result depends on
        the operating system.  Note that function 'main' excludes this
        possibility."""
    import sys
    infile = open(src) if src else sys.stdin
    outfile = open(dest, 'w') if dest else sys.stdout
    for line in infile:
        entabbed = entab_line(line, tab)
        outfile.write(entabbed)
    if dest:
        outfile.close()
    if src:
        infile.close()

def main(args):
    """entry point for entab"""
    src = args.input
    dest = args.output
    tab = args.tab
    if src == dest and src is not None:
        src = savecopy(src)
    entab(src, dest, tab)

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

# END: entab.py
