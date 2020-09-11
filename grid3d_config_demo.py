#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# grid3d_config_demo.py - test configuration in grid3d
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
grid3d_config_demo.py - test configuration in grid3d
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from math import sqrt, ceil
import argparse
import matplotlib.pyplot as plt

from grid3d import Grid3D
from recursive_backtracker import Recursive_Backtracker as DFS
from layout_plot3d import Plot3D_Layout

def render(args, maze, filename, title):
    """render a maze
    
    This is an entry point to this script.  If the script is run
    from the command line, a weave maze will be created and carved
    using the High Card Wins algorithm.

    maze = a rectangular or weave maze to be rendered
    filename = filename or pathname for output
    title = a title for the plot
    """

        # generate the plots
    print("Plotting maze...")
    n = ceil(sqrt(args.height))
    dim = (n, n)
    layout = Plot3D_Layout(maze, plt, dim, title=title)
    layout.draw_grid()
    print("Saved to " + filename)
    layout.render(filename)
    if args.show:
        plt.show()
    return layout

def make_3D_grid(m, n, height, maze_name):
    """create a rectangular grid"""
    grid = Grid3D(m, n, height, name=maze_name, inset=0.2)
    return grid

def make_config(args):
    """create a configuration file"""
    m, n = args.dim
    maze = make_3D_grid(m, n, args.height, "3-D Maze")
    print("%d cells" % len(maze))

    print("Recursive Backtracker (DFS): Carve a maze...")
    DFS.on(maze)

    filename = "demos/grid3d_config_demo"
    maze.save_config(filename + ".ini")

    title = "Three Dimensional Oblong Grid"
    render(args, maze, filename + ".png", title)

def main(args):
    """create config or build from config"""
    make_config(args)

if __name__ == "__main__":
    desc = "High-Card-Wins algorithm demonstration"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', metavar=('ROWS', 'COLS'), \
        nargs=2, type=int, default=[5, 7], \
        help='planar dimensions (default [5, 7])')
    parser.add_argument('--height', type=int, default=3, \
        help='the height of the maze')
    parser.add_argument('--show', action='store_true', \
        help='show plots before exiting')
    parser.add_argument('--build', action='store_true', \
        help='build from demos/grid3d_build.ini')
    args = parser.parse_args()
    main(args)

# END: grid3d_config_demo.py
