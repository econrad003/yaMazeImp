#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# high_card_demo.py - test the high-card-wins maze algorithm
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
#     31 Aug 2020 - Initial version
##############################################################################
"""
high_card_demo.py - test the high-card-wins implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import argparse
import matplotlib.pyplot as plt

from rectangular_grid import Rectangular_Grid
from high_card_wins import High_Card_Wins, NAry_Tree_State
from layout_plot import Layout

def render(maze, filename, title):
    """render a maze
    
    This is an entry point to this script.  If the script is run
    from the command line, a weave maze will be created and carved
    using Prim's algorithm.

    maze = a rectangular or weave maze to be rendered
    filename = filename or pathname for output
    title = a title for the plot
    """

        # generate the plots
    print("Plotting maze...")
    layout = Layout(maze, plt, title=title)
    layout.ax.set(aspect=1)
    layout.ax.axis('off')
    layout.draw_grid()
    print("Saved to " + filename)
    layout.render(filename)
    return layout

def make_2D_grid(m, n, maze_name):
    """create a rectangular grid"""
    grid = Rectangular_Grid(m, n, name=maze_name, inset=0.1)
    return grid

def display_unicode(grid):
    """display a small maze in the terminal using unicode"""
    m, n = grid.rows, grid.cols
    source = grid[0, n-1]               # start cell
    terminus = grid[m-1, 0]             # finish cell
    source.kwargs["content"] = "S"
    terminus.kwargs["content"] = "T"
    print(grid.unicode())

def main_simple(args):
    """run the undiluted high-card-wins algorithm

    Note: The end result might not be connected.
    """
    m, n = args.dim
    maze = make_2D_grid(m, n, "High Card Wins")
    High_Card_Wins.on(maze)
    # display_unicode(maze)
    filename = "demos/high_card_demo.png"
    title = "High Card Wins\n(no biasing)"
    layout = render(maze, filename, title)
    layout.draw_grid()
    return layout

def main_binary(args):
    """create a S/E binary tree using High-Card-Wins"""
    m, n = args.dim
    maze = make_2D_grid(m, n, "S/E Binary Tree")
    state = NAry_Tree_State(maze, directions=["south", "east"])
    High_Card_Wins.on(maze, state)
    # display_unicode(maze)
    filename = "demos/high_card_demo-binarySE.png"
    title = "High Card Wins\nBinary Tree (south/east)"
    layout = render(maze, filename, title)
    layout.draw_grid()
    return layout

def main(args):
    """entry point"""
    if not args.binary:
        args.basic = True
    if args.basic:
        main_simple(args)
    if args.binary:
        main_binary(args)
    if args.show:
        plt.show()

if __name__ == "__main__":
    desc = "High-Card-Wins algorithm demonstration"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', metavar=('ROWS', 'COLS'), \
        nargs=2, type=int, default=[10, 15], \
        help='planar dimensions (default [10, 15])')
    parser.add_argument('--basic', action='store_true', \
        help='run the basic high-card-wins algorithm')
    parser.add_argument('--binary', action='store_true', \
        help='use high-card-wins to create a S/E binary tree')
    parser.add_argument('--show', action='store_true', \
        help='show plots before exiting')
    args = parser.parse_args()
    main(args)

# END: high_card_demo.py
