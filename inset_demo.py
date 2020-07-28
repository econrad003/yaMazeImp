#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# inset_demo.py - demonstrate inset
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
#     27 July 2020 - Initial version
##############################################################################
"""
inset_demo.py - demonstrate rectangular grid with inset
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import matplotlib.pyplot as plt
from rectangular_grid import Rectangular_Grid
from recursive_backtracker import Recursive_Backtracker as DFS
from layout_plot_color import Color_Layout

def main(m, n, inset):
    """create an inset maze"""
    print("create grid: Rectangular_Grid(%d, %d, inset=%f)" % (m, n, inset))
    grid = Rectangular_Grid(m, n, inset=inset)
    print("Create perfect maze using randomized DFS...")
    DFS.on(grid)
    layout = Color_Layout(grid, plt, title="Inset Maze Demonstration")
    print("Creating color palette...")
    layout.palette[0] = 'violet'
    layout.palette[1] = 'powderblue'
    layout.palette[2] = 'red'
    layout.palette[3] = 'green'
    for i in range(m):
        for j in range(n):
            layout.color[grid[i, j]] = (i+j)%2
    layout.color[grid[0, 0]] = 2
    layout.color[grid[m-1, n-1]] = 3

    print("Plotting...")
    layout.draw_grid()
    layout.render("demos/inset_demo.png")
    # plt.show()

if __name__ == "__main__":
    main(15, 20, 0.15)

# END: inset_demo.py
