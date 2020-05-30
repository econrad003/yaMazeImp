# -*- coding: utf-8 -*-
# layout_plot_color.py - a layout color class for rectangular mazes
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
"""
layout_plot_color.py - basic plotting with color for rectangular mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from layout_plot import Layout
import matplotlib.patches as patches

class Color_Layout(Layout):
    """implementation of rectangular maze wit colored cells"""
    
    def __init__(self, grid, plt, **kwargs):
        """constructor"""
        super().__init__(grid, plt, **kwargs)
        self.color = {}               # default - no colors
        self.palette ={}              # palette

    def draw_cell(self, cell, color):
        """draw a square cell with no inset"""
        if cell in self.color:
            facecolor = self.palette[self.color[cell]]
            x, y = cell.position
            half = cell.scale / 2.0
            x0, y0 = x-half, y-half         # SW corner
            rect = patches.Rectangle((x0,y0), cell.scale, cell.scale,
                                     edgecolor=None,
                                     facecolor=facecolor)
            self.ax.add_patch(rect)
        super().draw_cell(cell, color)

    def set_palette_color(self, ID, color):
        """load the color into the palette"""
        self.palette[ID] = color

    def set_color(self, cell, ID):
        """set the color of a cell"""
        self.color[cell] = ID

# END: layout_plot_color.py
