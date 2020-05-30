#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# ortho_delta_demo.py - test the rectangular delta maze implementation
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
#     28 May 2020 - Initial version
##############################################################################
"""
ortho_delta_demo.py - rectangular delta maze testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from ortho_delta_grid import Ortho_Delta_Grid
from recursive_backtracker import Recursive_Backtracker

desc = 'Create a maze by applying DFS to a rectangular delta grid.'

def render_plot(grid, pathname):
    """render the maze using matplotlib"""
    import matplotlib.pyplot as plt
    from layout_plot_polygon import Polygonal_Layout
    layout = Polygonal_Layout(grid, plt, title='Rectangular Delta Grid')

    m, n = grid.rows, grid.cols
    layout.set_palette_color(1, 'red')
    layout.set_palette_color(2, 'green')
    cell1 = grid[0, n-1, 1]
    layout.set_color(cell1, 1)
    cell2 = grid[m-1, 0, 2]
    layout.set_color(cell2, 2)
    layout.ax.set(aspect=1)

    plt.axis('off')
    layout.draw_grid()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    layout.render(pathname, tight=True)

def main(args):
    m, n = args.dim
    print("Grid: m=%d, n=%d, v=%d" % (m, n, m*n*2))
    grid = Ortho_Delta_Grid(m, n)
    print("Grid: Each individual grid square has two cells")
    Recursive_Backtracker.on(grid)
    render_plot(grid, args.output)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', default=[30, 20], type=int, nargs=2,
                        help='grid square dimensions (default: [30,20])')
    parser.add_argument('-o', '--output', default='demos/ortho_delta_demo.png',
                        help='mask file (default: demos/ortho_delta_demo.png)')
    args = parser.parse_args()
    main(args)

# END: ortho_delta_demo.py
