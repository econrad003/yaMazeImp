#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# kruskals_demo.py - demonstrate Kruskal's maze generation algorithm
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
#     9 Aug 2020 - Documentation corrections
##############################################################################
"""
kruskals_demo.py - demonstrate the Kruskal's algorithm implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
from kruskals import Kruskals
from layout_plot_color import Color_Layout
from layout_plot_polar import Polar_Layout

def make_square_grid(m, n, inset=0.15):
    """create an ordinary rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from rectangular_grid import Rectangular_Grid

    print("Grid: Rectangular_Grid(%d, %d)" % (m, n))
    grid = Rectangular_Grid(m, n, inset=inset)
    return grid
    
def make_weave_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Preweave_Grid

    print("Grid: Preweave_Grid(%d, %d)" % (m, n))
    grid = Preweave_Grid(m, n)
    return grid

def make_polar_grid(m, n=1):
    """create a polar grid
    
    Arguments:
        m - the number of circles of latitude
        n - the number of pole cells"""
    from polar_grid import Polar_Grid

    print("Grid: Polar_Grid(%d, poleCells=%d)" % (m, n))
    grid = Polar_Grid(m, poleCells=n)
    return grid
    
def generate_maze(grid):
    """generate a perfect maze on the grid"""

    print("Generate perfect maze using Kruskal's algorithm")
    Kruskals.on(grid)
    print("Done!")

def generate_weave_maze(grid):
    """generate a perfect weave maze on the grid"""
    from kruskals import Kruskals

    print("Generate perfect maze using Kruskal's algorithm")
    state = Kruskals.State(grid)
    added = state.add_random_weaves()
    density = added / (grid.rows * grid.cols)
    print("%d weaves added (weave density = %f)" % (added, density))
    Kruskals.on(grid, state)
    print("Done!")

def tweak(fig, axs, titles):
    """a tweaking function to modify the plots"""
    for j in range(3):
        ax = axs[j]
        ax.title.set_text(titles[j])
        ax.set(aspect=1)
        ax.axis('off')
    fig.suptitle("Demonstration of Kruskal's algorithm")

titles3 = ["Rectangular", "Weave", "Sigma"]

def render(mazes, filename, tweaker=tweak, titles=titles3):
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
    cols = len(mazes)
    fig, axs = plt.subplots(1, len(mazes))
    tweaker(fig, axs, titles)

        # generate the plots
    for j in range(cols):
        print("   plotting maze %d..." % (j+1))
        maze, LayoutClass = mazes[j]
        ax = axs[j]
        layout = LayoutClass(maze, plt, figure=[fig, ax])
        layout.palette[0] = "yellow"
        layout.palette[1] = "brown"
        for cell in maze.each():
            layout.color[cell] = 1 if "underCell" in cell.kwargs else 0
        layout.draw_grid()

    print("Saved to " + filename)
    plt.subplots_adjust(hspace=.001, wspace=.001)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(filename, bbox_inches='tight', pad_inched=0.0)
    # plt.show()

if __name__ == "__main__":
    print("Kruskal's Algorithm Test Script...")
    print("Generate maze #1")
    maze1 = make_square_grid(30, 15)
    generate_maze(maze1)

    print("Generate maze #2")
    maze2 = make_weave_grid(30, 15)
    generate_weave_maze(maze2)

    print("Generate maze #3")
    maze3 = make_polar_grid(15)
    generate_maze(maze3)

    mazes = [[maze1, Color_Layout], [maze2, Color_Layout], \
        [maze3, Polar_Layout]]
    filename = "demos/kruskals-array.png"
    render(mazes, filename)

# END: kruskals_demo.py
