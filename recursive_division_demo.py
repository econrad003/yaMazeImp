#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# recursive_division_demo.py - demonstrate the recursive division algorithm
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
#     13 Aug 2020 - Initial version
##############################################################################
"""
recursive_division_demo.py - demonstrate recursive division
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import matplotlib.pyplot as plt
import recursive_division as rd
from recursive_division import Recursive_Division
from aldous_broder import Aldous_Broder
from layout_plot_color import Color_Layout

def make_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from rectangular_grid import Rectangular_Grid

    print("Grid: Rectangular_Grid(%d, %d)" % (m, n))
    grid = Rectangular_Grid(m, n, inset=0.15)
    return grid

def generate_maze(grid, state=None, **kwargs):
    """generate a perfect maze on the grid"""

    print("Generate perfect maze using recursive division")
    Recursive_Division.on(grid, state, **kwargs)
    print("Done!")

def render(maze, filename, title, debug=False):
    """render a mazes
    
    This is the main entry point to this script.  If the script is run
    from the command line, the maze will be created using recursive
    division algorithm.

    filename = filename or pathname for output
    title = a title for the printout
    """

        # generate the plots
    print("Plotting...\n%s" % title)
    layout = Color_Layout(maze, plt, title=title)
    layout.ax.set(aspect=1)
    layout.ax.axis('off')
    layout.palette[0] = "yellow"
    layout.palette[1] = "brown"
    for cell in maze.each():
        layout.color[cell] = 1 if "underCell" in cell.kwargs else 0
    layout.draw_grid()
    layout.render(filename)
    if debug:
        layout.plt.show()

if __name__ == "__main__":
    print("Recursive Division Test Script...")
        # test 1
    maze = make_grid(30, 40)
    generate_maze(maze)
    filename = "demos/recursive_division_demo1.png"
    render(maze, filename, \
        "Recursive Division\n(default state matrix)")

        # test 2
    maze = make_grid(30, 40)
    state = rd.Golden_State(maze)
    generate_maze(maze, state)
    filename = "demos/recursive_division_demo2.png"
    render(maze, filename, \
        "Recursive Division\n(Fibonaccian state matrix)")

        # test 3
    maze = make_grid(30, 40)
    state = Recursive_Division.State(maze, delta=5)
    generate_maze(maze, state)
    filename = "demos/recursive_division_demo3.png"
    render(maze, filename, \
        "Recursive Division\n(delta=5)")

        # test 4
    maze = make_grid(30, 40)
    state = Recursive_Division.State(maze, delta=5, \
        algorithm=Aldous_Broder)
    generate_maze(maze, state)
    filename = "demos/recursive_division_demo4.png"
    render(maze, filename, \
        "Recursive Division\n(delta=5, Aldous/Broder)")

# END: recursive_division_demo.py
