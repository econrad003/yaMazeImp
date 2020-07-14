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

from layout_plot_color import Color_Layout
import matplotlib.patches as patches
from math import cos, sin, pi

class Polar_Layout(Color_Layout):
    """implementation of polar maze plotting"""
    
    def __init__(self, grid, plt, **kwargs):
        """constructor"""
        self.grid = grid
        self.plt = plt
        self.kwargs = kwargs
        self.color = {}               # default - no colors
        self.palette ={}              # palette

            # We should really use polar coordinates, but matplotlib support
            # for polar coordinates is inconsistent and poorly documented.

        self.fig, self.ax = kwargs["figure"] if "figure" in kwargs \
            else plt.subplots(1, 1)
        if "title" in self.kwargs:
            self.ax.set_title(self.kwargs["title"])

    def draw_cell(self, cell, color):
        """draw a square cell with no inset"""
            # get the cell geometry
        celltype = cell.celltype
        if celltype[0] == 'sector':     # annular sector
            r0, r1, theta1, theta2 = celltype[1:]
        elif celltype[0] == 'wedge':    # circular sector
            r1, theta1, theta2 = celltype[1:]
            r0 = 0
        else:   # celltype[0] == 'circle'
            r1 = celltype[1]
            theta1 = 0
            theta2 = 1
            r0 = 0

            # from revolutions to radians
        theta1 *= 2 * pi
        theta2 *= 2 * pi

            # draw the face
#       We need to figure out how to do this in rectangular coordinates...
#         It would be easy in polar coordinates using bars, but then we have
#       the problem of drawing arcs of a given radius about the center...
#       This second ploblem can be solved by applying two sets of coordinates
#       to the axes, but the required code would be hard to support.

            # workaround - polygonal faces
        if cell in self.color:
            outwards = cell.outwards
            if outwards is 0:
                outwards = 20
            xy = []
                # lay out the outer wall of the cell
            for i in range(outwards+1):
                theta = theta1 + (i * (theta2 - theta1)/outwards)
                xy.append((r1 * cos(theta), r1 * sin(theta)))

                # and inner wall if applicable
            if celltype[0] == 'sector':
                xy.append((r0 * cos(theta2), r0 * sin(theta2)))
                xy.append((r0 * cos(theta1), r0 * sin(theta1)))
            elif celltype[0] == 'wedge':
                xy.append((0, 0))

            polygon = patches.Polygon(xy, closed=True,
                                      facecolor=self.palette[self.color[cell]])
            self.ax.add_patch(polygon)

              # polar coordinate bars
#        if cell in self.color:
#            facecolor = self.palette[self.color[cell]]
#            align = 'edge'
#            width = theta2 - theta1
#            bar = ax.bar(theta1, r1, width=width, bottom=r0, color=facecolor)

        # Important: here we do not call super()

            # draw the walls
        # print("%s (%f-%f,%f-%f)" % (cell.name, r0, r1, theta1, theta2))
        n = len(cell.directions)
        for i in range(n):
            direction = cell.directions[i]
            if not cell.status(direction):
                if direction == "ccw":
                        # polar coordinates
#                    self.draw_polyline([theta1, theta1], [r0, r1], color)

                        # rectangular coordinates
                    xx = [r0 * cos(theta2), r1 * cos(theta2)]
                    yy = [r0 * sin(theta2), r1 * sin(theta2)]
                    self.draw_polyline(xx, yy, color)

                elif direction == "inward":
                        # polar coordinates - this does not work at all
#                    ts = np.arange(theta1, theta2, 0.1)
#                    for t in ts:
#                        self.plt.polar(t, r0)

                        # this works (in a manner) but is incompatible with bars above
#                    self.draw_polyline([theta1, theta2], [r0, r0], color)

                        # rectangular coordinates - this works, but it's crappy
#                    t1 = theta1 * 180 / pi    # we need degrees!!!
#                    t2 = theta2 * 180 / pi    # more degrees!!!
#                    d = 2 * r0                # diameter, not radius
#                    arc = patches.Arc([0, 0], d, d, theta1=t1, theta2=t2,
#                                      edgecolor=color)
#                    self.ax.add_patch(arc)

                        # and this is the polygonal compromise
                    xx = [r0 * cos(theta1), r0 * cos(theta2)]
                    yy = [r0 * sin(theta1), r0 * sin(theta2)]
                    self.draw_polyline(xx, yy, color)

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
