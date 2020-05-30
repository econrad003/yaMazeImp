# -*- coding: utf-8 -*-
##############################################################################
# grid.py - grid class for mazes
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
#     21 Apr 2020 - EC - Initial version
#     23 Apr 2020 - EC - Add return value to __setitem__
# Credits:
#     EC - Eric Conrad
##############################################################################
"""
grid.py - basic grid implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

No assumptions are made here about the physical representation of the maze,
its passages or its walls, or the underlying grid.  Details of that sort are
left for subclasses.

Definitions:

    A grid is a graph G=(C,E) consisting of a finite set C of cells and
    a set E of edges, where an edge is an unordered pair of distinct cells.
    In other words, a grid is a simple graph as loops and parallel edges are
    not admitted.

    A maze on a grid is a spanning subgraph of the grid.  In a maze, the
    the edge set of the grid is partitioned into two subsets, the walls and
    the passages.  The passages are edges in the spanning subgraph.

Variations:

    See the documentation of cell.py for generalizations.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    1. The __getitem__ and __setitem__ functions are quite crude and subject
       to misuse.
    2. The choice function returns None if no cells have been indexed.
"""

class Grid(object):
    """base class for grids"""

    ID = -1                 # source for a unique identifier for the grid

    def __init__(self, **kwargs):
        """constructor

        Optional named arguments:
            name - a name for the cell
        """
            # unique identifier
        Grid.ID += 1
        self.id = Grid.ID

            # grid management
        self.name = kwargs["name"] if "name" in kwargs \
            else "Maze[{x}]".format(x=self.id)
        self.kwargs = kwargs
        self.cells = {}

        self.initialize()             # a hook for subclasses
        self.configure()              # another hook for subclasses

    def initialize(self):
        """grid initialization, e.g. create cells"""
        pass

    def configure(self):
        """grid configuration, e.g. configure neighborhoods"""
        pass

    def __getitem__(self, index):
        """return the cell associated with the given index"""
        if index in self.cells:
            return self.cells[index]      # return the cell
        return None                   # no such cell

    def __setitem__(self, index, cell):
        """"associate the cell with the given index"""
        self.cells[index] = cell
        return cell

    def choice(self):
        """return a cell at random"""
        from random import choice
        index = choice(list(self.cells)) if self.cells else None
        return self[index]

    def __len__(self):
        """return the number of indexed cells"""
        return len(self.cells)

        # generators

    def each(self):
        """iterate over the cells"""
        for index in self.cells:
            yield self.cells[index]

        # special methods

    def inject_method(self, f):
        """inject a method into a grid

        Parameters:
            f - a method to insert
                f must take at least one parameter
        """
        from types import MethodType

        return MethodType(f, self)

# END: grid.py
