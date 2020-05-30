#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# layout_plot_demo.py - test the maze render implementation (using matplotlib)
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

import matplotlib.pyplot as plt

from rectangular_grid import Rectangular_Grid
from binary_tree import Binary_Tree
from norms import distances
from layout_plot import Layout

# set to true to test with a small example
DEBUG = False

m, n = (20, 30) if not DEBUG else (5, 7)
grid = Rectangular_Grid(m, n, name="BinaryTree1")
Binary_Tree.on(grid)
if DEBUG:
    print(grid.unicode())

layout = Layout(grid, plt, title="Binary Tree")
layout.draw_grid()
layout.render("plots/layout_demo.png")

plt.show()

# END: layout_plot_demo.py
