# -*- coding: utf-8 -*-
# cell.py - cell class for mazes
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
#     15 May 2020 - Added topology management routines
#         These will provide hooks for masking routines...
#         Also, they avoid direct access of the cell topology dictionary...
"""
cell.py - basic cell implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

No assumptions are made here about the physical representation of the cell,
its passages or its walls.  Details of that sort are left for subclasses.

Definitions:

    A grid is a graph G=(C,E) consisting of a finite set C of cells and
    a set E of edges, where an edge is an unordered pair of distinct cells.
    In other words, a grid is a simple graph as loops and parallel edges are
    not admitted.

    A maze on a grid is a spanning subgraph of the grid.  In a maze, the
    the edge set of the grid is partitioned into two subsets, the walls and
    the passages.  The passages are edges in the spanning subgraph.

Variations and Generalizations:

    There a a number of variations on this theme and the terminology is
    by no means standardized.

    One generalization admits one-way passages.  (These are spanning
    subdigraphs H of the grid G.) Here the passages in the maze are the
    arcs that form the spanning subdigraph H.  By extension, the walls
    are the arcs in the relative complement G\\H.  Mazes used in the game
    Sokoban are mazes of this sort.

    Another generalization involves the placement of obstacles, some of
    which may be fixed in place and others moveable or removeable.
    Sokoban has obstacles of both sorts.  Text adventure games (like
    Cave or Zork™) are typically mazes with obstacles.

Implementations:

    Since the passages are generally more important than the walls, we
    maintain a list of passages that is separate from the list of
    neighbors.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs (Features?):

    1. When creating passages, no check is made to insure that the cell is
       a neighbor.
    2. One can easily create passages between cells which are not members
       of the same parent grid.
"""

class Cell(object):
    """base class for cells"""

    ID = -1                 # source for a unique identifier for the cell

    def __init__(self, index, **kwargs):
        """constructor

        Mandatory arguments:
            index - the cell's index in the parent grid

        Optional named arguments:
            name - a name for the cell
        """
            # unique identifier
        Cell.ID += 1
        self.id = Cell.ID

            # cell management
        self.index = index
        self.name = kwargs["name"] if "name" in kwargs \
            else "Cell[{x}]".format(x=self.id)
        self.kwargs = kwargs

            # grid management
            #     Example: cell1.topology["north"] = cell2
            # Better:
            #     cell1["north"] -> cell2 or None
            #     cell1["north"] = cell2

        self.topology = {}          # the neighborhood

            # maze management
        self.arcs = {}              # the passages in the neighborhood

            # topology management - added 15-05-2020
            # These should normally not be overridden, except for masking.

    def __getitem__(self, direction):
        """find the cell in a given direction"""
        if direction in self.topology:
            return self.topology[direction]
        return None

    def __setitem__(self, direction, nbr):
        """set the cell in given direction"""
        if nbr:
            self.topology[direction] = nbr
            return nbr
        del self.topology[direction]
        return None

    def each_neighbor(self):
        """traverse the neighborhood"""
        for direction in self.topology:
            nbr = self.topology[direction]
            if nbr:
                yield nbr

    def each_direction(self):
        """traverse the compass"""
        for direction in self.topology:
            yield direction

        # updating the instance

    def makePassage(self, cell, twoWay=True):
        """establish a passage to a given cell

        Arguments:
            cell - a cell, typically a neighbor
            twoWay (default=True) - if False, this is a one-way passage
        """
        self.arcs[cell] = True
        if twoWay:
            cell.makePassage(self, False)
        return self

    def erectWall(self, cell, twoWay=True):
        """establish a wall to a neighbor or remove a passage to a cell

        Arguments:
            cell - a cell, typically a neighbor
            twoWay (default=True) - if False, this is a one-way wall
        """
        if cell in self.arcs:
            del self.arcs[cell]
        if twoWay:
            cell.erectWall(self, twoWay=False)
        return self

        # status information

    def passages(self):
        """return a list of cells connected by passages"""
        return list(self.arcs)

    def walls(self):
        """return a list of cells connected by walls"""
        L = []
        for nbr in self.neighbors():
            if nbr not in self.arcs:
                L.append(nbr)
        return L

    def neighbors(self):
        """return a list of neighboring cells"""
            # use the topology management routines
        # return list(self.topology.values())
        L = []
        for nbr in self.each_neighbor():
            L.append(nbr)
        return L

    def have_passage(self, cell):
        """determine whether a given cell is connected by a passage"""
        return cell in self.arcs

    def status(self, direction):
        """determine what's in the given direction

        Returns True, False or None
            True if passage
            False if wall
            None if not a neighbor
        """
        # if direction in self.topology:
            # nbr = self.topology[direction]
        nbr = self[direction]
        if nbr:
            return self.have_passage(nbr)
        return None

# END: cell.py
