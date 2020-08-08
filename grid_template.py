# -*- coding: utf-8 -*-
##############################################################################
# grid_template.py - grid template class for mazes
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
#     1 Aug 2020 - EC - Initial version
##############################################################################
"""
grid_template.py - grid template implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Provides methods for removing cells and grid connections.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from random import randint

class Grid_Template(object):
    """base class for grid templates"""

    def __init__(self, grid, **kwargs):
        """constructor"""
        self.grid = grid
        self.kwargs = kwargs
        self.log = []
        self.initialize()             # a hook for subclasses

    def initialize(self):
        """grid housekeeping or template initialization"""
            # does nothing in base class
        pass

        # surgical primitives
        #   - remove directed arcs from the grid
        #   - remove grid edges
        #   - remove cells from the grid
        #   - reinstate cell

    def remove_grid_arc(self, cell, thisaway, logging=True):
        """remove a directed arc from the grid"""
        nbr = cell[thisaway]
        if not nbr:
            return False            # nothing in this direction
        if cell.have_passage(nbr):
            return False            # the two cells are already linked
        cell[thisaway] = None

        if logging:
            self.log.append(["remove arc", cell.index, nbr.index])
        return True

    def remove_grid_edge(self, cell, thisaway, logging=True):
        """remove a grid edge from the grid"""
        nbr = cell[thisaway]
        stat = self.remove_grid_arc(cell, thisaway, logging=False)
        if not stat:
            return False            # the two cells are linked

            # look for a return arc
        thataway = None
        for direction in nbr.each_direction():
            if nbr[direction] is cell:
                thataway = direction
                break
        if thataway:
            self.remove_grid_arc(nbr, thataway, logging=False)

        if logging:
            log.append(["remove edge", cell.index, nbr.index])
        return True

    def remove_cell(self, cell, logging=True, backlinks=True):
        """remove a cell from the grid"""
        if cell.arcs:
            return False            # the cell has sinks

            # check for backlinks
        if backlinks:
            for item in self.grid.each():
                if item.have_passage(cell):
                    return False

            # remove all incident grid edges
        directions = list(cell.topology.keys())
        for direction in directions:
            self.remove_grid_edge(cell, direction, logging=False)

        del self.grid.cells[cell.index]

        if logging:
                # this maintains a reference to the "deleted" cell
            log.append(["remove cell", cell.index, cell])
        return True

    def reinstate_cell(self, cell, logging=True):
        """reinstate a cell
        
        This does not reinstate grid edges!"""
        self.grid[cell.index] = cell
        if logging:
            log.append(["reinstate cell", cell.index])
        return True

        # major surgery

    def vertical_wall(self, i0, m, j, sink=None,
                      logging=False):
        """create a hard vertical wall the east

        Parameters:
            rows i0 through m, inclusive
            column j
            sink:
                None - no door
                cell on west side - grid connection for door
        """
            # east wall
        for i in range(i0, m+1):
            cell = self.grid[i, j]
            if cell is not sink:
                self.remove_grid_edge(cell, "east", logging)

    def horizontal_wall(self, i, j0, n, sink=None,
                        logging=False):
        """create a hard horizontal wall to the north

        Parameters:
            row i
            columns i, j0
            sink:
                None - no door
                cell on south side - grid connection for door
        """
            # north wall
        for j in range(j0, n+1):
            cell = self.grid[i, j]
            if cell is not sink:
                self.remove_grid_edge(cell, "north", logging)

    def oriented_wall(self, start, direction, length, sink=None,
                      logging=False):
        y1, x1 = y0, x0 = start
        if direction == "south":
            y1 = y0 - length + 1
            self.vertical_wall(y1, y0, x0, sink, logging)
        elif direction == "east":
            x1 = x0 + length - 1
            self.horizontal_wall(y0, x0, x1, sink, logging)
        elif direction == "north":
            y1 = y0 + length - 1
            self.vertical_wall(y0, y1, x0, sink, logging)
        else:     # direction == "west"
            x1 = x0 - length + 1
            self.horizontal_wall(y0, x1, x0, sink, logging)
        # print("%sward wall from (%d,%d) to (%d,%d)" % (direction, y0, x0, y1, x1))
        return y1, x1

    def make_rooms(self, row_min, col_min, exits="RR",
                   lower_left=None, upper_right=None, logging=False):
        """partition the grid into rooms with exits

        This is essentially the recursive division algorithm.
        
        Parameters:
            exits:
                two-character string in R, H, M, L, N...
                the first character locates a vertical door in a horizontal
                wall, the second a horizontal door...
                    R (random) - choose access for door randomly
                    H (high) - access is rightmost or highest value
                    M (median) - middle value, truncated
                    L (low) - access is leftmost or lowest position
                    N (none) - no access point
        """

        if row_min < 3:
            row_min = 3
        if col_min < 3:
            col_min = 3
        (i0, j0) = lower_left if lower_left else (0, 0)
        (m, n) = upper_right if upper_right else \
            (self.grid.rows - 1, self.grid.cols - 1)
        exitv = exits[0]
        exith = exits[1]

        def partition_vertically(y0, x0, y1, x1):
            """do the partitioning"""
                # terminate?
            rows = y1 - y0 + 1
            if rows < row_min:
                return

            split = randint(y0, y1-1)     # split row
            exit = None
            if exitv != 'N':
                if exitv == 'H':
                    exit = self.grid[split, x1]
                elif exitv == 'M':
                    exit = self.grid[split, (x0 + x1) // 2]
                elif exitv == 'L':
                    exit = self.grid[split, x0]
                else:   # random
                    exit = self.grid[split, randint(x0, x1)]
            # e = str(exit.index) if exit else "None"
            # print("vertical: split=%d y∈[%d,%d] exit=%s" % (split, y0, y1, e))
            self.horizontal_wall(split, x0, x1, exit, logging)
            partition_horizontally(y0, x0, split, x1)
            partition_horizontally(split+1, x0, y1, x1)

        def partition_horizontally(y0, x0, y1, x1):
            """do the partitioning"""
                # terminate?
            cols = x1 - x0 + 1
            if cols < col_min:
                return

            split = randint(x0, x1-1)     # split column
            exit = None
            if exitv != 'N':
                if exitv == 'H':
                    exit = self.grid[y1, split]
                elif exitv == 'M':
                    exit = self.grid[(y0 + y1) // 2, split]
                elif exitv == 'L':
                    exit = self.grid[y0, split]
                else:   # random
                    exit = self.grid[randint(y0, y1), split]
            # e = str(exit.index) if exit else "None"
            # print("horizontal: split=%d x∈[%d,%d] exit=%s" % (split, x0, x1, e))
            self.vertical_wall(y0, y1, split, exit, logging)
            partition_vertically(y0, x0, y1, split)
            partition_vertically(y0, split+1, y1, x1)

        partition_vertically(i0, j0, m, n)

    def spiral(self, center, radius, orientation="ccw", logging=False):
        """make a square spiral"""
            # check space
        y0, x0 = center
        m, n = self.grid.rows-1, self.grid.cols-1
        if y0 < radius or m-y0 < radius:
            print("ERROR1: y0=%d, m=%d, radius=%d" % (y0, m, radius))
            return False
        if x0 < radius or n-x0 < radius:
            print("ERROR2: x0=%d, n=%d, radius=%d" % (x0, n, radius))
            return False

            # orientation
        next_direction = {}
        adjustments = {}
        start = {}
        if orientation == "ccw":
            next_direction["south"] = "east"
            adjustments["south"] = [-1, 1]
            start["south"] = (y0, x0-1)
            next_direction["east"] = "north"
            adjustments["east"] = [1, 0]
            start["east"] = (y0-1, x0+1)
            next_direction["north"] = "west"
            start["north"] = (y0+1, x0)
            next_direction["west"] = "south"
            start["west"] = (y0, x0-1)
            adjustments["west"] = [0, -1]
        else:
            next_direction["north"] = "east"
            adjustments["north"] = [0, 1]
            start["north"] = (y0+1, x0-1)
            next_direction["west"] = "north"
            adjustments["west"] = [1, -1]
            start["west"] = (y0-1, x0-1)
            next_direction["south"] = "west"
            start["south"] = (y0, x0)
            next_direction["east"] = "south"
            adjustments["south"] = [-1, 0]
            start["east"] = (y0, x0+1)

        for start_direction in ["south", "east", "north", "west"]:
            direction = start_direction[:]
            y0, x0 = start[direction]
            if direction == "south":
                y0 -= 1
            P = (y0, x0)
            sink = None
            for length in range(1, 2*radius-1, 2):
                y0, x0 = self.oriented_wall(P, direction, length, \
                    sink, logging)
                k, h = adjustments[direction] \
                    if direction in adjustments else (0,0)
                P = (y0+k, x0+h)
                direction = next_direction[direction]
        return True

# END: grid_template.py
