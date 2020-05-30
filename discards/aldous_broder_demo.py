#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# aldous_broder_demo.py - test the Aldous/Broder maze algorithms
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
#     2 May 2020 - Initial version
##############################################################################
"""
aldous_broder_demo.py - test the Aldous/Broder algorithms implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

    # pylint: disable=redefined-outer-name
    #     reason: grid, m and n are standard names for these variables

from rectangular_grid import Rectangular_Grid
from aldous_broder import Aldous_Broder
from layout_graphviz import Layout
from helpers import Helper

def make_maze(m, n, maze_name, reverse):
    """create a maze"""
    grid = Rectangular_Grid(m, n, name=maze_name)
    if reverse:                           # last-exit algorithm
        Aldous_Broder.reverse_on(grid)
    else:                                 # first-entrance algorithm
        Aldous_Broder.on(grid)
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

FORWARD_AB = False
REVERSE_AB = True

m, n = 5, 7                           # small rectangular mazes
    # First Entrance / Passage carver / Small Maze

print("1. Aldous/Broder - first entrance algorithm - small maze")
grid = make_maze(m, n, "AldousBroder1", FORWARD_AB)
display_unicode(grid)
display_tree(grid, 'demos/Aldous-Broder_tree.gv')
display_maze(grid, 'demos/Aldous-Broder_maze1.gv')
check_maze(grid)

    # Last Ext / Passage carver / Small Maze

print("2. reverse Aldous/Broder - last exit algorithm - small maze")
grid = make_maze(m, n, "AldousBroderRev1", REVERSE_AB)
display_unicode(grid)
display_tree(grid, 'demos/Aldous-Broder_rev_tree.gv')
display_maze(grid, 'demos/Aldous-Broder_rev_maze1.gv')
check_maze(grid)

m, n = 30, 20                         # large rectangular mazes
    # First Entrance / Passage carver / Large Maze

print("3. Aldous/Broder - first entrance algorithm - larger maze")
grid = make_maze(m, n, "AldousBroder2", FORWARD_AB)
display_maze(grid, 'demos/Aldous-Broder_maze2.gv')
check_maze(grid)

    # Last Ext / Passage carver / Large Maze

print("4. reverse Aldous/Broder - last exit algorithm - larger maze")
grid = make_maze(m, n, "AldousBroderRev2", REVERSE_AB)
display_maze(grid, 'demos/Aldous-Broder_rev_maze2.gv')
check_maze(grid)

# END: aldous_broder_demo.py
