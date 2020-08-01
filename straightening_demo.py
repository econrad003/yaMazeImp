#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# straightening_demo.py - demonstrate the straightener braiding algorithm
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
#     30 Jul 2020 - Initial version
##############################################################################
"""
straightify_demo.py - demonstrate the straightener braiding algorithm
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
    grid = Rectangular_Grid(m, n, inset=0.15)
    return grid
    
def generate_maze(grid):
    """generate a perfect maze on the grid"""
    from aldous_broder import Aldous_Broder

    print("Generate perfect maze... (Aldous/Broder)")
    Aldous_Broder.on(grid)
    print("Done!")

def tweak(fig, axs):
    """a tweaking function to modify the plots"""
    for j in range(3):
        titles = ["Perfect Maze", "Straighter Maze", "Straightest Maze"]
        ax = axs[j]
        ax.title.set_text(titles[j])
        ax.set(aspect=1)
        ax.axis('off')
    fig.suptitle("Straightening Demonstration")

def render(maze, filename, p=0.5, tweaker=tweak):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, a rectangular grid will be created and a
    perfect mazes will be created from it using the first-entry
    Aldous/Broder algorithm.  Three subplots are produced:

        a) a plot of the given maze
        b) a plot of the maze after single-pass braid-removal by
           straightening with bias 50%
        c) a plot of the maze after a complete straightening pass

    maze = a Grid object with a maze to braid by straightening
    filename = filename or pathname for output
    p = the bias to be used for partial braiding (default 0.5)
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: the number of mazes, a Figure object and array
        of Axes objects"""
    import matplotlib.pyplot as plt
    from braiding import Braiding
    from layout_plot_color import Color_Layout

        # create a subplot array
    fig, axs = plt.subplots(1, 3)
    tweaker(fig, axs)

        # generate the plots
    print("Plotting...")
    print("   column 0 - given maze...")
    ax = axs[0]
    layout = Color_Layout(maze, plt, figure=[fig, ax])
    layout.draw_grid()
    print("   column 1 - first pass, bias p=%f..." % (p * 100))
    n, _, k, q = Braiding.straightener(maze, bias = p)
    print("       %d dead ends, %d removed (q=%f)" % (n, k, q * 100))
    ax = axs[1]
    layout = Color_Layout(maze, plt, figure=[fig, ax])
    layout.draw_grid()
    print("   column 2 - first pass, full straightening...")
    n, _, k, q = Braiding.straightener(maze)
    print("       %d dead ends, %d removed (q=%f)" % (n, k, q * 100))
    ax = axs[2]
    layout = Color_Layout(maze, plt, figure=[fig, ax])
    layout.draw_grid()

    print("Saved to " + filename)
    plt.subplots_adjust(hspace=.001, wspace=.001)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(filename, bbox_inches='tight', pad_inched=0.0)
    # plt.show()

if __name__ == "__main__":
    print("Straight Braid Maze Script...")
    maze = make_rectangular_grid(30, 20)
    generate_maze(maze)
    filename = "demos/straightening-array.png"
    render(maze, filename)

# END: straightening_demo.py
