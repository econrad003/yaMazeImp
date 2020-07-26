# -*- coding: utf-8 -*-
#######################################################################
# inwinder.py - a spanning tree algorithm for theta grids
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
#######################################################################
# Maintenance History:
#     15 Jul 2020 - Initial version
#######################################################################
"""
inwinder.py - a spanning tree algorithm for theta grids
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    The algorithm is a modification of the sidewinder algorithm for
    rectangular grids.  We proceed inward and counterclockwise.

    Initially, at each latitude, we randomly choose a starting cell.
    Then, working counterclockwise, cell by cell, in the given latitude,
    we flip a coin.  If the current cell is not the final cell in the
    range and the coin says heads, we continue counterclockwise.  Otherwise
    we select one of the cells in the current counterclockwise run and
    carve a passage inward.

    Two versions are available here.  The first is a passage carver and
    the second is a wall builder.  The wall builder is slightly more
    efficient but requires more effort in grid configuration.

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

class Inwinder:
    """implementation of the sidewinder algorithm adapted to theta mazes"""

    @classmethod
    def on(cls, grid, bias=0.5):
        """carve a perfect theta maze using inwinder (passage carver)

        Mandatory arguments:
            grid - a theta grid

        Optional named arguments:
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random, choice, randrange

        for i in range(grid.rows):
            n = len(grid.latitude[i])           # number of cells in the ring
            s = randrange(n)                    # starting cell in the ring
            if i is 0:                          # polar ring
                    # carve a passage (not a circuit) around the polar ring
                for j in range(n-1):
                    cell = grid[i, (s+j)%n]
                    nbr = cell['ccw']
                    cell.makePassage(nbr)
                continue

                # not the polar ring
            run = []
            for j in range(n):
                cell = grid[i, (s+j)%n]
                run.append(cell)
                if j < n-1 and random() < bias:
                        # head: proceed counterclockwise
                    nbr = cell['ccw']
                    cell.makePassage(nbr)
                else:
                        # tail: close out run by carving a passage inward
                    cell = choice(run)
                    nbr = cell['inward']
                    cell.makePassage(nbr)
                    run = []

    @classmethod
    def wallBuilder_on(cls, grid, bias=0.5):
        """carve a spanning tree maze using sidewinder (wall builder)

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            bias (default is 50%) - the percentage of heads in the coin flip
                This is a float, so 50% is 0.5, 75% is 0.75, etc.
        """
        from random import random, choice, randrange

        for i in range(grid.rows):
            n = len(grid.latitude[i])           # number of cells in the ring
            s = randrange(n)                    # starting cell in the ring
            if n > 0:                           # polar ring
                    # leave a passage (but not a circuit) around the polar ring
                cell = grid[i, s]
                nbr = cell['cw']
                cell.erectwall(nbr)

                # not the polar ring
            run = []
            for j in range(n):
                cell = grid[i, (s+j)%n]
                run.append(cell)
                if j < n-1 and random() < bias:
                        # head: proceed counterclockwise
                    pass
                else:
                        # tail: close out run by carving a passage inward
                    nbr = cell['ccw']
                    cell.erectWall(nbr)

                    cell = choice(run)
                    for member in run:
                        if member is not cell:
                            nbr = member['inward']
                            member.makePassage(nbr)
                    run = []

# END: inwinder.py
