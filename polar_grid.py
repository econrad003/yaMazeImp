# -*- coding: utf-8 -*-
# polar_grid.py - grid class for polar mazes
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
#     1 Jun 2020 - Initial version
#     25 Jul 2020 - spruce up with pylint3
"""
polar_grid.py - polar grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A polar maze is a maze with cells arranged inside a disk and around the
center (or pole).  Except for a degenerate cell at the pole or a disk of
degenerate cells having a vertex at the pole, each cell is bounded outside
by a pair of latitude arcs and a pair of longitude lines.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

# from math import sin, cos, pi
from math import pi
from polar_cell import Polar_Cell
from grid import Grid

class Polar_Grid(Grid):
    """polar grid implementation"""

    def __init__(self, rows, **kwargs):
        """constructor

        Mandatory arguments:
            rows - the number of rows in the grid

        Optional named arguments:
            name - a name for the cell
            origin - default (0,0) - the (x,y)-coordinates of the center
                of the lower left cell
            scale - default 1 - the length of the side of a cell
                the sides are bounded by latitude line
            inset - default 0 - the inset of a cell
            poleCells - default 1
                If poleCells > 1, then the there will be poleCells cells all
              sharing a vertex at the pole.  Otherwise there will be a single
              cell which has the pole at its center.
            splitAt - default 1
                If the arc length of the outer wall of a cell is greater
              than splitAt, then the cell will have at least 2 outer
              neighbors, each having an inward wall length of at most
              splitAt
            wallAdder - if present (ignoring value), will add passages
        """
            # grid management
        self.params = {}
        self.latitude = {}              # cells sorted by latitude
        for i in range(rows):
            self.latitude[i] = []
        self.rows = rows

        self.params["poleCells"] = kwargs["poleCells"] \
            if "poleCells" in kwargs else 1

        self.params["splitAt"] = kwargs["splitAt"] \
            if "splitAt" in kwargs else 1
        if self.params["splitAt"] < 0.5:
            raise ValueError("SplitAt parameter is too small.")

        self.origin = kwargs["origin"] if "origin" in kwargs else (0, 0)
        self.scale = kwargs["scale"] if "scale" in kwargs else 1
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

        super().__init__(**kwargs)

    def create_pole_cell(self, splitAt):
        """create a cell centered at the pole - for initialize"""
        celltype = ['circle', 1]

            # the only walls are outward
        directions = []
        outwards = int(2 * pi / splitAt)
        if outwards < 1:
            outwards = 1
        if self.rows is 1:
            outwards = 0
        for i in range(outwards):
            directions.append("outward%d" % i)

        index = (0, 0)
        self[index] = Polar_Cell(index, directions, outwards, celltype)
        self.latitude[0].append(self[index])
        return outwards

    def create_cells_at_pole(self, n, splitAt):
        """create n cells at the pole - for initialize"""
            # two longitudinal walls plus the outward walls
        directions = ['ccw', 'cw']
        outC = 4 * pi       # outer circumference of next shell
        outwards = int((outC / splitAt) / n)
        if outwards < 1:
            outwards = 1
        if self.rows is 1:
            outwards = 0

        for k in range(outwards):
            directions.append("outward%d" % k)

        for j in range(n):
            celltype = ['wedge', 1, j/n, (j+1)/n]
            index = (0, j)
            self[index] = Polar_Cell(index, directions, outwards, celltype)
            self.latitude[0].append(self[index])
        return outwards

    def create_outer_cells(self, i, n, splitAt):
        """create n cells at latitude i - for initialize"""
            # two longitudinal walls plus inward wall plus the outward walls
        directions = ['ccw', 'cw', 'inward']
        outC = (i+2) * 2 * pi       # outer circumference of next shell
        outwards = int((outC / splitAt) / n)
        if outwards < 1:
            outwards = 1
        if i+1 is self.rows:
            outwards = 0
        for k in range(outwards):
            directions.append("outward%d" % k)

        # uncomment for debugging
#        print("level %d, %d cells, next level times %d (c=%f)" % (i, n, outwards, outC))

        for j in range(n):
            celltype = ['sector', i, i+1, j/n, (j+1)/n]
            index = (i, j)
            self[index] = Polar_Cell(index, directions, outwards, celltype)
            self.latitude[i].append(self[index])
        return outwards

    def initialize(self):
        """grid initialization, e.g. create cells"""
        poleCells = self.params["poleCells"]
        splitAt = self.params["splitAt"]
        if poleCells < 2:
            poleCells = 1
            outwards = self.create_pole_cell(splitAt)
        else:
            outwards = self.create_cells_at_pole(poleCells, splitAt)

        n = poleCells * outwards
        self.outwards = [outwards]
        for i in range(1, self.rows):
            outwards = self.create_outer_cells(i, n, splitAt)
            n *= outwards
            self.outwards.append(outwards)

    def configure(self):
        """grid configuration, e.g. configure neighborhoods"""
        for i in range(self.rows):
            cols = len(self.latitude[i])
            for j in range(cols):
                self.configure_topology(i, j, self.rows, cols)

    def configure_topology(self, i, j, rows, cols):
        """configure neighborhood for a given cell"""
        cell = self[i, j]

        if cols > 1:
            cell['ccw'] = self[i, (j+1)%cols]
            cell['cw'] = self[i, (j-1)%cols]
            if "wallAdder" in self.kwargs:
                cell.makePassage(cell['ccw'])
        if i+1 < rows:
            for k in range(cell.outwards):
                nbr = self[i+1, j*cell.outwards + k]
                nbr['inward'] = cell
                cell['outward%d' % k] = nbr
                if "wallAdder" in self.kwargs:
                    cell.makePassage(cell['outward%d' % k])
        return cell

        # Ordered iteration is by longitude (column) within latitude (row).
        # This is latitude-major ordering.
        # Since the number of cells in a given longitude range varies
        #   by latitude, we only support latitude-major (i.e. row-major)
        #   iteration.

    def each_row(self):
        """iterate row by row"""
        for i in range(self.rows):
            yield self.latitude[i][:]

    def each_rowcol(self):
        """iterate by row and column (row major order)"""
        for i in range(self.rows):
            cols = len(self.latitude[i])
            for j in range(cols):
                yield self[i, j]

# END: polar_grid.py
