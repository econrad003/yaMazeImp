#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# Moebius_demo.py - test the Moebius strip maze implementation
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
#     24 Apr 2020 - EC - Initial version (adapted from cylinder_demo.py)
# Credits:
#     EC - Eric Conrad
##############################################################################
"""
Moebius_demo.py - Moebius maze testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from moebius_grid import Moebius_Grid
from moebius_grid import Binary_Tree_Moebius as Binary_Tree
from moebius_grid import Sidewinder_Moebius as Sidewinder
from statistics import Maze_Statistics
from helpers import Helper

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

def init(name, complete, rows=5):
    """Label west and east ends for gluing"""
    assert rows in [5, 6]
    majescules = ['A', 'B', 'C', 'D', 'E', 'F']
    miniscules = ['a', 'b', 'c', 'd', 'e', 'f']
    if rows is 5:
        majescules.pop()
        miniscules.pop()
    grid = Moebius_Grid(rows, 7, wallAdder=complete, name=name)
    for i in range(rows):
        grid[i,7].kwargs["content"] = miniscules[i]
        grid[i,6].kwargs["content"] = majescules[i]
    return grid

def tests(grid):
    print(grid.unicode())

    stats = Maze_Statistics(grid)
    v = stats.size()
    p, w, e = stats.Euler_edge_counts()
    
    k, _ = Helper.find_components(grid)
    print("%s: %d cells" % (stats.name, v) + \
        ", %d passages, %d walls, %d edges" % (p//2, w//2, e//2) + \
        ", %d maze components" % k)
    degseq = stats.degree_counts()
    print("  Degree sequence: " + sorted_degrees(degseq))
    
        # The maze is a tree if and only if both of the following
        # are true:
        #   (a) the maze is passage-connected, and
        #   (b) the number of passages is one less than the number
        #       of cells.

    assert v is 35, "Vertex count error (got %s, expected v=5x7=35)" % v
    assert p is 68, "Passage count error (got %s, expected p=v-1=34)" % (p//2)
    assert e is 126, "Edge count error (got %s, expected e=63)" % (e//2)
    assert w is 58, "Wall count error (got %s, expected w=e-p=29)" % (w//2)
    assert k is 1, "The maze is disconnected (got k=%d, expected k=1)" % k

    # BINARY TREE ALGORITHM

grid = init("BinaryTree-E/N", True)
Binary_Tree.on(grid)
tests(grid)

#grid = init("BinaryTree-N/E", True)
#Binary_Tree.on(grid, forward="north")
#tests(grid)

#grid = init("Sidewinder-E/N", True)
#Sidewinder.on(grid)
#tests(grid)

#grid = init("Sidewinder-N/E", True)
#Sidewinder.on(grid, forward="north")
#tests(grid)
