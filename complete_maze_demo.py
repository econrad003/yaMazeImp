#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# complete_maze_demo.py - test the complete maze algorithm
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
#     2 Sep 2020 - Initial version
##############################################################################
"""
complete_maze_demo.py - test the complete maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import argparse

from rectangular_grid import Rectangular_Grid
from complete_maze import Complete_Maze

def make_grid():
    """create a rectangular grid"""
    grid = Rectangular_Grid(4, 5)
    return grid

def display_unicode(grid):
    """display a small maze in the terminal using unicode"""
    m, n = grid.rows, grid.cols
    source = grid[0, n-1]               # start cell
    terminus = grid[m-1, 0]             # finish cell
    source.kwargs["content"] = "S"
    terminus.kwargs["content"] = "T"
    print(grid.unicode())

def main(args):
    """run the complete maze algorithm on a 4x5 grid"""
    maze = make_grid()
    Complete_Maze.on(maze)
    display_unicode(maze)

if __name__ == "__main__":
    desc = "Complete maze algorithm demonstration"
    parser = argparse.ArgumentParser(description=desc)
    args = parser.parse_args()
    main(args)

# END: complete_maze_demo.py
