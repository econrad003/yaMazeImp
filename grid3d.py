# -*- coding: utf-8 -*-
# grid3d.py - grid class for three-dimensional oblong mazes
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
#     1 Sep 2020 - Initial version
"""
grid3d.py - three-dimensional oblong grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A rectangular 3D maze (or a cubic maze or an oblong 3D maze) is a maze
with cubic cells that tessellate a rectangular parallopiped with sides
parallel to the coordinate axes.

More information:

    see grid.py and cell.py for more information.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from cell3d import Cell3D
from grid import Grid

class Grid3D(Grid):
    """three-dimensional oblong grid implementation"""

    def __init__(self, rows, cols, height, **kwargs):
        """constructor

        Mandatory arguments:
            rows - the number of rows in the grid
            cols - the number of columns in the grid
            height - the number of levels or height of the grid

        Optional named arguments:
            name - a name for the cell
            origin - default (0,0) - the (x,y)-coordinates of the center
                of the lower left cell in the x-y plane;
                translation only affects x and y coordinates
            scale - default 1 - the length of the side of a cell
            inset - default 0 - the inset of a cell
            content - default ' ' - for ASCII and Unicode
            bgcolor - default None - for PNG
            wallAdder - if present (ignoring value), will add passages
            topology - connectedness of planes parallel to the x-y plane
                4 - N/S/E/W
                6 - N/S/E/W/NE/SW
                8 - N/S/E/W/NE/NW/SE/SW
        """
            # grid management
        self.rows = rows
        self.cols = cols
        self.height = height
        self.levels =[]         # levels (e.g. [[z=0], [z=1], [z=2]])
        self.origin = kwargs["origin"] if "origin" in kwargs \
            else (0, 0)
        self.scale = kwargs["scale"] if "scale" in kwargs else 1
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

        if "topology" not in kwargs:
            kwargs["topology"] = 8

        super().__init__(**kwargs)

    def initialize(self, higher=[]):
        """grid initialization, e.g. create cells

        Parameters:
            higher - higher dimensional coordinates

        Example:
            grid4d.initialize(self, higher=[]):
                for k in range(self.hyperlevels):
                    level = higher[:]
                    level.insert(0, k)
                    super().initialize(level)
        """
        for k in range(self.height):
            level = higher[:]         # make a copy!
            level.insert(0, k)        # list [z, w, v, ...]
            # print("level %s" % str(level))
            self.levels.append(level) # add the level to the directory
            self.initialize_level(level)

    def initialize_level(self, level):
        """grid plane initialization"""
        h1, h2 = self.origin
        for i in range(self.rows):
            for j in range(self.cols):
                x = self.scale * j + h1
                y = self.scale * i + h2
                name = "Cell-%d-%d" % (i, j)
                assert len(level) == 1    # Cell3D shouldn't change this!
                for z in level:
                    name += "-%d" % z
                cell = Cell3D(i, j, level, position=(x, y), \
                    scale=self.scale, inset=self.inset, \
                    name=name)
                self[cell.index] = cell

    def configure(self):
        """grid configuration, e.g. configure neighborhoods"""
        for cell in self.each():
            self.configure_topology(cell)

    @staticmethod
    def from_cell(cell):
        """unpack relevant cell coordinates"""
        index = list(cell.index)
        i, j, k = index[0:3]
        rest = index[3:]
        return [i, j, k, rest]

    def to_cell(self, i, j, k, rest, debug=False):
        """pack cell coordinates"""
        index = tuple([i, j, k] + rest)
        return self[index]

    def configure_topology(self, cell):
        """configure neighborhood for a given cell"""
        i, j, k, rest = self.from_cell(cell)

            # the 4-neighborhood
        north = self.to_cell(i+1, j, k, rest, True)
        if north: cell["north"] = north

        south = self.to_cell(i-1, j, k, rest)
        if south: cell["south"] = south

        east = self.to_cell(i, j+1, k, rest)
        if east: cell["east"] = east

        west = self.to_cell(i, j-1, k, rest)
        if west: cell["west"] = west

            # the 6-neighborhood
        northeast = None
        if self.kwargs["topology"] > 4:
            northeast = self.to_cell(i+1, j+1, k, rest)
            if northeast: cell["northeast"] = northeast
            southwest = self.to_cell(i-1, j-1, k, rest)
            if southwest: cell["southwest"] = southwest

            # the 8-neighborhood
        northwest = None
        if self.kwargs["topology"] > 6:
            northwest = self.to_cell(i+1, j-1, k, rest)
            if northwest: cell["northwest"] = northwest
            southeast = self.to_cell(i-1, j+1, k, rest)
            if southeast: cell["southeast"] = southeast

            # the vertical neighborhood
        up = self.to_cell(i, j, k+1, rest)
        if up: cell["up"] = up

        down = self.to_cell(i, j, k-1, rest)
        if down: cell["down"] = down

        if "wallAdder" in self.kwargs:
            if north: cell.makePassage(north)
            if east: cell.makePassage(east)
            if northeast: cell.makePassage(northeast)
            if northwest: cell.makePassage(northwest)
            if up: cell.makePassage(up)

        return cell

            # iteration (generally one level plane at a time)
            #
            # by a level plane, I mean a plane that is parallel to the
            # x-y coordinate plane -- coordinates other than x and y
            # (such as z in 3-d) do not change in a level plane

    def each_row(self, level):
        """iterate row by row within a level"""
        k, rest = level[0], level[1:]
        for i in range(self.rows):
            L = []
            for j in range(self.cols):
                L.append(self.to_cell(i, j, k, rest))
            yield L

    def each_column(self, level):
        """iterate column by column within a level"""
        k, rest = level[0], level[1:]
        for j in range(self.cols):
            L = []
            for i in range(self.rows):
                L.append(self.to_cell(i, j, k, rest))
            yield L

    def each_rowcol(self, level):
        """iterate in row major order within a level"""
        k, rest = level[0], level[1:]
        for i in range(self.rows):
            for j in range(self.cols):
                yield self.to_cell(i, j, k, rest)

    def each_colrow(self, level):
        """iterate in column major order within a level"""
        k, rest = level[0], level[1:]
        for j in range(self.cols):
            for i in range(self.rows):
                yield self.to_cell(i, j, k, rest)

            # and this gives us a way to move among the
            # level planes

    def each_level(self):
        """iterate through the set of levels"""
        for level in self.levels:
            yield level


            # display of mazes

    # (1) convert to ini configuration

    # (2) use ini configuration to produce inform-7 code

# END: grid3d.py
