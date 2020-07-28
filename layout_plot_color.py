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
#     26 Jul 2020 - Add method to color inset cells
#     28 Jul 2020 - Need to color passages for inset cells.
#       Note to self: For undercells, only the passage are colored as the
#         body of the cell is hidden from view.  This will be important in
#         weave mazes.
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

    def draw_inset_cell(self, cell, color, inset):
        """draw a square cell with an inset"""
        scale = cell.scale
        half = cell.scale / 2.0
        if half <= inset:
                # this is an error.  To recover, we draw the cell plainly.
            self.draw_cell(cell, color)
            return

        if cell not in self.color:
                # cell is not colored; just draw walls and passages...
            super().draw_inset_cell(cell, color, inset)
            return

            # color the face and passages of the cell.
            # 
            # if this is a weave maze and the cell is an undercell, we don't
            # color the face as it is hidden by its parent cell.

        facecolor = self.palette[self.color[cell]]
        x, y = cell.position
        scale -= inset + inset

        if "underCell" not in cell.kwargs:
            x0, y0 = x-half+inset, y-half+inset         # SW corner
            rect = patches.Rectangle((x0, y0), scale, scale, \
                edgecolor=None, facecolor=facecolor)
            self.ax.add_patch(rect)

        if cell.status("south"):            # south passage
            x0, y0 = x-half+inset, y-half
            rect = patches.Rectangle((x0,y0), scale, inset, \
                edgecolor=None, facecolor=facecolor)
            self.ax.add_patch(rect)

        if cell.status("east"):             # east passage
            x0, y0 = x+half-inset, y-half+inset 
            rect = patches.Rectangle((x0,y0), inset, scale, \
                edgecolor=None, facecolor=facecolor)
            self.ax.add_patch(rect)

        if cell.status("north"):            # north passage
            x0, y0 = x-half+inset, y+half-inset 
            rect = patches.Rectangle((x0,y0), scale, inset, \
                edgecolor=None, facecolor=facecolor)
            self.ax.add_patch(rect)

        if cell.status("west"):             # west passage
            x0, y0 = x-half, y-half+inset 
            rect = patches.Rectangle((x0,y0), inset, scale, \
                edgecolor=None, facecolor=facecolor)
            self.ax.add_patch(rect)

            # now fill in the walls and passages
        super().draw_inset_cell(cell, color, inset)

    def set_palette_color(self, ID, color):
        """load the color into the palette"""
        self.palette[ID] = color

    def set_color(self, cell, ID):
        """set the color of a cell"""
        self.color[cell] = ID

# END: layout_plot_color.py
