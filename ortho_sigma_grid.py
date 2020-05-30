# -*- coding: utf-8 -*-
# ortho_sigma_grid.py - grid class for rectangular sigma mazes
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
#     28 May 2020 - Initial version
"""
ortho_sigma_grid.py - rectangular sigma grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A rectangular sigma maze is a maze with regular hexagonal cells that
form an approximate rectangle with sides parallel to the coordinate
axes. The even rows are indented.  Cells have six directions: F (N),
FL, BL, B (S), BR, FR.

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
from math import cos, sin, pi


class Sigma_Cell(Polygonal_Cell):
    """hexagonal cell"""
    labels = ['FR', 'F', 'FL', 'BL', 'B', 'BR']
    vectors = [(cos(i*pi/3), sin(i*pi/3)) for i in range(6)]
    radius = 1
    apothem = sin(pi/3)

    def __init__(self, origin, scale, index, **kwargs):
        """create a hexagonal cell"""
        i, j = index
            # determine the cell's center
        sep = Sigma_Cell.radius * 1.5 * scale
        h, k = origin
        x0 = h + 2 * j * sep
        if i % 2 is 1:
            x0 += sep             # indented row
        y0 = k + i * Sigma_Cell.apothem * scale
            # determine the cells vertices
        polygon = []
        for i in range(6):
            h, k = Sigma_Cell.vectors[i]
            polygon.append((x0+h, y0+k))
        
        super().__init__(index, Sigma_Cell.labels, polygon, **kwargs)

class Ortho_Sigma_Grid(Grid):
    """rectangular delta grid implementation"""

    def __init__(self, rows, cols, **kwargs):
        """constructor

        Mandatory arguments:
            rows - the number of rows in the grid
            cols - the number of columns in the grid

            Each lattice point indexes a cell in the shape of a regular
            hexagon.  The hexagons in odd rows are set off-center.

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

    def initialize(self):
        """grid initialization, e.g. create cells"""
        for i in range(self.rows):
            for j in range(self.cols):
                index = (i, j)
                name = 'C[%d,%d]' % index
                self[index] = Sigma_Cell(self.origin, self.scale, index,
                                         name=name)

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
        F = self[i+2, j]
        B = self[i-2, j]
        if i % 2 is 0:                          # even rows
            FR = self[i+1, j]
            FL = self[i+1, j-1]
            BL = self[i-1, j-1]
            BR = self[i-1, j]
        else:                                   # odd rows (indented)
            FR = self[i+1, j+1]
            FL = self[i+1, j]
            BL = self[i-1, j]
            BR = self[i-1, j+1]

        if F: cell['F'] = F                 # Forward/up/north
        if B: cell['B'] = B                 # Backward/down/south
        if FR: cell['FR'] = FR              # Forward right (roughly ENE-NE)
        if FL: cell['FL'] = FL              # Forward left (roughly NW-WNW)
        if BR: cell['BR'] = BR              # Backward right (roughly SE-ESE)
        if BL: cell['BL'] = BL              # Backward left (roughly WSW-SW)

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

# END: ortho_sigma_grid.py
