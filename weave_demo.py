#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# weave_demo.py - demonstrate rectangular weave mazes
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
#     29 Jul 2020 - Initial version
##############################################################################
"""
weave_demo.py - demonstrate rectangular weave mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
from recursive_backtracker import Recursive_Backtracker as DFS
from hunt_and_kill import Hunt_and_Kill
from aldous_broder import Aldous_Broder
from layout_plot_color import Color_Layout

def make_weave_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Weave_Grid

    print("Grid: Weave_Grid(%d, %d)" % (m, n))
    grid = Weave_Grid(m, n)
    return grid
    
def generate_maze(grid, algorithm):
    """generate a perfect maze on the grid"""

    print("Generate perfect maze using %s" % algorithm.__name__)
    algorithm.on(grid)
    n = 0
    for cell in grid.each():
        if "underCell" in cell.kwargs:
            n += 1
    m = grid.rows * grid.cols
    print("Number of cells = %d, including %d undercells" % (m, n))
    print("Done!")

def tweak(fig, axs, titles):
    """a tweaking function to modify the plots"""
    for j in range(3):
        ax = axs[j]
        ax.title.set_text(titles[j])
        ax.set(aspect=1)
        ax.axis('off')
    fig.suptitle("Weaving Demonstration")

titles3 = ["DFS", "Hunt and Kill", "Aldous/Broder"]

def render(mazes, filename, tweaker=tweak, titles=titles3):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, three rectangular weave grids will be created,
    and perfect mazes will be created from them using depth-first search,
    hunt and kill, and first-entry Aldous/Broder.  For each given maze, 
    a subplots is produced:

        a) a plot of the given maze
        b) a plot of the maze after partial braiding
        c) a plot of the maze after braiding is complete

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
        maze = mazes[j]
        ax = axs[j]
        layout = Color_Layout(maze, plt, figure=[fig, ax])
        layout.palette[0] = "yellow"
        layout.palette[1] = "green"
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
    print("Weave Maze Test Script...")
    print("Generate maze #1")
    maze1 = make_weave_grid(20, 10)
    generate_maze(maze1, DFS)

    print("Generate maze #2")
    maze2 = make_weave_grid(20, 10)
    generate_maze(maze2, Hunt_and_Kill)

    print("Generate maze #3")
    maze3 = make_weave_grid(20, 10)
    generate_maze(maze3, Aldous_Broder)

    mazes = [maze1, maze2, maze3]
    filename = "demos/weave-array.png"
    render(mazes, filename)

# END: weave_demo.py
