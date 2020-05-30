#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# layout_demo.py - test the maze render implementation (using GraphViz/dot)
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
#     1 May 2020 - Initial version
"""
layout_demo.py - plotter testing (GraphViz/dot)
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from rectangular_grid import Rectangular_Grid
from binary_tree import Binary_Tree
from norms import distances
from layout_graphviz import Layout


    # PASSAGE CARVER

m=5
n=7
grid = Rectangular_Grid(m, n, name="BinaryTree1")
Binary_Tree.on(grid)

source = grid[m-1, n-1]           # start cell
terminus = grid[0, 0]             # finish cell

norms = distances(terminus)
for cell in norms.metrics:
    cell.kwargs["content"] = "%d" % (norms.metrics[cell] % 10)
source.kwargs["content"] = "S"
terminus.kwargs["content"] = "T"

print(grid.unicode())

    # TEST # 1 - RAW LAYOUT

dot = Layout(grid)
dot.draw()
dot.render()

    # TEST # 2 - RECTANGULAR LAYOUT

dot = Layout(grid, engine='fdp', filename='demos/maze1.gv')
dot.set_square_cells()

dmax = 1                          # 1 to avoid divide by 0
for cell in norms.metrics:
    d = norms[cell]
    if d > dmax:
        dmax = d
dmax = float(dmax)
for cell in norms.metrics:
    d = 250 * norms[cell] / dmax
    red = int(d)
    green = int(251 - d)
    blue = 0
    rgb = '#%02x%02x%02x' % (red, green, blue)
    dot.set_cell(cell, style='filled', fillcolor=rgb)

path = norms.path_to_root(source)
for cell in path:
    d = "%d" % norms[cell]
    dot.set_cell(cell, label=d)
    
dot.set_cell(source, label='Start')
dot.set_cell(terminus, label='End')

dot.draw()
dot.render()

# END: layout_demo.py
