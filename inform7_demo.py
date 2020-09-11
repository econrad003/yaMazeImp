#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# inform7_demo.py - demonstrate Inform 7 code generation
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
#     4 Sep 2020 - Initial version
##############################################################################
"""
inform7_demo.py - demonstrate Inform 7 code generation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import argparse
import configparser
from inform7 import Inform7

def main(args):
    """generate some Inform7 code"""
        # get the configuration
    config = configparser.ConfigParser()
    config.read(args.input)

    inform7 = Inform7(config, filename=args.output) if args.output \
        else Inform7(config, console=True)
    inform7.generate()

if __name__ == "__main__":
    desc = "Inform 7 code generator"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', '--input', type=str, \
        default="demos/grid3d_config_demo.ini", \
        help="input configuration file name (extension: .ini)")
    parser.add_argument('-o', '--output', type=str, default=None, \
        help="output Inform 7 code (extension: .txt), else console")
    args = parser.parse_args()
    main(args)

# END: inform7_demo.py
