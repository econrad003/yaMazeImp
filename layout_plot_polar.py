# -*- coding: utf-8 -*-
# layout_plot_polyar.py - a layout class for polar mazes
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
#     11 Jul 2020 - Initial version
#     13 Jul 2020 - Matplotlib support for polar coordinates and flood fill is
#       poorly documented, so we will stick to polygonal areas.  For cells in
#       outer latitudes, these will approximate circular bars.  In inner latitudes,
#       the polygons will be obvious.
"""
layout_plot_polar.py - basic plotting for polar mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    If the maze has a central cell with fewer than two neighbors, it will not
    be properly rendered.
"""

from math import cos, sin, pi
import matplotlib.patches as patches
from layout_plot_color import Color_Layout

class Polar_Layout(Color_Layout):
    """implementation of polar maze plotting"""

    def __init__(self, grid, plt, **kwargs):
        """constructor"""
            ##################################################################
            # We should really use polar coordinates, but matplotlib support
            # for polar coordinates is inconsistent and poorly documented.
            #
            # Note: we can associate polar coordinates with an Axes object
            # that has rectangular coordinates, but documentation is weak
            # and the feature does not seem to be well-known, indicating
            # that the feature may be unstable.)
            #
            # It's not as aesthetically pleasing near the center (aka the
            # pole) but as a workaround we instead just draw polygons.
            # Note: Some special manipulation of fig and ax in kwargs may
            # need to be placed here if we do use polar coordinates.
            #
            # For the moment, all we need is the parent constructor...  But
            # pylint doesn't like a constructor that just calls the parent,
            # so...
            ##################################################################

            # pylint: disable=useless-super-delegation

        super().__init__(grid, plt, **kwargs)

    def draw_annular_sector(self, cell, color, celltype):
        """draw an annular sector cell with no inset"""
            # Sorry, but this needs all these variables to be readable!
            # pylint: disable=too-many-locals
        r0, r1, theta1, theta2 = celltype       # unpack coordinates
        theta1 *= 2 * pi                        # convert to radians
        theta2 *= 2 * pi

            # We could paint the faces using a polar bar chart, but matplotlib
            # has surprisingly poor support (or possibly just poor
            # documentation) for drawing the walled edges in polar
            # coordinates.

            # workaround - polygonal faces
        if cell in self.color:
            outwards = cell.outwards
            if outwards is 0:
                outwards = 20                   # to give roundness
            xy = []                             # points in ccw order
                # first lay out the outer wall of the cell
            for i in range(outwards+1):
                theta = theta1 + (i * (theta2 - theta1)/outwards)
                xy.append((r1 * cos(theta), r1 * sin(theta)))
                # now lay out the inner wall (note order!)
            xy.append((r0 * cos(theta2), r0 * sin(theta2)))
            xy.append((r0 * cos(theta1), r0 * sin(theta1)))
            polygon = patches.Polygon(xy, closed=True,
                                      facecolor=self.palette[self.color[cell]])
            self.ax.add_patch(polygon)

            # draw the inward and counterclockwise walls
        if not cell.status("ccw"):
                # rectangular coordinates
            xx = [r0 * cos(theta2), r1 * cos(theta2)]
            yy = [r0 * sin(theta2), r1 * sin(theta2)]
            self.draw_polyline(xx, yy, color)
        if not cell.status("inward"):
                # polygonal compromise
            xx = [r0 * cos(theta1), r0 * cos(theta2)]
            yy = [r0 * sin(theta1), r0 * sin(theta2)]
            self.draw_polyline(xx, yy, color)

    def draw_polar_wedge(self, cell, color, celltype):
        """draw a wedge cell at the pole with no inset"""
            # Sorry, but this needs all these variables to be readable!
            # pylint: disable=too-many-locals
        r1, theta1, theta2 = celltype           # unpack coordinates
        r0 = 0
        theta1 *= 2 * pi                        # convert to radians
        theta2 *= 2 * pi

            # workaround - polygonal faces
        if cell in self.color:
            outwards = cell.outwards
            if outwards is 0:
                outwards = 20                   # to give roundness
            xy = []                             # points in ccw order
                # first lay out the outer wall of the cell
            for i in range(outwards+1):
                theta = theta1 + (i * (theta2 - theta1)/outwards)
                xy.append((r1 * cos(theta), r1 * sin(theta)))
                # now connect the outer wall to the pole
            xy.append((0, 0))
            polygon = patches.Polygon(xy, closed=True,
                                      facecolor=self.palette[self.color[cell]])
            self.ax.add_patch(polygon)

            # draw the counterclockwise wall
        if not cell.status("ccw"):
                # rectangular coordinates
            xx = [r0 * cos(theta2), r1 * cos(theta2)]
            yy = [r0 * sin(theta2), r1 * sin(theta2)]
            self.draw_polyline(xx, yy, color)

    def draw_pole_cell(self, cell, r1):
        """draw a circular cell about the pole with no inset"""
        # this one is easy - just draw the face as there is no ccw
        # wall and no inward wall.
        if cell not in self.color:
            return
        theta1 = 0
        theta2 = 2 * pi

            # workaround - polygonal faces
        outwards = cell.outwards
        if outwards is 0:
            outwards = 20                   # to give roundness
        xy = []
            # lay out the outer wall of the cell
        for i in range(outwards+1):
            theta = theta1 + (i * (theta2 - theta1)/outwards)
            xy.append((r1 * cos(theta), r1 * sin(theta)))
        polygon = patches.Polygon(xy, closed=True,
                                  facecolor=self.palette[self.color[cell]])
        self.ax.add_patch(polygon)

    def draw_cell(self, cell, color):
        """draw a cell with no inset"""
            # get the cell geometry
        celltype = cell.celltype
        if celltype[0] == 'sector':     # annular sector
            self.draw_annular_sector(cell, color, celltype[1:])
        elif celltype[0] == 'wedge':    # circular sector
            self.draw_polar_wedge(cell, color, celltype[1:])
        else:   # celltype[0] == 'circle'
            self.draw_pole_cell(cell, celltype[1])

    def draw_grid(self, linecolor="black"):
        """draw the maze"""
        super().draw_grid(linecolor)

            # rectangular coordinates (crappy but works)
        d = self.grid.rows * 2         # diameter, not radius
                # and degrees instead of radians
        arc = patches.Arc([0, 0], d, d, theta1=0, theta2=360,
                          edgecolor=linecolor)
        self.ax.add_patch(arc)

        for cell in self.grid.each():
            self.draw_cell(cell, linecolor)


# END: layout_plot_polar.py
