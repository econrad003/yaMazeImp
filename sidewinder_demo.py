#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# sidewinder_tree_demo.py - test the sidewinder spanning tree implementation
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
#
# Maintenance History:
#     22 Apr 2020 - Initial version
"""
sidewinder_demo.py - sidewinder spanning tree testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from rectangular_grid import Rectangular_Grid
from sidewinder import Sidewinder
from statistics import Maze_Statistics

def sorted_degrees(d):
    """format the degree sequence"""
    s = ""
    X = sorted(list(d))
    if not X:
        return s
    for x in X:
        s += "%d -> %d, " % (x, d[x])
    s = s[:-2]
    return s

    # PASSAGE CARVER

grid = Rectangular_Grid(5, 7, name="PassageCarver")
stats = Maze_Statistics(grid)
Sidewinder.on(grid)

v = stats.size()
p, w, e = stats.Euler_edge_counts()
print("%s: %d cells, %d passages, %d walls, %d edges" \
    % (stats.name, v, p//2, w//2, e//2))
degseq = stats.degree_counts()
print("  Degree sequence: " + sorted_degrees(degseq))

grid[4,0].kwargs["content"] = "S"
grid[0,6].kwargs["content"] = "T"
print(grid.unicode())

assert v is 35, "Vertex count error (got %s, expected v=5x7=35)" % v
assert p is 68, "Passage count error (got %s, expected p=v-1=34)" % (p//2)
assert e is 116, "Edge count error (got %s, expected e=58)" % (e//2)
assert w is 48, "Wall count error (got %s, expected w=e-p=24)" % (w//2)

    # WALL BUILDER (forward=southward, upward=westward)
    #
    #     1. Since our ordering is incompatible with both grid.rowcol() and
    #        grid_colrow(), we need to create a generator...
    #     2. We then need to associate the generator with the grid object.
    #     3. Finally we need to alert the Sidewinder class
    #
    #   For (1), we need to be careful the forward direction.  Since the
    #   forward direction is vertical, we process the cells in a column
    #   major fashion (laterally).  And since our forward direction is
    #   downward, we need to traverse each column in reverse order (from 
    #   north to south).
    #
    #   We can pick our columns in any order.
    ###############
    #   Step 0. Create the object
grid = Rectangular_Grid(5, 7, wallAdder=True, name="WallBuilder")
    #   Step 1. Create the generator
def generator1(grid):
    for j in range(grid.cols):                # column major (lateral)
        for i in range(grid.rows-1, -1, -1):      # row minor (southward)
            yield grid[i, j]
    #   Step 2. Inject it into the grid object
each_SW = grid.inject_method(generator1)
    #   Step 3. Alert the Sidewinder class
Sidewinder.GENERATOR = each_SW

stats = Maze_Statistics(grid)
Sidewinder.wallBuilder_on(grid, forward="south", upward="west")

v = stats.size()
p, w, e = stats.Euler_edge_counts()
print("%s: %d cells, %d passages, %d walls, %d edges" \
    % (stats.name, v, p//2, w//2, e//2))
degseq = stats.degree_counts()
print("  Degree sequence: " + sorted_degrees(degseq))

grid[4,0].kwargs["content"] = "S"
grid[0,6].kwargs["content"] = "T"
print(grid.unicode())

assert v is 35, "Vertex count error (got %s, expected v=5x7=35)" % v
assert p is 68, "Passage count error (got %s, expected p=v-1=34)" % (p//2)
assert e is 116, "Edge count error (got %s, expected e=58)" % (e//2)
assert w is 48, "Wall count error (got %s, expected w=e-p=24)" % (w//2)

# END: sidewinder_demo.py
