#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# edge_growing_demo.py - demonstrate growing tree algorithms including
#   Prim's algorithm
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
#     9 Aug 2020 - Initial version
##############################################################################
"""
edge_growing_demo.py - demonstrate growing tree algorithms
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

These are a collection of algorithms based on Prim's minimal-weight
spanning tree algorithm. 

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import edgewise_growing_tree as egt
from layout_plot_color import Color_Layout

def make_weave_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Weave_Grid

    print("Grid: Weave_Grid(%d, %d)" % (m, n))
    grid = Weave_Grid(m, n)
    return grid

def make_preweave_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Preweave_Grid

    print("Grid: Preweave_Grid(%d, %d)" % (m, n))
    grid = Preweave_Grid(m, n)
    return grid

def generate_Prim(grid, start):
    """use pure edgewise Prim's algorithm"""
    from prims import Prims

    print("Create maze using Prim's algorithm...")
    Prims.on(grid, start=start, debug=True)
    
def generate_Kruskal1(grid):
    """use Kruskal's algorithm"""
    from kruskals import Kruskals

    print("Create maze using Kruskal's algorithm without preweave...")
    Kruskals.on(grid)
    print("Done!")

def generate_Kruskal2(grid):
    """use Kruskal's algorithm with preweave"""
    from kruskals import Kruskals

    print("Create maze using Kruskal's algorithm with preweave...")
    state = Kruskals.State(grid)
    added = state.add_random_weaves()
    density = added / (grid.rows * grid.cols)
    print("%d weaves added (weave density = %f)" % (added, density))
    Kruskals.on(grid, state=state)
    print("Done!")

def generate_growing_tree(grid, start, state):
    """generate maze using edgewise growing tree"""

    print("Create maze using the edgewise growing tree algorithm...")
    egt.Edge_Growing_Tree.on(grid, state, start=start, debug=True)
    

def tweak(fig, axs):
    """a tweaking function to modify the plots"""
    titles = [["Pure Prim", "Kruskal", "Kruskal\n(preweave)", "Mixed"], \
        ["LIFO", "FIFO", "MIFO", "RIFO"]]
    suptitle = "Prim's Algorithm and Its Relatives"
    for i in range(2):
        for j in range(4):
            ax = axs[i][j]
            ax.title.set_text(titles[i][j])
            ax.set(aspect=1)
            ax.axis('off')
    fig.suptitle(suptitle)

def render(mazes, filename, tweaker=tweak):
    """render a set of mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, eight rectangular weave grids will be
    created, and perfect mazes will be created from them using various 
    growing tree algorithms.

    mazes = a (2,4) matrix of mazes.
    filename = filename or pathname for output.
    tweaker = the tweaking routine (default tweak).  This function takes
        two parameters: a Figure object and a 2x4 matrix of Axes
        objects.
    """

    mpl.rcParams['lines.linewidth'] = 0.5

        # create a subplot array
    fig, axs = plt.subplots(2, 4)
    tweaker(fig, axs)

        # generate the plots
    for i in range(2):
        for j in range(4):
            print("   plotting maze %d..." % (4*i + j + 1))
            maze = mazes[i][j]
            ax = axs[i][j]
            layout = Color_Layout(maze, plt, figure=[fig, ax])
            layout.palette[0] = "yellow"
            layout.palette[1] = "green"
            for cell in maze.each():
                layout.color[cell] = 1 if "underCell" in cell.kwargs \
                    else 0
            layout.draw_grid()

    print("Saved to " + filename)
    plt.subplots_adjust(hspace=.001, wspace=.001)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(filename, bbox_inches='tight', pad_inched=0.0, dpi=300)
    plt.show()

if __name__ == "__main__":
    print("Prim's Algorithm Test Script...")
    print("Generate maze #1")
    maze1 = make_weave_grid(21, 21)
    generate_Prim(maze1, start=maze1[10, 10])

    print("Generate maze #2")
    maze2 = make_weave_grid(21, 21)
    generate_Kruskal1(maze2)

    print("Generate maze #3")
    maze3 = make_preweave_grid(21, 21)
    generate_Kruskal2(maze3)

    print("Generate maze #4")
    maze4 = make_weave_grid(21, 21)
    print("   mixed state matrix")
    state = egt.Mixed_State(maze4)
    generate_growing_tree(maze4, maze4[10, 10], state)

    print("Generate maze #5")
    maze5 = make_weave_grid(21, 21)
    print("   LIFO state matrix")
    state = egt.LIFO_State(maze5)
    generate_growing_tree(maze5, maze5[10, 10], state)

    print("Generate maze #6")
    maze6 = make_weave_grid(21, 21)
    print("   FIFO state matrix")
    state = egt.FIFO_State(maze6)
    generate_growing_tree(maze6, maze6[10, 10], state)

    print("Generate maze #7")
    maze7 = make_weave_grid(21, 21)
    print("   MIFO state matrix")
    state = egt.MIFO_State(maze7)
    generate_growing_tree(maze7, maze7[10, 10], state)

    print("Generate maze #8")
    maze8 = make_weave_grid(21, 21)
    print("   RIFO state matrix")
    state = egt.RIFO_State(maze8)
    generate_growing_tree(maze8, maze8[10, 10], state)

    mazes = [[maze1, maze2, maze3, maze4], [maze5, maze6, maze7, maze8]]
    filename = "demos/growing_tree-array.png"
    render(mazes, filename)

# END: edge_growing_demo.py
