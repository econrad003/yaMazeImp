# -*- coding: utf-8 -*-
# weave_cell.py - cell classes for rectangular weave mazes
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
#     1 Aug 2020 - Add Simple_Overcell
"""
weave_cell.py - cell implementation for rectangular weave mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Description:

    Standard square cells are (obviously) square in shape.  In
    addition, their sides are parallel to the coordinate axes.  In a 
    weave maze, an undercell lies under a given cell (which we call 
    its parent) and satisfies several constraints:

    (1) Two level construction:

        An undercell cannot lie under another undercell.  (Weave mazes
        have just two levels, the ground level containing the basic 
        cells and the underground level consisting of undercells.)

    (2) Short straight tunnel construction:

        An undercell is in the interior of a single three-cell path
        (called a tunnel) connecting exactly two neighbors of its
        parent cell, either a vertical tunnel connecting the parent's
        north and the south neighbors, or a horizontal tunnel
        connecting the parent's east and the west neighbors.  Neither
        of these neighbors is linked to the parent cell.

        This is a strong condition as it rejects tunnels consisting
        of more than three cells.

    (3) Bridge/tunnel construction:

        (a) A passage may not come to a dead end over or under another
        passage.

        (b) A tunnel under a cell must be perpendicular to the passage
        through the cell.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    1. Parameters are not validated.
"""

from square_cell import Square_Cell

class Overcell(Square_Cell):
    """ground level cell implementation for rectangular weave mazes"""

    def __init__(self, row, col, grid, **kwargs):
        """constructor

        Mandatory arguments:
            row, col - the cell's row and column in the parent grid

        Optional named arguments:
            name - a name for the cell
            position - (x, y)-position of the center of the cell;
              the default position is (col, row)
            scale - larger than 0 - a scaling factor; the default is 1
            inset - a value in (0,1) - the default is 0.15
        """
            # initialize the parent class
        if "inset" not in kwargs:
            kwargs["inset"] = 0.15
        super().__init__(row, col, **kwargs)
        self.grid = grid

    def neighbors(self):
        """return a list of neighboring cells"""
        L = super().neighbors()
        if self.can_tunnel_south():
            L.append(self["south"]["south"])
        if self.can_tunnel_east():
            L.append(self["east"]["east"])
        if self.can_tunnel_north():
            L.append(self["north"]["north"])
        if self.can_tunnel_west():
            L.append(self["west"]["west"])
        return L

    def each_neighbor(self):
        for direction in self.topology:
            nbr = self.topology[direction]
            if nbr:
                yield nbr
        if self.can_tunnel_south():
            yield self["south"]["south"]
        if self.can_tunnel_east():
            yield self["east"]["east"]
        if self.can_tunnel_north():
            yield self["north"]["north"]
        if self.can_tunnel_west():
            yield self["west"]["west"]

    def can_tunnel_south(self):
        """check tunneling"""
        south = self["south"]
                # is there a southern neighbor?
        if not south:
            return False
                # does this neighbor have a neighbor to the south?
        if not south["south"]:
            return False
                # is there a horizontal passage to tunnel under?
        return south.is_horizontal_thru()

    def can_tunnel_north(self):
        """check tunneling"""
        north = self["north"]
                # is there a northern neighbor?
        if not north:
            return False
                # does this neighbor have a neighbor to the north?
        if not north["north"]:
            return False
                # is there a horizontal passage to tunnel under?
        return north.is_horizontal_thru()

    def can_tunnel_east(self):
        """check tunneling"""
        east = self["east"]
                # is there an eastern neighbor?
        if not east:
            return False
                # does this neighbor have a neighbor to the east?
        if not east["east"]:
            return False
                # is there a vertical passage to tunnel under?
        return east.is_vertical_thru()

    def can_tunnel_west(self):
        """check tunneling"""
        west = self["west"]
                # is there an eastern neighbor?
        if not west:
            return False
                # does this neighbor have a neighbor to the west?
        if not west["west"]:
            return False
                # is there a horizontal passage to tunnel under?
        return west.is_vertical_thru()

    def is_vertical_thru(self):
        """do we have a vertical 3-passage?"""
        return self.have_passage(self["north"]) \
            and self.have_passage(self["south"]) \
            and not self.have_passage(self["east"]) \
            and not self.have_passage(self["west"])

    def is_horizontal_thru(self):
        """do we have a horizontal 3-passage?"""
        return self.have_passage(self["east"]) \
            and self.have_passage(self["west"]) \
            and not self.have_passage(self["north"]) \
            and not self.have_passage(self["south"])

    def makePassage(self, nbr, twoWay=True):
        """establish a passage to a given cell"""
        if self["north"] and self["north"] is nbr["south"]:
            platform = self["north"]
        elif self["south"] and self["south"] is nbr["north"]:
            platform = self["south"]
        elif self["east"] and self["east"] is nbr["west"]:
            platform = self["east"]
        elif self["west"] and self["west"] is nbr["east"]:
            platform = self["west"]
        else:
            platform = None
        if platform:
            self.grid.tunnel_under(platform)
        else:
                #    ----- NOTE -----
                # we make the links directly to avoid issues with 
                # calling makePassage twice via super() when twoWay
                # is True.
            self.arcs[nbr] = True
            if twoWay:
                nbr.arcs[self] = True

class Simple_Overcell(Overcell):
    """for preconfigured weaving with Kruskal's algorithm"""

    def neighbors(self):
        """return a list of neighboring cells"""
        L = []
        for direction in self.topology:
            nbr = self.topology[direction]
            if nbr:
                L.append(nbr)
        return L

    def each_neighbor(self):
        for direction in self.topology:
            nbr = self.topology[direction]
            if nbr:
                yield nbr

class Undercell(Square_Cell):
    """underground cell implementation for rectangular weave mazes"""

    def __init__(self, parent, **kwargs):
        """constructor

        Mandatory arguments:
            row, col - the cell's row and column in the parent grid

        Optional named arguments:
            name - a name for the cell
            position - (x, y)-position of the center of the cell;
              the default position is (col, row)
            scale - larger than 0 - a scaling factor; the default is 1
            inset - a value in (0,1) - the default is 0.15
        """
            # initialize the cell
        if "inset" not in kwargs:
            kwargs["inset"] = 0.15
        kwargs["underCell"] = 1
        row, col = parent.index
        super().__init__(row, col, **kwargs)
        self.index = parent

            # create the tunnel
        if parent.is_horizontal_thru():
                # adjust pointers to the northern neighbor and link
            self["north"] = parent["north"]
            self["north"]["south"] = self
            parent["north"] = None
            self.makePassage(self["north"])
                # adjust pointers to the southern neighbor and link
            self["south"] = parent["south"]
            self["south"]["north"] = self
            parent["south"] = None
            self.makePassage(self["south"])
        else:
                # adjust pointers to the eastern neighbor and link
            self["east"] = parent["east"]
            self["east"]["west"] = self
            parent["east"] = None
            self.makePassage(self["east"])
                # adjust pointers to the western neighbor and link
            self["west"] = parent["west"]
            self["west"]["east"] = self
            parent["west"] = None
            self.makePassage(self["west"])

    def is_vertical_thru(self):
        """do we have a vertical 3-passage"""
        return self["north"] or self["south"]

    def is_horizontal_thru(self):
        """do we have a horizontal 3-passage"""
        return self["east"] or self["west"]

# END: weave_cell.py
