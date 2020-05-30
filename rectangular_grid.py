# -*- coding: utf-8 -*-
# rectangular_grid.py - grid class for rectangular mazes
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
#     21 Apr 2020 - Initial version
#     30 Apr 2020 - Reconfigure name parameter as "C[i,j]"
#     15 May 2020 - Use cell topology management methods.
"""
rectangular_grid.py - rectangular grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A rectangular maze (or a square maze) is a maze with square cells that
tessellate a rectangle with sides parallel to the coordinate axes.

More information:

    see grid.py and cell.py for more information.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from square_cell import Square_Cell
from grid import Grid

class Rectangular_Grid(Grid):
    """rectangular grid implementation"""

    def __init__(self, rows, cols, **kwargs):
        """constructor

        Mandatory arguments:
            rows - the number of rows in the grid
            cols - the number of columns in the grid

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
        h, k = self.origin
        for i in range(self.rows):
            for j in range(self.cols):
                x = self.scale * j + h
                y = self.scale * i + k
                name = "C[%d,%d]" % (i, j)      # added 30 Apr 2020
                cell = Square_Cell(i, j, position=(x, y), scale=self.scale,
                                   inset=self.inset, name=name)
                self[i, j] = cell

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

        north = self[i+1, j]
        if north: cell["north"] = north         # 15-05-2020
        south = self[i-1, j]
        if south: cell["south"] = south         # 15-05-2020

        east = self[i, j+1]
        if east: cell["east"] = east            # 15-05-2020
        west = self[i, j-1]
        if west: cell["west"] = west            # 15-05-2020

        if "wallAdder" in self.kwargs:
            if north: cell.makePassage(north)
            if east: cell.makePassage(east)

        return cell

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

        # display of mazes

    def __str__(self):
        """cast to string"""

        def get_content(cell):
            """get the content string of a cell"""
                #   pylint: disable=multiple-statements
                #           reason: simple conditions or short consequences
            if "content" not in cell.kwargs: return ' '
            content = str(cell.kwargs["content"])
            if not content: return ' '
            return content[0]

        s = ""
        for i in range(self.rows - 1, -1, -1):    # north to south
                # top
            for j in range(self.cols):
                cell = self[i, j]
                if cell.status("north"):
                    s += "+   "
                else:
                    s += "+---"
            s += "+\n"                            # close out top
                # middle
            for j in range(self.cols):
                cell = self[i, j]
                if cell.status("west"):
                    s += "  " + get_content(cell) + " "
                else:
                    s += "| " + get_content(cell) + " "
            cell = self[i, self.cols-1]               # close out middle
            if cell.status("east"):
                s += " \n"                            # non-planar embeddings
            else:
                s += "|\n"

            # and finally, the bottom of row 0
        for j in range(self.cols):
            cell = self[0, j]
            if cell.status("south"):
                s += "+   "                       # non-planar embeddings
            else:
                s += "+---"
        s += "+"
        return s

    def unicode(self):
        """cast to unicode"""

        def get_content(cell):
            """get the content string of a cell"""
                #   pylint: disable=multiple-statements
                #           reason: simple conditions or short consequences
            if "content" not in cell.kwargs: return ' '
            content = str(cell.kwargs["content"])
            if not content: return ' '
            return content[0]

        s = ""
        for i in range(self.rows - 1, -1, -1):    # north to south
                # top
            corner = "\u250f" if i + 1 == self.rows else "\u2523"
            for j in range(self.cols):
                s += corner
                corner = "\u2533" if i + 1 == self.rows else "\u254b"
                cell = self[i, j]
                if cell.status("north"):
                    s += "   "                        # non-planar embeddings
                else:
                    s += "\u2501" * 3
            corner = "\u2513" if i + 1 == self.rows else "\u252b"
            s += corner + "\n"                        # close out top
                # middle
            for j in range(self.cols):
                cell = self[i, j]
                if cell.status("west"):
                    s += "  " + get_content(cell) + " "
                else:
                    s += "\u2503 " + get_content(cell) + " "
            cell = self[i, self.cols-1]               # close out middle
            if cell.status("east"):
                s += " \n"                            # non-planar embeddings
            else:
                s += "\u2503\n"

            # and finally, the bottom of row 0
        corner = "\u2517"
        for j in range(self.cols):
            s += corner
            corner = "\u253b"
            cell = self[0, j]
            if cell.status("south"):
                s += "   "                            # non-planar embeddings
            else:
                s += "\u2501" * 3
        s += "\u251b"
        return s

# END: rectangular_grid.py
