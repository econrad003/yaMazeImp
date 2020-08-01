# -*- coding: utf-8 -*-
# weave_grid.py - grid class for rectangular weave mazes
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
#     29 Jul 2020 - Initial version
"""
weave_grid.py - rectangular weave grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A rectangular maze (or a square maze) is a maze with square cells that
tessellate a rectangle with sides parallel to the coordinate axes.

More information:

    see grid.py, cell.py and weave_cell.py for more information.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    The each_rowcol() and each_colrow() generators will not return
    undercells.
"""

from weave_cell import Overcell, Undercell, Simple_Overcell
from rectangular_grid import Rectangular_Grid

class Weave_Grid(Rectangular_Grid):
    """rectangular weave grid implementation"""

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
        inset = kwargs["inset"] if "inset" in kwargs else 0.15

        super().__init__(rows, cols, inset=inset, **kwargs)

    def initialize(self):
        """grid initialization, e.g. create cells
        
        Apart from the cell constructor call, this code should be
        identical with the code in Rectangular_Grid.initialize()"""
        h, k = self.origin
        for i in range(self.rows):
            for j in range(self.cols):
                x = self.scale * j + h
                y = self.scale * i + k
                name = "C[%d,%d]" % (i, j)      # added 30 Apr 2020
                    # the following line should be the only change!
                cell = Overcell(i, j, self, position=(x, y), \
                    scale=self.scale, inset=self.inset, name=name)
                self[i, j] = cell

    def tunnel_under(self, overcell):
        undercell = Undercell(overcell)
        i, j = overcell.index
        self[i, j, 1] = undercell

class Preweave_Grid(Weave_Grid):
    """rectangular weave grid with preconfigured weave"""

    def initialize(self):
        """grid initialization, e.g. create cells
        
        Apart from the cell constructor call, this code should be
        identical with the code in Weave_Grid.initialize()"""
        h, k = self.origin
        for i in range(self.rows):
            for j in range(self.cols):
                x = self.scale * j + h
                y = self.scale * i + k
                name = "C[%d,%d]" % (i, j)      # added 30 Apr 2020
                    # the following line should be the only change!
                cell = Simple_Overcell(i, j, self, position=(x, y), \
                    scale=self.scale, inset=self.inset, name=name)
                self[i, j] = cell

# END: weave_grid.py
