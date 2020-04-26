#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
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
#
# Maintenance History:
#     21 Apr 2020 - Initial version
"""
binary_tree_demo.py - binary tree testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from rectangular_grid import Rectangular_Grid
from binary_tree import Binary_Tree

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

def test(grid):
    """run a battery of tests"""
    from statistics import Maze_Statistics
    from helpers import Helper

    stats = Maze_Statistics(grid)
    v = stats.size()
    p, w, e = stats.Euler_edge_counts()
    k, _ = Helper.find_components(grid)
    print("%s: %d cells, %d passages, %d walls, %d edges, %d components" \
        % (stats.name, v, p//2, w//2, e//2, k))
    degseq = stats.degree_counts()
    print("  Degree sequence: " + sorted_degrees(degseq))

    assert v is 35, "Vertex count error (got %s, expected v=5x7=35)" % v
    assert p is 68, "Passage count error (got %s, expected p=v-1=34)" % (p//2)
    assert e is 116, "Edge count error (got %s, expected e=58)" % (e//2)
    assert w is 48, "Wall count error (got %s, expected w=e-p=24)" % (w//2)
    assert k is 1, "Component count error (got %s, expected k=1)" % k

    # PASSAGE CARVER

grid = Rectangular_Grid(5, 7, name="PassageCarver")
Binary_Tree.on(grid)
grid[4,6].kwargs["content"] = "S"
grid[0,0].kwargs["content"] = "T"
print(grid.unicode())
test(grid)

    # WALL BUILDER

grid = Rectangular_Grid(5, 7, wallAdder=True, name="WallBuilder")
Binary_Tree.wallBuilder_on(grid, forward="south", upward="west")
grid[0,0].kwargs["content"] = "S"
grid[4,6].kwargs["content"] = "T"
print(grid.unicode())
test(grid)

# END: binary_tree_demo.py
