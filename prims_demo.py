#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# prims_demo.py - demonstrate Prim's maze generation algorithm
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
#     31 Jul 2020 - Initial version
##############################################################################
"""
prims_demo.py - demonstrate Prim's algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
from prims import Prims
from layout_plot_color import Color_Layout

def make_weave_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Weave_Grid

    print("Grid: Weave_Grid(%d, %d)" % (m, n))
    grid = Weave_Grid(m, n)
    return grid

def generate_maze(grid):
    """generate a perfect maze on the grid"""

    print("Generate perfect maze using Prim's algorithm")
    Prims.on(grid, debug=True)
    print("Done!")

def tweak(fig, ax, title):
    """a tweaking function to modify the plots"""
    ax.set(aspect=1)
    ax.axis('off')
    fig.suptitle(title)

def render(maze, filename, tweaker=tweak, title="Prim's Algorithm"):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, three mazes will be created using Kruskals
    algorithm, namely one rectangular maze, one rectangular weave maze,
    and one polar maze.

    mazes = a list of [maze, layout] pairs
    filename = filename or pathname for output
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: a Figure object, an array of Axes objects, and
        a set of maze titles"""

        # create a subplot array
    fig, ax = plt.subplots(1, 1)
    tweaker(fig, ax, title)

        # generate the plots
    print("Plotting maze...")
    layout = Color_Layout(maze, plt, figure=[fig, ax])
    layout.palette[0] = "yellow"
    layout.palette[1] = "brown"
    for cell in maze.each():
        layout.color[cell] = 1 if "underCell" in cell.kwargs else 0
    layout.draw_grid()

    print("Saved to " + filename)
    layout.render(filename)
    # plt.show()

if __name__ == "__main__":
    print("Prim's Algorithm Test Script...")
    maze = make_weave_grid(30, 40)
    generate_maze(maze)
    filename = "demos/prims_demo.png"
    render(maze, filename)

# END: prims_demo.py
