#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# polar_demo.py - test the polar maze and polar layout implementations
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
#     15 Jul 2020 - Initial version
#     25 Jul 2020 - Add titles to the plots
##############################################################################
"""
inwinder_demo.py - inwinder algorithm testing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
from inwinder import Inwinder

desc = 'Create a maze by applying Inwinder to a polar grid.'

def main(args):
    """entry point"""
    import matplotlib.pyplot as plt
    from polar_grid import Polar_Grid
    from layout_plot_polar import Polar_Layout

    m = 20
    grid = Polar_Grid(m)
    Inwinder.on(grid)

    layout = Polar_Layout(grid, plt, title="Inwinder - Single Pole Cell")
    layout.palette[0] = 'red'
    layout.palette[1] = 'green'
    layout.color[grid[0,0]] = 0
    layout.color[grid[m-1, 0]] = 1

    layout.draw_grid()
    layout.render('demos/inwinder1.png')

    grid = Polar_Grid(m, poleCells=3)
    Inwinder.on(grid)

    layout = Polar_Layout(grid, plt, title="Inwinder - Three Wedges at Pole")
    layout.palette[0] = 'red'
    layout.palette[1] = 'green'
    layout.color[grid[0,0]] = 0
    layout.color[grid[m-1, 0]] = 1

    layout.draw_grid()
    layout.render('demos/inwinder2.png')
    # plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=desc)
    args = parser.parse_args()
    main(args)

# END: inwinder_demo.py
