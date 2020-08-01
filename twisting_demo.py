#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# twisting_demo.py - demonstrate the twister braiding algorithm
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
straightify_demo.py - demonstrate the twister braiding algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import matplotlib.pyplot as plt
from braiding import Braiding

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
        titles = ["Perfect Maze", "Twistier Maze", "Twistiest Maze"]
        ax = axs[j]
        ax.title.set_text(titles[j])
        ax.set(aspect=1)
        ax.axis('off')
    fig.suptitle("Twisting Demonstration")

def tweak_right(fig, axs):
    """another tweaking function to modify the plots"""
    for j in range(3):
        titles = ["Perfect Maze", "Twistier Maze", "Twistiest Maze"]
        ax = axs[j]
        ax.title.set_text(titles[j])
        ax.set(aspect=1)
        ax.axis('off')
    fig.suptitle("Twisting Right Demonstration")

def tweak_left(fig, axs):
    """yet another tweaking function to modify the plots"""
    for j in range(3):
        titles = ["Perfect Maze", "Twistier Maze", "Twistiest Maze"]
        ax = axs[j]
        ax.title.set_text(titles[j])
        ax.set(aspect=1)
        ax.axis('off')
    fig.suptitle("Twisting Left Demonstration")

def render(maze, filename, p=0.3, tweaker=tweak, turns=None):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, a rectangular grid will be created and a
    perfect mazes will be created from it using the first-entry
    Aldous/Broder algorithm.  Three subplots are produced:

        a) a plot of the given maze
        b) a plot of the maze after single-pass braid-removal by
           twisting with bias 30%
        c) a plot of the maze after a complete straightening pass

    maze = a Grid object with a maze to braid by straightening
    filename = filename or pathname for output
    p = the bias to be used for partial braiding (default 0.3)
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: the number of mazes, a Figure object and array
        of Axes objects
    turns = a dictionary of turns.  The entries have the form
            turns[direction] = [direction1, direction2, ...]
        If turns is None, the default turning dictionary is used. 
    """
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
    n, _, k, q = Braiding.twister(maze, bias = p, turns = turns)
    print("       %d dead ends, %d removed (q=%f)" % (n, k, q * 100))
    ax = axs[1]
    layout = Color_Layout(maze, plt, figure=[fig, ax])
    layout.draw_grid()
    print("   column 2 - first pass, full twisting...")
    n, _, k, q = Braiding.twister(maze)
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
    print("Twisty Braid Maze Script...")
    maze = make_rectangular_grid(30, 20)
    generate_maze(maze)
    filename = "demos/twister-array-both.png"
    render(maze, filename)

    maze = make_rectangular_grid(30, 20)
    generate_maze(maze)
    filename = "demos/twister-array-right.png"
    render(maze, filename, turns = Braiding.right_turns(), \
        tweaker = tweak_right)

    maze = make_rectangular_grid(30, 20)
    generate_maze(maze)
    filename = "demos/twister-array-left.png"
    render(maze, filename, turns = Braiding.left_turns(), \
        tweaker = tweak_left)

# END: twisting_demo.py
