#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# plotter_demo.py - test the plotter implementation (using GraphViz/dot)
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
#     30 Apr 2020 - Clean up and add some tests
#         - use names to reference source (start) and terminus (end) cells;
#         - add test #3 to show arrowheads;
#         - add test #4 using larger graph and different algorithm
"""
plotter_demo.py - plotter testing (GraphViz/dot)
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from rectangular_grid import Rectangular_Grid
from binary_tree import Binary_Tree
from sidewinder import Sidewinder
from plotter_graphviz import GraphViz_Plotter as Plot1
from plotter_graphviz import GraphViz_Plotter_Rectangular as Plot2


    # PASSAGE CARVER

m=5
n=7
grid = Rectangular_Grid(m, n, name="BinaryTree1")
Binary_Tree.on(grid)

source = grid[m-1, n-1]           # start cell
terminus = grid[0, 0]             # finish cell

source.kwargs["content"] = "S"
terminus.kwargs["content"] = "T"
print(grid.unicode())


    # 1. tree structure of maze unravelled
    #    (crude but revealing)

pathname = "demos/graphviz1"
print("saving file %s.dot" % pathname)
plot = Plot1(grid, filename=pathname, title="Binary Tree Maze (Unravelled)")
plot.settings[source]["label"] = "Start"
plot.settings[terminus]["label"] = "End"
plot.draw()
plot.close()
plot.show()

    # 2. maze with cell locations placed geometrically
    #    (crude but functional)

pathname = "demos/graphviz2"
print("saving file %s.dot" % pathname)
plot = Plot2(grid, filename=pathname, title="Binary Tree Maze")
plot.settings[source]["label"] = "Start"
plot.settings[terminus]["label"] = "End"
plot.draw()
plot.close()
plot.show()

    # 3. same maze with directed arrows at start and at dead ends
    #     mark dead ends and start vertes with arrows - carefully!
    #     first identify deadends, changing nothing

L = []
for cell in grid.each():
    if len(cell.arcs) is 1:
        print("len(%s) is %d" % (cell.name, len(cell.arcs)))
        for nbr in cell.arcs:
            print("  nbr is %s" % (str(nbr)))
            L.append([cell, nbr])     # outward aec
    #     add source vertex inward arcs
for nbr in source.arcs:
    L.append([nbr, source])
    #     now make the changes
for cell, nbr in L:
    cell.erectWall(nbr, twoWay=False)

pathname = "demos/graphviz3"
print("saving file %s.dot" % pathname)
plot = Plot2(grid, filename=pathname, title="Binary Tree Maze")
plot.settings[source]["label"] = "Start"
plot.settings[terminus]["label"] = "End"
plot.draw()
plot.close()
plot.show()

    # 4. A larger example using the sidewinder algorithm

m=20
n=34
grid = Rectangular_Grid(m, n, name="SidewinderTree1")
Sidewinder.on(grid)

source = grid[m-1, n-1]           # start cell
terminus = grid[0, 0]             # finish cell

pathname = "demos/graphviz4"
print("saving file %s.dot" % pathname)
plot = Plot2(grid, filename=pathname, title="Sidewinder Maze")
plot.settings[source]["label"] = "Start"
plot.settings[terminus]["label"] = "End"
plot.draw()
plot.close()
plot.show()

# END: plotter_demo.py
