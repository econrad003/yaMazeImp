#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################
# binary_tree_demo.py - test the binary tree implementation
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
#######################################################################
# Maintenance History:
#     21 Apr 2020 - Initial version
#     2 May 2020 - Rewrite using GraphViz/dot layout engine
#     3 May 2020 - Cleanup with pylint
#######################################################################
"""
binary_tree_demo.py - binary tree testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck. Mazes for Programmers. 2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

To do:
    Check other combinations besides the forward=eastward and
    upward=west.
"""

    # pylint: disable=redefined-outer-name
    #     reason: grid, m and n are standard names for these variables

from rectangular_grid import Rectangular_Grid
from binary_tree import Binary_Tree
from layout_graphviz import Layout
from helpers import Helper

def make_maze(m, n, maze_name, wallbuilder):
    """create a maze"""
    if wallbuilder:                       # wall-builder algorithm
        grid = Rectangular_Grid(m, n, name=maze_name, wallAdder=True)
        Binary_Tree.wallBuilder_on(grid)
    else:                                 # passage-carver algorithm
        grid = Rectangular_Grid(m, n, name=maze_name)
        Binary_Tree.on(grid)
    return grid

def display_unicode(grid):
    """display a small maze in the terminal using unicode"""
    source = grid[m-1, n-1]               # start cell
    terminus = grid[0, 0]                 # finish cell
    source.kwargs["content"] = "S"
    terminus.kwargs["content"] = "T"
    print(grid.unicode())

def display_tree(grid, pathname):
    """display the maze as a tree using dot"""
    dot = Layout(grid, filename=pathname)
    dot.draw()
    dot.render()                          # rooted tree

def display_maze(grid, pathname):
    """display the maze preserving its rectangular geometry"""
    source = grid[m-1, n-1]               # start cell
    terminus = grid[0, 0]                 # finish cell
    dot = Layout(grid, engine='fdp', filename=pathname)
    dot.set_square_cells()
    dot.set_cell(source, label='Start')
    dot.set_cell(terminus, label='End')
    dot.draw()
    dot.render()                          # rectangular maze

def check_maze(grid):
    """check that the maze is perfect

    We want the maze to be a spanning tree of the grid.  If v is the
    number of vertices, e the number of edges, and k the number of
    components, we want to satisfy both the following conditions:
        (1) k = 1 (the maze is connected)
        (2) v = e + 1 (every edge is a bridge, given k=1)
    Since edges are counted in the manner of Euler, we count each edge
    twice.

    Note: Loops are not counted here with multiplicity, but the
    assertion will fail (as it should) if any loops occur.
    """
    m, n = grid.rows, grid.cols
    v = m * n                             # number of vertices
    e = 0                                 # number of arcs (2e)
    for cell in grid.each():
        e += len(cell.arcs)                   # Euler counting
    k, _ = Helper.find_components(grid)
        # note: e is twice the number of edges
    assert e + 2 == 2 * v and k == 1, \
        "v=%d, 2*e=%d, k=%d - not a tree" % (v, e, k)

WALLBUILDER = True
PASSAGECARVER = False

m, n = 5, 7                           # small rectangular mazes
    # Passage carver / Small Maze

print("1. Binary Tree - passage carver - small maze")
grid = make_maze(m, n, "BinaryTree1", PASSAGECARVER)
display_unicode(grid)
display_tree(grid, 'demos/BinaryTree_tree.gv')
display_maze(grid, 'demos/BinaryTree_maze1.gv')
check_maze(grid)

    # Wall builder / Small Maze

print("2. Binary Tree - wall builder - small maze")
grid = make_maze(m, n, "BinaryTree2", WALLBUILDER)
display_unicode(grid)
check_maze(grid)

m, n = 30, 20                         # large rectangular mazes
    # Passage carver / Large Maze

print("3. Binary Tree - passage carver - large maze")
grid = make_maze(m, n, "BinaryTree3", PASSAGECARVER)
display_maze(grid, 'demos/BinaryTree_maze2.gv')
check_maze(grid)

    # Wall builder / Large Maze

print("4. Binary Tree - wall builder - small maze")
grid = make_maze(m, n, "BinaryTree4", WALLBUILDER)
display_maze(grid, 'demos/BinaryTree_maze3.gv')
check_maze(grid)

# END: binary_tree_demo.py
