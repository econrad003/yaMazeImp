# -*- coding: utf-8 -*-
# layout_plot.py - a layout class for rectangular mazes using matplotlib
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
#     12 May 2020 - Initial version
#     27 Jul 2020 - Add draw_inset_cell method
"""
layout_plot.py - basic plotter implementation for rectangular mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

class Layout(object):
    """implementation of rectangular maze layout using matplotlib"""
    
    def __init__(self, grid, plt, **kwargs):
        """constructor"""
        self.grid = grid
        self.plt = plt
        self.kwargs = kwargs

        self.fig, self.ax = kwargs["figure"] if "figure" in kwargs \
            else plt.subplots(1, 1)
        if "title" in self.kwargs:
            self.ax.set_title(self.kwargs["title"])

    def draw_cell(self, cell, color):
        """draw a square cell with no inset"""
        x, y = cell.position
        half = cell.scale / 2
        x0, y0 = x-half, y-half         # SW corner
        x1, y1 = x+half, y-half         # SE corner
        x2, y2 = x+half, y+half         # NE corner
        x3, y3 = x-half, y+half         # NW corner
        if not cell.status("south"):
            self.draw_polyline([x0, x1], [y0, y1], color)
        if not cell.status("east"):
            self.draw_polyline([x1, x2], [y1, y2], color)
        if not cell.status("north"):
            self.draw_polyline([x2, x3], [y2, y3], color)
        if not cell.status("west"):
            self.draw_polyline([x3, x0], [y3, y0], color)

    def draw_inset_cell(self, cell, color, inset):
        """draw a square cell with a given inset"""
        x, y = cell.position
        half = cell.scale / 2
        if half <= inset:
            self.draw_cell(cell, color)
            return
        xx = [x-half, x-half+inset, x+half-inset, x+half]
        yy = [y-half, y-half+inset, y+half-inset, y+half]

        if cell.status("south"):        # southward passage
            y0, y1 = yy[1], yy[0]
            x0 = x1 = xx[1]
            self.draw_polyline([x0, x1], [y0, y1], color)
            x0 = x1 = xx[2]
            self.draw_polyline([x0, x1], [y0, y1], color)
        else:                           # southward wall
            x0, x1 = xx[1], xx[2]
            y0 = y1 = yy[1]
            self.draw_polyline([x0, x1], [y0, y1], color)

        if cell.status("east"):         # eastward passage
            x0, x1 = xx[2], xx[3]
            y0 = y1 = yy[1]
            self.draw_polyline([x0, x1], [y0, y1], color)
            y0 = y1 = yy[2]
            self.draw_polyline([x0, x1], [y0, y1], color)
        else:                           # eastward wall
            y0, y1 = yy[1], yy[2]
            x0 = x1 = xx[2]
            self.draw_polyline([x0, x1], [y0, y1], color)

        if cell.status("north"):        # northward passage
            y0, y1 = yy[2], yy[3]
            x0 = x1 = xx[1]
            self.draw_polyline([x0, x1], [y0, y1], color)
            x0 = x1 = xx[2]
            self.draw_polyline([x0, x1], [y0, y1], color)
        else:                           # northward wall
            x0, x1 = xx[1], xx[2]
            y0 = y1 = yy[2]
            self.draw_polyline([x0, x1], [y0, y1], color)

        if cell.status("west"):         # westward passage
            x0, x1 = xx[0], xx[1]
            y0 = y1 = yy[1]
            self.draw_polyline([x0, x1], [y0, y1], color)
            y0 = y1 = yy[2]
            self.draw_polyline([x0, x1], [y0, y1], color)
        else:                           # westward wall
            y0, y1 = yy[1], yy[2]
            x0 = x1 = xx[1]
            self.draw_polyline([x0, x1], [y0, y1], color)

    def draw_polyline(self, X, Y, linecolor):
        """draw a wall"""
        self.ax.plot(X, Y, color=linecolor)

    def draw_grid(self, linecolor="black"):
        for cell in self.grid.each():
            if cell.inset > 0:
                self.draw_inset_cell(cell, linecolor, cell.inset)
            else:
                self.draw_cell(cell, linecolor)

    def render(self, filename, tight=False):
        """render the output"""
        if tight:
            self.fig.savefig(filename, bbox_inches='tight', pad_inched=0.0)
        else:
            self.fig.savefig(filename)
        print('rendered figure to %s' % filename)

# END: layout_plot.py
