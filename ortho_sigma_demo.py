#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# ortho_sigma_demo.py - test the rectangular sigma maze implementation
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
#     30 May 2020 - Initial version
##############################################################################
"""
ortho_sigma_demo.py - rectangular sigma maze testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from ortho_sigma_grid import Ortho_Sigma_Grid
from recursive_backtracker import Recursive_Backtracker

desc = 'Create a maze by applying DFS to a rectangular sigma grid.'

def render_plot(grid, pathname):
    """render the maze using matplotlib"""
    import matplotlib.pyplot as plt
    from layout_plot_polygon import Polygonal_Layout
    layout = Polygonal_Layout(grid, plt, title='Rectangular Sigma Grid')

    m, n = grid.rows, grid.cols
    layout.set_palette_color(1, 'red')
    layout.set_palette_color(2, 'green')
    cell1 = grid[0, n-1]
    layout.set_color(cell1, 1)
    cell2 = grid[m-1, 0]
    layout.set_color(cell2, 2)
    layout.ax.set(aspect=1)

    plt.axis('off')
    layout.draw_grid()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    layout.render(pathname, tight=True)

def main(args):
    m, n = args.dim
    print("Grid: m=%d, n=%d, v=%d" % (m, n, m*n))
    grid = Ortho_Sigma_Grid(m, n)
    Recursive_Backtracker.on(grid)
    render_plot(grid, args.output)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--dim', default=[41, 21], type=int, nargs=2,
                        help='grid square dimensions (default: [41,21])')
    parser.add_argument('-o', '--output', default='demos/ortho_sigma_demo.png',
                        help='mask file (default: demos/ortho_sigma_demo.png)')
    args = parser.parse_args()
    main(args)

# END: ortho_sigma_demo.py
