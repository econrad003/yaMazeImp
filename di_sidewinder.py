# -*- coding: utf-8 -*-
# di_sidewinder.py - direct sidewinder algorithm
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
#     16 Sep 2020 - Initial version
"""
di_sidewinder.py - directed binary maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm notes:

    This is the sidewinder algorithm given in Chapters 2 of the Jamis
    Buck book adapted to produce one-way connections.  As in the
    directed binary tree algorithm, the terminus for E/N sidewinder
    is the cell in the northeastermost position.
    
      N.B: For E/N binary tree, any cell in the north row or east
      column could easily be taken as the terminus.  For E/N
      sidewinder, any cell in the north row could be easily be used.
      With some additional work any cell at all could be treated as 
      the terminus in either algorithm.
    
    For an ordinary E/N binary tree maze, to reach the NE cell from any
    given cell, simply go either north or east at every turn.  The
    terminus is the only cell where you can do neither.  In E/N
    sidewinder, some cells may offer a choice of going north or east.
    In these cells choose north.
    
      N.B.: E/N binary tree is a symmetric algorithm in the sense that
      E/N binary tree and N/E binary tree have the same range of trees.
      Sidewinder breaks that symmetry.

    To create a N/E sidewinder tree in a 4-connected rectangular grid:

        For each cell in the grid:
            if there are neigbors to the north and east:
                flip a coin to choose north or east:
                if the choice is north:
                    choose a random cell in the current eastward run
                    carve a passage northward from that choice
                else:
                    carve a passage eastward from the cell
            else if there is a neighbor to the east:
                carve a passage between the cell and its east neighbor
            else if there is a neighbor to the north:
                carve a passage between the cell and its north neighbor.

    There are two directed versions of the algorithm.  They differ in that
    one is towards the NE cell and the other is away from the NE cell.

    The order in which cells are actually processed is important --
    cells in a row must be processed in order from west to east.  

Additional notes:

    If both the towards and away versions of the algorithm be run on
    the same grid in the same pair of direction, then from any cell
    there will be a directed path from the cell to the terminus and
    also a directed path from the terminus to the cell.

Prerequisites:

    This algorithm depends on grid topology. As written, it is only
    guaranteed to work on rectangular grids with the usual 4-neighbor
    (N-E-S-W) topology.

    The algorithm works on rectangular grids.  With fiddling and some
    compromise, it can be made to work with polar grids and masked
    grids, and with non-planar topologies such as cylinders, Moebius 
    strips, tori and Klein bottles.

Parallelization:

    The algorithm could (in principle!) be run in parallel with a separate
    process for each row.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs and Features:

    See discussion above.
"""

from random import random, choice

class Directed_Sidewinder:
    """implementation of the directed binary tree algorithm"""

    class State(object):
        """a state matrix to allow customization of the alorithm"""

        def __init__(self, grid, towards=True,
                     directions=["east", "north"], bias=0.5):
            """constructor

            Mandatory arguments:
                grid - a grid on which carve a maze

            Optional arguments:
                towards - if False, carving will be away from
                    terminus; if True (default), towards the
                    terminus.
                directions - a pair of carving directions:
                    [forward, upward] (default: [east, north])
                bias - go forward probability (default=50%)
            """
            self.grid = grid
            self.towards = towards
            assert len(directions) == 2
            self.forward = directions[0]
            self.upward = directions[1]
            self.bias = bias
            self.termini = []         # ideally there should be exactly one
            self.fwdrun = []
            self.stat = 0

        def carve(self, cell, nbr):
            """carve the required arc"""
            if self.towards:
                cell.makePassage(nbr, twoWay=False)
            else:
                nbr.makePassage(cell, twoWay=False)

        def first_in_row(self, row):
            """find the first cell in a row

            This depends on the forward direction.
            """
            if self.forward == "east":
                cell = self.grid[row, 0]
            elif self.forward == "north":
                cell = self.grid[self.grid.rows -1, row]
            elif self.forward == "west":
                cell = self.grid[row, self.grid.cols -1, row]
            elif self.forward == "south":
                cell = self.grid[0, row]
            else:
                cell = None
            assert cell
            return cell

        def row_range(self):
            """return a generator for the rows"""
            if self.forward in {"east", "west"}:
                return range(self.grid.rows)
            if self.forward in {"north", "south"}:
                return range(self.grid.cols)
            assert False

        def last_in_row(self, cell):
            """is this the last cell in the processing row?"""
            if not cell:
                return True

        def close_out_run(self):
            """pick an upward cell"""
            if self.fwdrun:
                cell, upw = choice(self.fwdrun)
                self.carve(cell, upw)
            self.fwdrun = []

        def choose(self, cell):
            """choose the direction and carve an arc"""
            fwd = None if self.last_in_row(cell) else cell[self.forward]
            upw = cell[self.upward]
            if upw:
                self.fwdrun.append([cell, upw])

                # for debugging
#            s = str(cell.index) + ": "
#            if fwd: s += "E>" + str(fwd.index)
#            if upw: s += "N>" + str(upw.index)
#            s += " run " + str(len(self.fwdrun))
#            print(s)

            if fwd:
                if upw:
                        # both neighbors exist, so choose the way
                    flip = random()
                    if flip <= self.bias:
                        self.carve(cell, fwd)
                    else:
                        self.close_out_run()
                else:
                        # no upward neighbor
                    self.carve(cell, fwd)
            else:
                if upw:
                        # no forward neighbor
                    self.close_out_run()
                else:
                        # terminus
                    self.termini.append(cell)

        def run(self):
            """one pass of the algorithm"""
            d = "toward" if self.towards else "away"
            print("Directed sidewinder:")
            print("\t%s terminus" % d)
            print("\tdirections %s and %s" % (self.forward, self.upward))
            for row in self.row_range():
                cell = self.first_in_row(row)
                while not self.last_in_row(cell):
                    self.choose(cell)
                    cell = cell[self.forward]

        def run_both_ways(self):
            """two-way run"""
            self.run()
            self.towards = not self.towards
            self.termini = []
            self.run()
            print("Done!")

    @classmethod
    def on(cls, grid, state=None, towards="both", bias=0.5):
        """carve a directed binary tree maze (passage carver)

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            state - a state matrix
            towards - one of "towards", "away" or "both" (default: both);
                the first letter suffices
            bias - coin fairness changer
        """
        if not state:
            state = cls.State(grid)

        state.bias = 0.5
        state.towards = towards[0] not in {'a', 'A'}
        if towards[0] in {'b', 'B'}:
            state.run_both_ways()
        else:
            state.run()
        if len(state.termini) is 0:
            print("Topology warning: no terminus cell")
        elif len(state.termini) > 1:
            print("Topology warning: more than one terminus")
        else:
            print("Success!")
        state.stat = len(state.termini) - 1
        return state

# END: di_binary_tree.py
