#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# braid_demo.py - demonstrate the braiding algorithm
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
braid_demo.py - demonstrate the braiding algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

def make_rectangular_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from rectangular_grid import Rectangular_Grid

    print("Grid: Rectangular_Grid(%d, %d)" % (m, n))
    grid = Rectangular_Grid(m, n)
    return grid
    
def make_polar_grid(m, n=1, w=1.0):
    """create a rectangular grid
    
    Arguments:
        m - the number of latitudinal circles
        n - the number of central cells
        w - the target outer width of a non-central cell"""
    from polar_grid import Polar_Grid

    print("Grid: Polar_Grid(%d, poleCells=%d, splitAt=%f)" % (m, n, w))
    grid = Polar_Grid(m, poleCells=n, splitAt=w)
    return grid

def generate_maze(grid):
    """generate a perfect maze on the grid"""
    from recursive_backtracker import Recursive_Backtracker as DFS

    print("Generate perfect maze... (recursive backtracker [aka DFS])")
    DFS.on(grid)
    print("Done!")

def tweak(rows, fig, axs):
    """a tweaking function to modify the plots"""
    for i in range(rows):
        titles = ["Maze", "Partial Braid", "Full Braid"]
        for j in range(3):
            ax = axs[i, j]
            ax.title.set_text(titles[j])
            ax.set(aspect=1)
            ax.axis('off')
    fig.suptitle("Braiding Demonstration")

def render(mazes, filename, p=0.5, tweaker=tweak):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, two grids will be created, one rectangular
    and one polar, and perfect mazes will be created from them using the
    depth-first search algorithm (commonly known as recursive
    backtracker).  For each given maze, three subplots are produced:

        a) a plot of the given maze
        b) a plot of the maze after partial braiding
        c) a plot of the maze after braiding is complete

    The mazes list consists of pairs, a Grid object containing the
    given maze, and a Layout object to be used for plotting.

    mazes = a list of pairs, with each pair consisting of a Grid object
        and a Layout class to be used for plotting
    filename = filename or pathname for output
    p = the bias to be used for partial braiding (default 0.5)
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: the number of mazes, a Figure object and array
        of Axes objects"""
    import matplotlib.pyplot as plt

        # create a subplot array
    rows = len(mazes)
    fig, axs = plt.subplots(rows, 3)
    tweaker(rows, fig, axs)

        # generate the plots
    for i in range(rows):
        print("Plotting row %d..." % i)
        print("   column 0 - given maze...")
        maze, LayoutClass = mazes[i]
        ax = axs[i, 0]
        layout = LayoutClass(maze, plt, figure=[fig, ax])
        layout.draw_grid()
        print("   column 1 - %f %% braid..." % (p * 100))
        maze.braid(bias=p)
        ax = axs[i, 1]
        layout = LayoutClass(maze, plt, figure=[fig, ax])
        layout.draw_grid()
        print("   column 1 - full braid...")
        maze.braid()
        ax = axs[i, 2]
        layout = LayoutClass(maze, plt, figure=[fig, ax])
        layout.draw_grid()

    print("Saved to " + filename)
    plt.subplots_adjust(hspace=.001, wspace=.001)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(filename, bbox_inches='tight', pad_inched=0.0)
    # plt.show()

if __name__ == "__main__":
    from layout_plot_color import Color_Layout
    from layout_plot_polar import Polar_Layout

    print("Braid Maze Test Script...")
    print("Generate maze #1")
    maze1 = make_rectangular_grid(20, 20)
    generate_maze(maze1)

    print("Generate maze #2")
    maze2 = make_polar_grid(10, 3)
    generate_maze(maze2)

    mazes = [[maze1, Color_Layout], [maze2, Polar_Layout]]
    filename = "demos/braid-array.png"
    render(mazes, filename)

# END: braid_demo.py
