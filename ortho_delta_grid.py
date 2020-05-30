# -*- coding: utf-8 -*-
# ortho_delta_grid.py - grid class for rectangular delta mazes
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
#     27 May 2020 - Initial version
"""
ortho_delta_grid.py - rectangular delta grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A rectangular delta maze is a maze with right triangular cells that
tessellate a rectangle with sides parallel to the coordinate axes.
The cells have two orientations: (1) E, NW, S and (2) W, SE, N.  The
grid consists of small squares, each divided by a diagonal running
northeastward to form two right triangles, one of each orientation.

More information:

    see grid.py and cell.py for more information.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from polygonal_cell import Polygonal_Cell
from grid import Grid

class Delta_Cell(Polygonal_Cell):
    """triangular cell"""
    pass

class Ortho_Delta_Grid(Grid):
    """rectangular delta grid implementation"""

    def __init__(self, rows, cols, **kwargs):
        """constructor

        Mandatory arguments:
            rows - the number of rows in the grid
            cols - the number of columns in the grid

            each (square) entry has two triangular cells

        Optional named arguments:
            name - a name for the cell
            origin - default (0,0) - the (x,y)-coordinates of the center
                of the lower left cell
            scale - default 1 - the length of the side of a cell
            inset - default 0 - the inset of a cell
            content - default ' ' - for ASCII and Unicode
            bgcolor - default None - for PNG
            wallAdder - if present (ignoring value), will add passages
        """
            # grid management
        self.rows = rows
        self.cols = cols
        self.origin = kwargs["origin"] if "origin" in kwargs else (0, 0)
        self.scale = kwargs["scale"] if "scale" in kwargs else 1
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

        super().__init__(**kwargs)

    def make_delta1(self, i, j, x, y, scale):
        """create an E-NW-S cell"""
        index = (i, j, 1)
        P = (x+scale, y)
        Q = (x+scale, y+scale)
        R = (x, y)
        name = "T1[%d,%d]" % (i, j)
        cell = Delta_Cell(index, ['E', 'NW', 'S'], [P, Q, R], name=name)
        self[index] = cell

    def make_delta2(self, i, j, x, y, scale):
        """create an W-SE-N cell"""
        index = (i, j, 2)
        P = (x, y+scale)
        Q = (x, y)
        R = (x+scale, y+scale)
        name = "T2[%d,%d]" % (i, j)
        cell = Delta_Cell(index, ['W', 'SE', 'N'], [P, Q, R], name=name)
        self[index] = cell

    def initialize(self):
        """grid initialization, e.g. create cells"""
        scale = self.scale
        h, k = self.origin
        for i in range(self.rows):
            for j in range(self.cols):
                x = self.scale * j + h
                y = self.scale * i + k
                self.make_delta1(i, j, x, y, scale)
                self.make_delta2(i, j, x, y, scale)

    def configure(self):
        """grid configuration, e.g. configure neighborhoods"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.configure_topology(i, j)   # ignore return value

    def configure_topology(self, i, j):
        """configure neighborhood for a given cell"""
            #   pylint: disable=multiple-statements
            #           reason: simple conditions

        cell_SE = self[i, j, 1]
        cell_NW = self[i, j, 2]
        assert cell_SE and cell_NW, "both cells must exist"

        cell_SE["NW"] = cell_NW
        cell_NW["SE"] = cell_SE

        north = self[i+1, j, 1]
        if north: cell_NW["N"] = north
        south = self[i-1, j, 2]
        if south: cell_SE["S"] = south

        east = self[i, j+1, 2]
        if east: cell_SE["E"] = east
        west = self[i, j-1, 1]
        if west: cell_NW["W"] = west

        if "wallAdder" in self.kwargs:
            if north: cell_NW.makePassage(north)
            if east: cell_SE.makePassage(east)
            cell_SE.makePassage(cell_NW)

    def each_row(self):
        """iterate row by row"""
        for i in range(self.rows):
            L = []
            for j in range(self.cols):
                L.append(self[i, j, 2])
                L.append(self[i, j, 1])
            yield L

    def each_column(self):
        """iterate column by column"""
        for j in range(self.cols):
            L = []
            for i in range(self.rows):
                L.append(self[i, j, 1])
                L.append(self[i, j, 2])
            yield L

    def each_rowcol(self):
        """iterate by row and column (row major order)"""
        for i in range(self.rows):
            for j in range(self.cols):
                yield self[i, j, 2]
                yield self[i, j, 1]

    def each_colrow(self):
        """iterate by column and row (column major order)"""
        for j in range(self.cols):
            for i in range(self.rows):
                yield self[i, j, 1]
                yield self[i, j, 2]

# END: ortho_delta_grid.py
