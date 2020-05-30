# -*- coding: utf-8 -*-
# layout_plot_polygon.py - a layout class for mazes with polygonal cells
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
layout_plot_polygon.py - basic plotting for mazes with polygonal cells
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from layout_plot_color import Color_Layout
import matplotlib.patches as patches

class Polygonal_Layout(Color_Layout):
    """implementation of maze plotting with polygonal cells"""
    
    def draw_cell(self, cell, color):
        """draw a square cell with no inset"""
            # draw the face
        if cell in self.color:
            facecolor = self.palette[self.color[cell]]
            polygon = patches.Polygon(cell.walls, closed=True,
                                      edgecolor=None,
                                      facecolor=facecolor)
            self.ax.add_patch(polygon)

        # Important: here we do not call super()

            # draw the walls
        n = len(cell.directions)
        for i in range(n):
            direction = cell.directions[i]
            if not cell.status(direction):
                x0, y0 = cell.walls[i]
                x1, y1 = cell.walls[(i+1)%n]         # wrap around
                self.draw_polyline([x0, x1], [y0, y1], color)
            
# END: layout_plot_polygons.py
