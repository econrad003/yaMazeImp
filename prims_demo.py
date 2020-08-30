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
#     29 Aug 2020 - (1) Incorporate command line parsing with argparse
#       (2) Correct documentation
#       (3) Add a simple multilevel maze test script
##############################################################################
"""
prims_demo.py - demonstrate Prim's algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Create weave mazes and multilevel weave mazes with Prim's algorithm.

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
from prims import Prims
from layout_plot_color import Color_Layout
from layout_plot_multilevel import Multilevel_Projective_Layout

def make_weave_grid(m, n):
    """create a rectangular weave grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Weave_Grid

    print("Grid: Weave_Grid(%d, %d)" % (m, n))
    grid = Weave_Grid(m, n)
    return grid

def make_multilevel_grid(m, n, levels):
    """create a multilevel rectangular weave maze

    Arguments:
        m, n - the dimensions of the level subgrids
        levels - the number of floors or levels
    """
    from multilevel_grid import Multilevel_Grid

    print("Grid: Multilevel_Grid()")
    grid = Multilevel_Grid()

    floors = ['Ground Floor', 'First Floor', 'Second Floor', \
        'Third Floor', 'Fourth Floor']
    for i in range(levels):
        subgrid = make_weave_grid(m, n)
        subgrid.name = floors[i] if i < len(floors) \
            else 'Floor #' + str(i)
        grid.add_grid(subgrid)
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
    """render a maze
    
    This is an entry point to this script.  If the script is run
    from the command line, a weave maze will be created and carved
    using Prim's algorithm.

    maze = a rectangular or weave maze to be rendered
    filename = filename or pathname for output
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: a Figure object, an Axe objects, and a title
    """

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
    return layout

def render_multilevel(maze, filename, tweaker=tweak):
    """render a maze
    
    This is an entry point to this script.  If the script is run
    from the command line, a multilevel weave maze will be created
    and carved using Prim's algorithm.

    maze = a multilevel maze to be rendered
    filename = filename or pathname for output
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: a Figure object, an Axe objects, and a title
    """

        # create a subplot array
    levels = len(maze.levels)
    fig, axs = plt.subplots(1, levels+1)

        # generate the plots
    print("Plotting maze...")
    ax = axs[levels]
    layout = Multilevel_Projective_Layout(maze, plt, figure=(fig, ax))
    ax.title.set_text("schematic")
    ax.axis("off")

    for level in range(levels):
        subgrid = maze.levels[level]
        ax = axs[level]
        tweaker(fig, ax, subgrid.name)
        sublayout = layout.add_layout_for_grid(subgrid, plt, \
            Color_Layout, figure=(fig, ax))
        sublayout.palette[0] = "yellow"
        sublayout.palette[1] = "brown"
        for cell in maze.each():
            sublayout.color[cell] = 1 if "underCell" in cell.kwargs \
                else 0

    layout.draw_grid()
    print("Saved to " + filename)
    layout.render(filename)
    return layout

def build_corner_stairwells(grid):
    """build stairwells in alternating corners"""
    print("Building stairwells in alternating corners...")
    levels = len(grid.levels)
    for level in range(levels-1):
        subgrid = grid.levels[level]
        m, n = subgrid.rows, subgrid.cols
        downcells = [subgrid[0, 0], subgrid[m-1, n-1]] if level%2 is 0 \
            else [subgrid[0, n-1], subgrid[m-1, 0]]
        grid.add_stairs_upward(level, downcells[0])
        grid.add_stairs_upward(level, downcells[1])

def build_random_stairwell(grid, level):
    """attempt to build a stairwell at a random location"""
    retries = 10
    subgrid = grid.levels[level]
    for i in range(retries):
        downcell = subgrid.choice()
        if downcell["down"] or downcell["up"]:
            continue      # hash collision
        grid.add_stairs_upward(level, downcell)
        return 1          # success
    return 0              # failure

def build_stairwells(grid, n):
    """build n stairwells per level"""
    print("Building %d stairwells per level..." % n)
    levels = len(grid.levels)
    for level in range(levels-1):
        built = 0
        for i in range(n):
            built += build_random_stairwell(grid, level)
        if built < n:
            print(" -- level %d: wanted %d stairwells up, got %d" \
                % (level, n, built))

def main_multilevel(args):
    """entry point for multilevel"""
    print("Prim's Algorithm Test Script (Multilevel)...")
        # create the grid and the floors
    m, n = args.dim
    maze = make_multilevel_grid(m, n, args.levels)

        # create the stairwells
    if args.corners:
        build_corner_stairwells(maze)
    else:
        build_stairwells(maze, args.stairwells)

        # carve the maze
    generate_maze(maze)

        # render the maze
    basename = "prims_multilevel_"
    if args.corners:
        basename += "c_"
    basename += "demo"
    filename = "demos/" + basename + ".png"
    layout = render_multilevel(maze, filename)
    if args.show:
        layout.plt.show()

def main(args):
    """entry point for single level"""
    print("Prim's Algorithm Test Script...")
    m, n = args.dim
    maze = make_weave_grid(m, n)
    generate_maze(maze)
    filename = "demos/prims_demo.png"
    layout = render(maze, filename)
    if args.show:
        layout.plt.show()

if __name__ == "__main__":
    import argparse

    desc = "demonstration of Prim's algorithm"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--dim', metavar=('ROWS', 'COLS'), \
        nargs=2, default=None, type=int, \
        help='the numbers of rows and columns (default [30, 40])')
    parser.add_argument('--show', action='store_true', \
        help='display the figure before exiting')
    parser.add_argument('--multilevel', action='store_true', \
        help='create a multilevel maze with 3 levels' \
        + ' (dimensions are per level with default [20, 10])')
    parser.add_argument('-l', '--levels', default=None, type=int, \
        help='the numbers of levels (default 1 or 3)')
    parser.add_argument('-c', '--corners', action='store_true', \
        help='place stairwells on alternating corners, two per floor')
    parser.add_argument('-s', '--stairwells', default=2, type=int, \
        help='number of stairwells between floors')

        # parse the arguments and smooth out inconsistencies
    args = parser.parse_args()

    if not args.levels:
        args.levels = 3 if args.multilevel else 1

    args.multilevel = args.levels > 1
    if args.corners:
        args.stairwells = 2

    if not args.dim:
        args.dim = [20, 10] if args.multilevel else [30, 40]

        # generate the requested maze
    if args.multilevel:
        main_multilevel(args)
    else:
        main(args)

# END: prims_demo.py
