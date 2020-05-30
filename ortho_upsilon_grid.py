# -*- coding: utf-8 -*-
# ortho_upsilon_grid.py - grid class for rectangular delta mazes
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
#     30 May 2020 - Initial version
"""
ortho_upsilon_grid.py - rectangular upsilon grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A rectangular upsilon maze is a maze with an alternaning mix of regular
octagons and squares collected in a rectangle with sides parallel to the
coordinate axes.  Each of the regular polygons is centered on a lattice
point of the rectangle.

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
from math import sqrt, sin, cos, pi

class Octagonal_Cell(Polygonal_Cell):
    """a cell in the shape of regular octagon that is centered on a lattice
    point"""
    labels = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
    vectors = [(cos(i*pi/4 - pi/8), sin(i*pi/4 - pi/8)) for i in range(8)]
    radius = 1
    apothem = cos(pi/8)

    def __init__(self, origin, scale, index, **kwargs):
        """create an octagonal cell"""
        i, j = index
            # determine the cell's center
        sep = (Octagonal_Cell.apothem + Quadrilateral_Cell.apothem) * scale
        h, k = origin
        x0 = h + j * sep
        y0 = k + i * sep
            # determine the cells vertices
        polygon = []
        for i in range(8):
            h, k = Octagonal_Cell.vectors[i]    # note that r=1
            polygon.append((x0+h, y0+k))

        kwargs['name'] = 'P8[%d,%d]' % index
        super().__init__(index, Octagonal_Cell.labels, polygon, **kwargs)

class Quadrilateral_Cell(Polygonal_Cell):
    """a cell in the shape of square that is centered on a lattice
    point"""
    labels = ['E', 'N', 'W', 'S']
    vectors = [(cos(i*pi/2 - pi/4), sin(i*pi/2 - pi/4)) for i in range(4)]
    apothem = sin(pi/8)           # equal to half of a side
    radius = apothem * sqrt(2)    # orhalf of a diagonal

    def __init__(self, origin, scale, index, **kwargs):
        """create a square cell"""
        i, j = index
            # determine the cell's center
        sep = (Octagonal_Cell.apothem + Quadrilateral_Cell.apothem) * scale
        h, k = origin
        x0 = h + j * sep
        y0 = k + i * sep
            # determine the cells vertices
        polygon = []
        for i in range(4):
            h, k = Quadrilateral_Cell.vectors[i]
            h *= Quadrilateral_Cell.radius
            k *= Quadrilateral_Cell.radius
            polygon.append((x0+h, y0+k))
        
        kwargs['name'] = 'P4[%d,%d]' % index
        super().__init__(index, Quadrilateral_Cell.labels, polygon, **kwargs)

class Ortho_Upsilon_Grid(Grid):
    """rectangular upsilon grid implementation"""

    def __init__(self, rows, cols, **kwargs):
        """constructor

        Mandatory arguments:
            rows - the number of rows in the grid
            cols - the number of columns in the grid

            Each lattice point has either a square or a regular octagon at
            its center.

        Optional named arguments:
            kwargs['name'] = 'O[%d,%d]' % index
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

    def initialize(self):
        """grid initialization, e.g. create cells"""
        scale = self.scale
        origin = self.origin
        for i in range(self.rows):
            for j in range(self.cols):
                f = Octagonal_Cell if (i+j)%2 is 0 else \
                    Quadrilateral_Cell
                index = (i, j)
                self[i, j] = f(origin, scale, index)

    def configure(self):
        """grid configuration, e.g. configure neighborhoods"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.configure_topology(i, j)   # ignore return value

    def configure_topology(self, i, j):
        """configure neighborhood for a given cell"""
            #   pylint: disable=multiple-statements
            #           reason: simple conditions

        cell = self[i, j]
        E = self[i, j+1]
        if E: cell["E"] = E
        N = self[i+1, j]
        if N: cell["N"] = N
        W = self[i, j-1]
        if W: cell["W"] = W
        S = self[i-1, j]
        if S: cell["S"] = S

        if (i+j)%2 is 0:
            NE = self[i+1, j+1]
            if NE: cell["NE"] = NE
            NW = self[i+1, j-1]
            if NW: cell["NW"] = NW
            SW = self[i-1, j-1]
            if SW: cell["SW"] = SW
            SE = self[i-1, j+1]
            if SE: cell["SE"] = SE

        if "wallAdder" in self.kwargs:
            for nbr in cell.each_neighbor():
                cell.makePassage(nbr, twoWay=False)

    def each_row(self):
        """iterate row by row"""
        for i in range(self.rows):
            L = []
            for j in range(self.cols):
                L.append(self[i, j])
            yield L

    def each_column(self):
        """iterate column by column"""
        for j in range(self.cols):
            L = []
            for i in range(self.rows):
                L.append(self[i, j])
            yield L

    def each_rowcol(self):
        """iterate by row and column (row major order)"""
        for i in range(self.rows):
            for j in range(self.cols):
                yield self[i, j]

    def each_colrow(self):
        """iterate by column and row (column major order)"""
        for j in range(self.cols):
            for i in range(self.rows):
                yield self[i, j]

# END: ortho_upsilon_grid.py
