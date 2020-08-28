#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# polar_ellers_demo.py - demonstrate Eller's algorithm on a polar grid
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
#     28 Aug 2020 - Initial version
##############################################################################
"""
polar_ellers_demo.py - demonstrate Eller's algorithm on a polar grid
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Demonstrate the use of the implementation of Eller's algorithm by carving a
maze on a polar grid. 

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
from layout_plot_polar import Polar_Layout

def make_grid(m, n, s):
    """create a rectangular grid
    
    Arguments:
        m - the number of latitudinal rows
        n - the number of cells located at the pole
        s - split length
    """
    from polar_grid import Polar_Grid

    print("Grid: Polar_Grid(%d, poleCells=%d, splitAt=%d)" % (m, n, s))
    grid = Polar_Grid(m, poleCells=n, splitAt=s)
    return grid

def generate_maze(grid, bias1=0.5, bias2=0.5):
    """use Eller's algorithm"""
    from ellers import Ellers
    from polar_ellers import Polar_Ellers_State

    print("Carve maze using Eller's algorithm...")
    start = Polar_Ellers_State(grid)
    Ellers.on(grid, start, bias1, bias2)

def render(maze, filename):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, a polar grid will be created and a perfect
    maze will be carved from it using Eller's algorithm.  No tweaking
    is available here for renderng.

    maze = a carved maze.
    filename = filename or pathname for output.
    """

    layout = Polar_Layout(maze, plt, title="Eller's algorithm")
    layout.ax.set(aspect=1)
    layout.ax.axis('off')
    layout.draw_grid()

    print("Saved to " + filename)
    layout.fig.savefig(filename)
    return layout

def main(args):
    """entry point"""
    print("Eller's Algorithm Test Script (Polar Maze)...")
    print(args)
    maze = make_grid(args.rows, args.poleCells, args.splitAt)
    generate_maze(maze, args.bias1, args.bias2)
    basename = "polar_ellers"
    if args.poleCells > 1:
        basename += "_pole%d" % args.poleCells
    layout = render(maze, "demos/%s_demo.png" % basename)
    if args.show:
        layout.plt.show()
        
if __name__ == "__main__":
    import argparse

    desc = "Eller's algorithm demonstration"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-r', '--rows', default=20, type=int, \
        help='the numbers of latitudinal rows (default=20)')
    parser.add_argument('-n', '--poleCells', default=1, type=int, \
        help='the numbers of pole rows (default=1)')
    parser.add_argument('-s', '--splitAt', default=1, type=int, \
        help='the split length (arc length, default=1)')
    parser.add_argument('--show', action='store_true',
        help='display the figure before exiting')
    parser.add_argument('--bias1', type=int, default=0.5, \
        help='row merge probability (default=0.5)')
    parser.add_argument('--bias2', type=int, default=0.5, \
        help='column merge probability (default=0.5)')
    args = parser.parse_args()
    main(args)

# END: ellers_demo.py
