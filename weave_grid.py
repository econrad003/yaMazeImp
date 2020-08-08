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
#     1 Aug 2020 - Corrected handling of default inset
#     2 Aug 2020 - Added long_tunnel method to Preweave class
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

from weave_cell import Overcell, Undercell, \
    Simple_Overcell, Simple_Undercell
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
        if "inset" not in kwargs:               # 1 Aug 2020
            kwargs["inset"] = 0.15

        super().__init__(rows, cols, **kwargs)

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

    def add_long_tunnel(self, start, direction, length):
        """construct a long tunnel

        Parameters:
            start - a cell to start from
            direction - the direction to tunnel
            length - the number of undercells to use

        Returns:
            s, L, last where:
                s - empty string on success else failure reason
                L - empty list if the tunnel is not feasible
                  - a list of undercells, if the tunnel is constructed
                last - the cell where the tunnel would end (or None)
        """
        length = int(length)
        if length < 2:
            return "Length must be at least 2", [], None

            # Feasibility study
            # Step 1 - walk in the tunnel direction...
        s = "Step 1 - not enough cells %s of start" % direction
        L = []        # the cells that the tunnel will go under
        last = start[direction]
        for i in range(length):
            L.append(last)
            if not last:
                return s, [], None
            last = last[direction]
        if not last:
            return s, [], None
            #   At this point we have the needed cells.
            # Step 2 - check that we haven't already built here
        s = "Step 2 - an existing passage blocks this tunnel"
        path = [start] + L + [last]
        for i in range(length + 1):
            cell = path[i]
            nbr = path[i+1]
            if cell.have_passage(nbr):
                return s, [], None
            #   The path is clear.
            # Step 3 - check that tunnel construction does not isolate
            #   any cell
        def would_isolate_if(cell, tunnel_nbrs):
            for nbr in cell.neighbors():
                if nbr not in tunnel_nbrs:
                    return False
            return True

        s = "Step 3 - the tunnel would isolate a cell"
        if would_isolate_if(start, {start[direction]}):
            return s, [], None
        if would_isolate_if(last, {L[-1]}):
            return s, [], None
        for i in range(1, length):
            cell = path[i]
            nbrs = {path[i-1], path[i+1]}
            if would_isolate_if(cell, nbrs):
                return s, [], None

            # ok to build
        L = self._build_tunnel(path)
        return "", L, last

    def _build_tunnel(self, path):
        """private function - construct a long tunnel"""
        first = path[0]
        last = path[-1]
        interior = path[1:-1]
        length = len(interior)
        L = []

            # build the undercells
        for cell in interior:
            undercell = Simple_Undercell(cell)
            row, col = cell.index
            self[row, col, 1] = undercell
            L.append(undercell)

            # connect the tunnel
        newpath = [first] + L + [last]
        for i in range(length+1):
            cell = newpath[i]
            nbr = newpath[i+1]
            cell.makePassage(nbr)

            # correct the grid topology
        for direction in first.topology:
            if first[direction] is interior[0]:
                first[direction] = L[0]
        for direction in last.topology:
            if last[direction] is interior[-1]:
                last[direction] = L[-1]
        for i in range(length):
            overcell = interior[i]
            undercell = L[i]
            adjustments = []
            for direction in overcell.topology:
                if overcell[direction] is path[i]:
                    adjustments.append([direction, i])
                if overcell[direction] is path[i+2]:
                    adjustments.append([direction, i+2])
            for direction, j in adjustments:
                del overcell.topology[direction]
                undercell[direction] = newpath[j]
        return L

# END: weave_grid.py
