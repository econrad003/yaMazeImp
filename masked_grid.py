# -*- coding: utf-8 -*-
##############################################################################
# mask_grid.py - masked grid class
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
#     20 May 2020 - Initial version
##############################################################################
"""
masked_grid.py - masked grid implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

This differs considerably from the implementation described in Buck [1].
In particular, this implementation is intended to handle arbitrary grid
topologies.

Suggested Usage:

    1) To create a masked grid, use the following import:
          from masked_grid import Mask, Masked_Grid
    2) Then create a grid and a mask:
          grid = Grid_Subclass(args)
          mask = Mask()
    3) Enable most of the cells:
          mask[index1] = True; mask[index2] = True; ...
    4) Then create a masked grid:
          mgrid = Masked_Grid(grid, mask)
    5) Run a maze creation algorithm on the masked grid:
          Fubar.on(mgrid, bias=0.25)  # passage carvers work best
    6) Print the maze:
          print(grid.unicode())   # original grid

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from cell import Cell
from grid import Grid

class Mask(object):
    """a dictionary of masked cells"""

    def __init__(self):
        """constructor"""
        self.enabled = {}

    def __getitem__(self, index):
        """determine whether a given index is masked"""
        return index in self.enabled

    def __setitem__(self, index, enabled):
        """mask or unmask an index"""
        if enabled:
            self.enabled[index] = True
            return True
        if index in self.self.enabled:
            del self.enabled[index]
        return False

    def __len__(self):
        """return the number of masked cells"""
        return len(self.enabled)

class Mask_Cell(Cell):
    """cell class for masked grids"""

    def __init__(self, index, owner):
        """constructor"""
        super().__init__(index)
        self.owner = owner
        self.grid = self.owner.grid
        self.twin = self.grid[index]
        
    def makePassage(self, cell, twoWay=True):
        """establish a passage to a given cell

        We reflect the change in the twin as well.

        Arguments:
            cell - a cell, typically a neighbor
            twoWay (default=True) - if False, this is a one-way passage
        """
        self.arcs[cell] = True
        if twoWay:
            cell.arcs[self] = True

        self.twin.makePassage(cell.twin, twoWay)
        return self

    def erectWall(self, cell, twoWay=True):
        """establish a wall to a neighbor or remove a passage to a cell

        We reflect the change in the twin as well.

        Arguments:
            cell - a cell, typically a neighbor
            twoWay (default=True) - if False, this is a one-way wall
        """
        if cell in self.arcs:
            del self.arcs[cell]
        if twoWay and self in cell.arcs:
            del cell.arcs[self]

        self.twin.erectWall(cell.twin, twoWay)
        return self

class Masked_Grid(Grid):
    """masked grid class"""

    def __init__(self, grid, mask):
        """constructor"""
        self.grid = grid
        self.mask = mask
        super().__init__()

    def is_enabled(self, twin):
        """determine if the twin cell is enabled"""
        return self.mask[twin.index]

    def initialize(self):
        """grid initialization, e.g. create cells"""
        for twin in self.grid.each():
            if self.is_enabled(twin):
                cell = Mask_Cell(twin.index, self)
                self[twin.index] = cell

    def configure(self):
        """grid configuration"""
        for cell in self.each():
                # mirror the neighborhood
            twin = cell.twin
            for direction in twin.each_direction():
                cousin = twin[direction]
                if self.is_enabled(cousin):
                    cell[direction] = self[cousin.index]
                # mirror the passages
            linked = twin.passages()
            for cousin in linked:
                if self.is_enabled(cousin):
                    nbr = self[cousin.index]
                    cell.arcs[nbr] = True

def make_mask(pathname, debug=False):
    from rectangular_grid import Rectangular_Grid

    mask = Mask()
    if debug:
        print('make_mask: Creating mask from "' + pathname + '"...')
    n = 0
    lines = []
    with open(pathname) as fp:
        for line in fp:
            if len(line) < 2:
                continue
            if line[0] == "#":
                if debug:
                    print(line[:-1])
                continue
            lines.append(line[:-1])
            n2 = len(line) - 1
            n = max(n, n2)
    lines.reverse()
    m = len(lines)
    for i in range(m):
        line = lines[i]
        n2 = len(line)
        if n2 < n:
            line += ' ' * (n-n2)
        for j in range(n):
                if line[j] not in ['x', 'X']:
                    mask[i, j] = True

    if debug:
        print('Mask: m=%d, n=%d, enabled=%d' % (m, n, len(mask)))
        print('Grid: creating rectangular grid')
    if m * n is 0:
        raise ValueError('m=%d, n=%d: empty grid' % (m, n))
    grid = Rectangular_Grid(m, n)

    if debug:
        print('Masked_Grid: creating masked grid')
    masked = Masked_Grid(grid, mask)

    if debug:
        print('make_mask: complete')
    return grid, masked

# END: masked_grid.py
