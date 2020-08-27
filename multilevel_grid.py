# -*- coding: utf-8 -*-
##############################################################################
# multilevel_grid.py - grid class for multilevel mazes
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
##############################################################################
# Maintenance History:
#     14 Aug 2020 - EC - Initial version
# Credits:
#     EC - Eric Conrad
##############################################################################
"""
multilevel_grid.py - multi_level grid implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown
"""

from stairwell_cell import Stairwell_Cell
from grid import Grid
from rectangular_grid import Rectangular_Grid

class Multilevel_Grid(Grid):
    """a class for multi-level mazes"""

    def initialize(self):
        """grid initialization"""
        self.levels = []      # a list of grids starting at ground level
        self.levelOf = {}     # the level number of a grid
        self.stairs = {}      # the stairwells

    def add_level(self, rows, cols, **kwargs):
        """build a new level by adding a rectangular grid"""
        grid = Rectangular_Grid(rows, cols, **kwargs)
        self.add_grid(grid)
        return grid

    def add_grid(self, grid):
        """build a new level by adding a grid"""

            # add the grid to the grid array
        assert grid not in self.levelOf, \
            "the grid is already part of the maze"
        level = len(self.levels)
        self.levelOf[grid] = level
        self.levels.append(grid)

            # add the grid's cells to the cell array
        for cell in grid.each():
            index = (level, cell.index, "floor")
            self[index] = cell

    def add_stairs_upward(self, level, downcell, link=False):
        """build a stairwell up from the indicated cell"""

            # consistency checks
        index1 = downcell.index
        grid1 = self.levels[level]
        assert downcell is grid1[index1], \
            "Cell %s is not in level %d." % (str(index1), level)
        grid2 = self.levels[level+1]
        upcell = grid2[index1]
        assert upcell, \
            "There is no cell %s in level %d" % (str(index1), level+1)

        index2 = (downcell, upcell, "stairs")
        self[index2] = stairs = Stairwell_Cell(index2, downcell, upcell)
        self.stairs[stairs] = level

            # link the stairwell (default is not to link)
        if link:
            stairs.makePassage(downcell)
            stairs.makePassage(upcell)

# END: multilevel_grid.py
