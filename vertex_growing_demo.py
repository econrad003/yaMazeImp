#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# vertex_growing_demo.py - demonstrate growing tree algorithms based on
#     a modification of Prim's algorithm which uses vertes-weighted
#     graphs
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
vertex_growing_demo.py - demonstrate growing tree algorithms for
    vertex-weighted graphs
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import vertexwise_growing_tree as vgt
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
    
def generate_Simple_Prim(grid, start):
    """use simple vertexwise Prim's algorithm"""
    from prims import Prims

    print("Create maze using the simplified Prim's algorithm...")
    vgt.Vertex_Prims.on(grid, start=start, debug=True)
    
def generate_growing_tree(grid, start, state):
    """generate maze using edgewise growing tree"""

    print("Create maze using the cellwise growing tree algorithm...")
    vgt.Vertex_Prims.on(grid, state=state, start=start, debug=True)

def tweak(fig, axs):
    """a tweaking function to modify the plots"""
    titles = [["Truest\nPrim", "Simple\nPrim", "Untrue\nPrim",
        "FIFO State\nPrim"], ["LIFO State\nPrim", "LIFO Queue\nPrim",
        "RIFO Queue\nPrim", "FIFO Queue\nPrim"]]
    suptitle = "Vertexwise Growing Tree Algorithms"
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
    print("Vertex Growing Tree Algorithm Test Script...")
    print("Generate maze #1 (Truest [Edgwise] Prim)")
    maze1 = make_weave_grid(21, 21)
    generate_Prim(maze1, start=maze1[10, 10])

    print("Generate maze #2 (Simple Prim)")
    maze2 = make_weave_grid(21, 21)
    generate_Simple_Prim(maze2, start=maze1[10, 10])

    print("Generate maze #3 (Untrue [Vertexwise] Prim)")
    maze3 = make_weave_grid(21, 21)
    state = vgt.Random_Cost_State(maze3)
    generate_growing_tree(maze3, maze3[10, 10], state)

    print("Generate maze #4 (FIFO Cost Prim)")
    maze4 = make_weave_grid(21, 21)
    state = vgt.FIFO_Cost_State(maze4)
    generate_growing_tree(maze4, maze4[10, 10], state)

    print("Generate maze #5 (LIFO Cost Prim)")
    maze5 = make_weave_grid(21, 21)
    state = vgt.LIFO_Cost_State(maze5)
    generate_growing_tree(maze5, maze5[10, 10], state)

    print("Generate maze #6 (LIFO Queue Prim)")
    maze6 = make_weave_grid(21, 21)
    state = vgt.LIFO_Queue_State(maze6)
    generate_growing_tree(maze6, maze6[10, 10], state)

    print("Generate maze #7 (Random Queue Prim)")
    maze7 = make_weave_grid(21, 21)
    state = vgt.RIFO_Queue_State(maze7)
    generate_growing_tree(maze7, maze7[10, 10], state)

    print("Generate maze #8 (FIFO Queue Prim)")
    maze8 = make_weave_grid(21, 21)
    state = vgt.FIFO_Queue_State(maze8)
    generate_growing_tree(maze8, maze8[10, 10], state)

    mazes = [[maze1, maze2, maze3, maze4], [maze5, maze6, maze7, maze8]]
    filename = "demos/growing_tree-vertex-array.png"
    render(mazes, filename)

# END: vertex_growing_demo.py
