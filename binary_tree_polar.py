# -*- coding: utf-8 -*-
# binary_tree_polar.py - binary spanning tree algorithms for theta graphs
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
#     25 Jul 2020 - Initial version
"""
binary_tree_polar.py - binary spanning tree implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    We first identify a last cell in each latitude.
    We proceed along rows and columns counterclockwise, then inward.
    In a given cell, when there is a choice, we flip a coin.  If heads, 
    we carve a passage counterclockwise, and if tails, we inward.

    The order in which cells are actually processed is not important.
    Using a different underlying grid implementation, the cells could
    be processed asynchronously in parallel.

    Two versions are available here.  The first is a passage carver and
    the second is a wall builder.  The wall builder is slightly more
    efficient but requires more effort in grid configuration.

Prerequisites:

    This algorithm assumes theta (polar) grid topology.

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

class Binary_Tree_Polar:
    """implementation of the binary tree algorithm"""

    @classmethod
    def on(cls, grid, bias=0.5):
        """carve a binary spanning tree maze (passage carver)

        Preconditions:
            For a rectangular grid, the grid must be devoid of passages.

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random, randrange

            # mark an ending cell at each latitude
        lastcells = {}
        for i in range(grid.rows):
            n = len(grid.latitude[i])
            if n>1:
                lastcells[grid[i, randrange(n)]] = 1

            # now comes the coin flipping
        for cell in grid.each():
            nbrs = []
            if cell.status("ccw") is False:     # can tear down ccw wall
                if cell not in lastcells:
                    nbrs.append(cell["ccw"])
            if cell.status("inward") is False:  # can tear down inward wall
                nbrs.append(cell["inward"])

            if nbrs:                        # this is not the final central cell
                if len(nbrs) is 1:              # no choice
                    cell.makePassage(nbrs[0])
                else:                           # we have a choice
                        # flip a coin
                    index = 0 if random() < bias else 1
                    cell.makePassage(nbrs[index])

    @classmethod
    def wallBuilder_on(cls, grid, bias=0.5):
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
        from random import random, randrange

            # place an ending wall at each latitude
        for i in range(grid.rows):
            n = len(grid.latitude[i])
            if n>1:
                cell = grid[i, randrange(n)]
                cell.erectWall(cell["ccw"])

            # now comes the coin flipping
        for cell in grid.each():
                # pylint: disable=literal-comparison
                #     A constant named TWO would be just plain silly!
            nbrs = []
            if cell.status("ccw"):              # can erect ccw wall
                nbrs.append(cell["ccw"])
            if cell.status("inward"):           # can erect inward wall
                nbrs.append(cell["inward"])

            if len(nbrs) is 2:                  # we can block a passage
                    # flip a coin
                index = 0 if random() < bias else 1
                cell.erectWall(nbrs[index])

# END: binary_tree_polar.py
