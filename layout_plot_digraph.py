# -*- coding: utf-8 -*-
# layout_plot_digraph.py - a layout color class for rectangular mazes
#   with one-way passages
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
#     15 Sep 2020 - Initial version
"""
layout_plot_digraph.py - basic plotting with color for rectangular mazes
    with one-way passages
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

class Digraph_Layout(Color_Layout):
    """implementation of rectangular maze with one-way passages"""

    #
    # Class hierarchy:
    #     object - base
    #       Layout - basic matplotlib plotting of two-way rectangular
    #                mazes
    #         Color_Layout - add face coloring
    #           Digraph_Layout - allow for one-way connections
    #
    # In Layout, the cell-drawing operations don't check for one-way
    # connections.  A wall is drawn where we instead need a one-way
    # passage.
    #

    @staticmethod
    def passage_status(cell, nbr):
        """determine whether a connection is a wall, a passage in, a
            passage out, or a two-way passage

        Return value:
            None - a boundary wall
            0 - an internal wall
            1 - a one-way passage into the cell
            2 - a one-way passage out from the cell
            3 - a two-way passage
        """
        if not nbr:
            return None
        stat = 0
        if cell.have_passage(nbr):
            stat += 2
        if nbr.have_passage(cell):
            stat += 1
        return stat

    def draw_wall(self, cell, X, Y, color):
        """draw a wall"""
        if "underCell" not in cell.kwargs:
            self.draw_polyline(X, Y, color)

    def draw_corner(self, cell, X, Y, color):
        """draw a wall"""
        x0, x3 = X
        y0, y3 = Y
        inset = 0.1 * (x3 - x0)
        x1, x2 = x0 + inset, x3 - inset
        inset = 0.1 * (y3 - y0)
        y1, y2 = y0 + inset, y3 - inset
        X, Y = [x0, x1], [y0, y1]
        self.draw_polyline(X, Y, color)
        X, Y = [x2, x3], [y2, y3]
        self.draw_polyline(X, Y, color)

    def draw_arrow(self, direction, X, Y, half, color):
        """draw an arrow leaving a a cell.

        Arguments:
            X, Y - abscissae and ordinates of wall endponts
            half - distance from center to wall

        This will look bad if the cell is a one-way undercell.
        But we should be using insets with weave mazes anyway.
        """
        inset1 = half * 0.6             # inset for arrowshaft
        inset2 = half * 0.2             # inset for arrowhead
        x0, x1 = X                      # wall endpoints
        y0, y1 = Y
        if direction == "south":
            x2 = x3 = (x0+x1)/2         # shaft
            y2, y3 = y0 + inset1, y0
            y4 = y5 = y3 + inset2       # head
            x4, x5 = x3 - inset2, x3 + inset2
        elif direction == "east":
            y2 = y3 = (y0+y1)/2         # shaft
            x2, x3 = x0 - inset1, x0
            x4 = x5 = x3 - inset2       # head
            y4, y5 = y3 + inset2, y3 - inset2
        elif direction == "north":
            x2 = x3 = (x0+x1)/2         # shaft
            y2, y3 = y0 - inset1, y0
            y4 = y5 = y3 - inset2       # head
            x4, x5 = x2 + inset2, x2 - inset2
        elif direction == "west":
            y2 = y3 = (y0+y1)/2         # shaft
            x2, x3 = x0 + inset1, x0
            x4 = x5 = x3 + inset2       # head
            y4, y5 = y3 - inset2, y3 + inset2
        else:
                # unknown direction
            return
        X, Y = [x2, x3], [y2, y3]           # shaft
        self.draw_polyline(X, Y, color)
        X, Y = [x4, x3, x5], [y4, y3, y5]   # head
        self.draw_polyline(X, Y, color)

    def draw_passage(self, cell, direction, X, Y, half, color):
        """draw a passage or a wall (no inset)

        Parameters:
            cell - the cell being drawn
            direction - one of the four compass directions
            X, Y - the endpoints of the grid wall
            half - the half-width of the cell, used for
                for drawing arrows
            color - the line color
        """
        stat = self.passage_status(cell, cell[direction])
        if stat in {1, 3}:
                # two-way passage or one-way passage in
            self.draw_corner(cell, X, Y, color)
        elif stat == 2:
            self.draw_arrow(direction, X, Y, half, color)
        else:
            self.draw_wall(cell, X, Y, color)

    def draw_patch(self, x0, y0, b, h, fc):
        """draw a rectangular patch

        Arguments:
            x0, y0 - SW corner
            b, h - breadth and height
            fc - the fill color
        """
        rect = patches.Rectangle((x0, y0), b, h, edgecolor=None, \
            facecolor=fc)
        self.ax.add_patch(rect)

    def draw_cell(self, cell, color):
        """draw a square cell with no inset"""
            # face drawing code from Color_Layout
        x, y = cell.position
        half = cell.scale / 2.0
        if cell in self.color:
            fc = self.palette[self.color[cell]]
            self.draw_patch(x-half, y-half, cell.scale, cell.scale, fc)

            # cell boundary code from Layout
        x0, y0 = x-half, y-half         # SW corner
        x1, y1 = x+half, y-half         # SE corner
        x2, y2 = x+half, y+half         # NE corner
        x3, y3 = x-half, y+half         # NW corner
        X, Y = [x0, x1], [y0, y1]
        self.draw_passage(cell, "south", X, Y, half, color)
        X, Y = [x1, x2], [y1, y2]
        self.draw_passage(cell, "east", X, Y, half, color)
        X, Y = [x2, x3], [y2, y3]
        self.draw_passage(cell, "north", X, Y, half, color)
        X, Y = [x3, x0], [y3, y0]
        self.draw_passage(cell, "west", X, Y, half, color)

    def draw_inset_face(self, cell, scale, half, color, inset):
        """color the face of the and passages of the cell

        This is face drawing code adapted from Color_Layout.
        """
            # color the face and passages of the cell.
            # 
            # if this is a weave maze and the cell is an undercell, we don't
            # color the face as it is hidden by its parent cell.
        fc = self.palette[self.color[cell]]
        x, y = cell.position
        scale -= inset + inset

        if "underCell" not in cell.kwargs:
            x0, y0 = x-half+inset, y-half+inset         # central box
            self.draw_patch(x0, y0, scale, scale, fc)

        if cell.status("south"):            # south passage
            x0, y0 = x-half+inset, y-half
            self.draw_patch(x0, y0, scale, inset, fc)

        if cell.status("east"):             # east passage
            x0, y0 = x+half-inset, y-half+inset 
            self.draw_patch(x0, y0, inset, scale, fc)

        if cell.status("north"):            # north passage
            x0, y0 = x-half+inset, y+half-inset 
            self.draw_patch(x0, y0, scale, inset, fc)

        if cell.status("west"):             # west passage
            x0, y0 = x-half, y-half+inset 
            self.draw_patch(x0, y0, inset, scale, fc)

    def draw_inset_passage(self, X, Y, c):
        """draw the passage walls

        Arguments:
            X, Y - 4-vectors
            c - a color or None for the default linecolor
        """
        self.draw_polyline([X[0], X[1]], [Y[0], Y[1]], c)
        self.draw_polyline([X[2], X[3]], [Y[2], Y[3]], c)

    def draw_inset_cell(self, cell, color, inset):
        """draw a square cell with an inset"""
        x, y = cell.position
        scale = cell.scale
        half = cell.scale / 2.0
        if half <= inset:
                # this is an error.  To recover, we draw the cell plainly.
            self.draw_cell(cell, color)
            return

        if cell in self.color:
            self.draw_inset_face(cell, scale, half, color, inset)

                # now fill in the walls and passages
                # this code was adapted from Layout
        xx = [x-half, x-half+inset, x+half-inset, x+half]
        yy = [y-half, y-half+inset, y+half-inset, y+half]

                # Watch out for:
                #   1) directed passages
                #      a) inward arcs - draw the passage walls
                #      b) outward arcs - draw the arrow
                #   2) undercells - 
                #      a) don't draw internal walls
                #      b) watch arrow placement

        stat = self.passage_status(cell, cell["south"])
        if stat:          # draw passage walls
            X = [xx[1], xx[1], xx[2], xx[2]]
            Y = [yy[1], yy[0], yy[1], yy[0]]
            self.draw_inset_passage(X, Y, color)
        if "underCell" in cell.kwargs:
            if stat == 2:
                    # draw arrow
                X = [xx[1], xx[2]]
                Y = [yy[1]-half, yy[1]-half]
                self.draw_arrow("south", X, Y, half, color)
        else:
            if not stat:
                    # draw wall
                X, Y = [xx[1], xx[2]], [yy[1], yy[1]]
                self.draw_polyline(X, Y, color)
            elif stat == 2:
                    # draw arrow
                X, Y = [xx[1], xx[2]], [yy[1], yy[1]]
                self.draw_arrow("south", X, Y, half, color)

        stat = self.passage_status(cell, cell["east"])
        if stat:          # draw passage walls
            X = [xx[2], xx[3], xx[2], xx[3]]
            Y = [yy[1], yy[1], yy[2], yy[2]]
            self.draw_inset_passage(X, Y, color)
        if "underCell" in cell.kwargs:
            if stat == 2:
                    # draw arrow
                X = [xx[2]+half, xx[2]+half]
                Y = [yy[1], yy[2]]
                self.draw_arrow("east", X, Y, half, color)
        else:
            if not stat:
                    # draw wall
                X, Y = [xx[2], xx[2]], [yy[1], yy[2]]
                self.draw_polyline(X, Y, color)
            elif stat == 2:
                    # draw arrow
                X, Y = [xx[2], xx[2]], [yy[1], yy[2]]
                self.draw_arrow("east", X, Y, half, color)

        stat = self.passage_status(cell, cell["north"])
        if stat:          # draw passage walls
            X = [xx[1], xx[1], xx[2], xx[2]]
            Y = [yy[2], yy[3], yy[2], yy[3]]
            self.draw_inset_passage(X, Y, color)
        if "underCell" in cell.kwargs:
            if stat == 2:
                    # draw arrow
                X = [xx[1], xx[2]]
                Y = [yy[2]+half, yy[2]+half]
                self.draw_arrow("north", X, Y, half, color)
        else:
            if not stat:
                    # draw wall
                X, Y = [xx[1], xx[2]], [yy[2], yy[2]]
                self.draw_polyline(X, Y, color)
            elif stat == 2:
                    # draw arrow
                X, Y = [xx[1], xx[2]], [yy[2], yy[2]]
                self.draw_arrow("north", X, Y, half, color)

        stat = self.passage_status(cell, cell["west"])
        if stat:          # draw passage walls
            X = [xx[0], xx[1], xx[0], xx[1]]
            Y = [yy[1], yy[1], yy[2], yy[2]]
            self.draw_inset_passage(X, Y, color)
        if "underCell" in cell.kwargs:
            if stat == 2:
                    # draw arrow
                X = [xx[1]-half, xx[1]-half]
                Y = [yy[1], yy[2]]
                self.draw_arrow("west", X, Y, half, color)
        else:
            if not stat:
                    # draw wall
                X, Y = [xx[1], xx[1]], [yy[1], yy[2]]
                self.draw_polyline(X, Y, color)
            elif stat == 2:
                    # draw arrow
                X, Y = [xx[1], xx[1]], [yy[1], yy[2]]
                self.draw_arrow("west", X, Y, half, color)

# END: layout_plot_digraph.py
