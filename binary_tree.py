# -*- coding: utf-8 -*-
# binary_tree.py - binary spanning tree algorithms
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
#     15 May 2020 - Use new cell topology management routines...
"""
binary_tree.py - binary spanning tree implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    We proceed along rows and columns in a fixed directions (defaults:
    respectively northward and eastward).  In a given cell, when there is
    a choice, we flip a coin.  If heads, we carve a passage forward
    (e.g. eastward), and if tails, we carve a passage upward (e.g. northward).

    The order in which cells are actually processed is not important.
    Using a different underlying grid implementation, the cells could
    be processed asynchronously in parallel.

    Two versions are available here.  The first is a passage carver and
    the second is a wall builder.  The wall builder is slightly more
    efficient but requires more effort in grid configuration.

    If prerequsites are met, the algorithm produces a binary spanning
    tree of passages.  A given cell is passage-adjacent to at most three
    neighbors in the tree as either the forward neighbor or the upward
    neighbor will be blocked by a wall.

Prerequisites:

    This algorithm depends on grid topology. As written, it is only
    guaranteed to work on rectangular grids with the usual 4-neighbor
    (N-E-S-W) topology.

    The algorithm works on rectangular grids.  With some fiddling, it can be
    made to work with polar grids and masked grids, and with non-planar
    topologies such as cylinders, Moebius strips, tori and Klein bottles.

Parallelization:

    The algorithm could (in principle!) be run in parallel with each cell
    running asynchronously in its own process.  The underlying grid and cell
    structures would require considerable modification.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs and Features:

    See discussion above.
"""

class Binary_Tree:
    """implementation of the binary tree algorithm"""

    @classmethod
    def on(cls, grid, forward="east", upward="north", bias=0.5):
        """carve a binary spanning tree maze (passage carver)

        Preconditions:
            For a rectangular grid, the grid must be devoid of passages.

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            forward (default is eastward) - a direction
            upward (default is northward) - an independent direction
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random

        for cell in grid.each():
            nbrs = []
            if cell.status(forward) is False:   # can tear down forward wall
                nbrs.append(cell[forward])            # 15-05-2020
            if cell.status(upward) is False:    # can tear down upward wall
                nbrs.append(cell[upward])             # 15-05-2020

            if nbrs:                        # this is not a terminal cell
                if len(nbrs) is 1:              # no choice
                    cell.makePassage(nbrs[0])
                else:                           # we have a choice
                        # flip a coin
                    index = 0 if random() < bias else 1
                    cell.makePassage(nbrs[index])

    @classmethod
    def wallBuilder_on(cls, grid, forward="east", upward="north", bias=0.5):
        """create a binary spanning tree maze by building walls

        Preconditions:
            For a rectangular grid, the grid should be devoid of walls.

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            forward (default is eastward) - a direction
            upward (default is northward) - an independent direction
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random

        for cell in grid.each():
                # pylint: disable=literal-comparison
                #     A constant named TWO would be just plain silly!
            nbrs = []
            if cell.status(forward):            # can erect forward wall
                nbrs.append(cell[forward])          # 15-05-2020
            if cell.status(upward):             # can erect upward wall
                nbrs.append(cell[upward])           # 15-05-2020

            if len(nbrs) is 2:                  # we can block a passage
                    # flip a coin
                index = 0 if random() < bias else 1
                cell.erectWall(nbrs[index])

# END: binary_tree.py
