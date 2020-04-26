# -*- coding: utf-8 -*-
# sidewinder.py - a spanning tree algorithm
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
#     22 Apr 2020 - Initial version
"""
sidewinder.py - a spanning tree implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    The algorithm is a modification of the binary tree algorithm for
    rectangular grids.

    We proceed along rows and columns in a fixed directions (defaults:
    respectively northward and eastward).  In a given cell, when there is
    a choice, we flip a coin.  If heads, we carve a passage forward
    (e.g. eastward) to extend a run, and if tails, we close out the
    forward run and carve a passage upward (e.g. northward) from a random
    cell in the run.

    The order in which cells are actually processed is important.  Within
    a given row, cells must be processed in order.  With changes in
    implementation, the rows could be be processed asynchronously in parallel.

    Two versions are available here.  The first is a passage carver and
    the second is a wall builder.  The wall builder is slightly more
    efficient but requires more effort in grid configuration.

    If the prerequisites are met, the result will be a spanning tree of
    passages.  This tree will not in general be a binary tree as some
    cells may be passage-adjacent to four neighbors.

Prerequisites:

    This algorithm depends on grid topology. As written, it is only
    guaranteed to work on rectangular grids with the usual 4-neighbor
    (N-E-S-W) topology.

    The algorithm works on rectangular grids.  With some fiddling, it can be
    made to work with polar grids and masked grids, and with non-planar
    topologies such as cylinders, Moebius strips, tori and Klein bottles.

Parallelization:

    The algorithm could (in principle!) be run in parallel with each row of
    cells running asynchronously in its own process.  The underlying grid
    and cell structures would require considerable modification.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs and Features:

    See discussion above.
"""

class Sidewinder:
    """implementation of the sidewinder algorithm"""

    GENERATOR = None

    @classmethod
    def fetch_generator(cls, grid, forward, upward):
        if Sidewinder.GENERATOR:
            return Sidewinder.GENERATOR
        config = [forward, upward]
        if forward == "east":
            return grid.each_rowcol
        if forward == "north":
            return grid.each_colrow
        assert False, "Sidewinder: No generator for config = %s" % str(config)

    @classmethod
    def store_generator(cls, generator):
        Sidewinder.GENERATOR = generator

    @classmethod
    def on(cls, grid, forward="east", upward="north", bias=0.5):
        """carve a spanning tree maze using sidewinder (passage carver)

        Preconditions:
            For a rectangular grid, the grid must be devoid of passages.

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            each - a row/column generator compatible with the given directions
                if None, the directions will try to pick a generator
            forward (default is eastward) - a direction
            upward (default is northward) - an independent direction
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random, choice

        each = Sidewinder.fetch_generator(grid, forward, upward)
        run = []
        for cell in each():
            if cell.status(upward) is False:    # can tear down upward wall
                run.append([cell, cell.topology[upward]])

            nbr = cell.topology[forward] if cell.status(forward) is False \
                else None                       # can tear down forward wall

            if nbr:                         # can go forward
                if run:                         # can go upward
                        # we have a choice: flip a coin
                    if random() < bias:
                        cell.makePassage(nbr)
                    else:
                            # close out run
                        cell1, cell2 = choice(run)
                        cell1.makePassage(cell2)
                        run = []
                else:                           # can only go forward
                    cell.makePassage(nbr)
            elif run:                       # can only go upward
                    # close out run
                cell1, cell2 = choice(run)
                cell1.makePassage(cell2)
                run = []
        Sidewinder.GENERATOR = None         # clean up

    @classmethod
    def wallBuilder_on(cls, grid, each=None, forward="east",
                       upward="north", bias=0.5):
        """carve a spanning tree maze using sidewinder (wall builder)

        Preconditions:
            For a rectangular grid, the grid should be devoid of walls.

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            each - a row/column generator compatible with the directions
                if None, the directions will try to pick a generator
            forward (default is eastward) - a direction
            upward (default is northward) - an independent direction
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random, randrange

        each = Sidewinder.fetch_generator(grid, forward, upward)
        run = []
        for cell in each():
            if cell.status(upward):         # can erect upward wall
                run.append([cell, cell.topology[upward]])

            nbr = cell.topology[forward] if cell.status(forward) \
                else None                       # can erect forward wall

            if nbr:                         # can go forward
                if run:                         # can go upward
                        # we have a choice: flip a coin
                    if random() > bias:
                            # close out run
                        cell.erectWall(nbr)
                        n = randrange(len(run))
                        run.pop(n)
                        for cell1, cell2 in run:
                            cell1.erectWall(cell2)
                        run = []
            elif run:                       # can only go upward
                            # close out run
                n = randrange(len(run))
                run.pop(n)
                for cell1, cell2 in run:
                    cell1.erectWall(cell2)
                run = []
        Sidewinder.GENERATOR = None         # clean up

# END: sidewinder.py
