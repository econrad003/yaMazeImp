#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# mask_demo.py - test the masked maze implementation
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
#     27 May 2020 - Initial version
##############################################################################
"""
mask_demo.py - masked maze testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from masked_grid import make_mask
from aldous_broder import Aldous_Broder

desc = 'Create a maze by applying Aldous/Broder to a masked grid.'

def render_plot(grid, masked, pathname):
    """render the maze using matplotlib"""
    import matplotlib.pyplot as plt
    from layout_plot_color import Color_Layout

    layout = Color_Layout(grid, plt, title='Masked Grid')
    layout.set_palette_color(1, 'red')
    for cell in grid.each():
        if not masked.is_enabled(cell):
            layout.set_color(cell, 1)
    layout.ax.set(aspect=1)
    plt.axis('off')
    layout.draw_grid()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    layout.render(pathname, tight=True)

def main(args):
    grid, masked = make_mask(args.input, debug=True)
    m, n = grid.rows, grid.cols
    print("Grid: m=%d, n=%d, v=%d" % (m, n, m*n))
    Aldous_Broder.on(masked)
    render_plot(grid, masked, args.output)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-i', '--input', default='input/simple_mask.txt',
                        help='mask file (default: input/simple_mask.txt)')
    parser.add_argument('-o', '--output', default='demos/mask_demo.png',
                        help='mask file (default: demos/mask_demo.png)')
    args = parser.parse_args()
    main(args)

# END: mask_demo.py
