# -*- coding: utf-8 -*-
# di_binary_tree.py - direct binary maze algorithm
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
#     13 Sep 2020 - Initial version
#     13 Sep 2020 - Customize to set a random terminus
"""
di_binary_tree.py - directed binary maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm notes:

    This is essentially the binary tree algorithm given in Chapters 1
    and 2 of the Jamis Buck book with one important distinction.  To
    make the distinction, we first need to identify a cell which we'll
    call the terminus.  In a rectangular maze, it will be the meeting
    cell of the long passage row and the long passage column.  For
    binary tree mazes built eastward and northward, this long passages
    will be the northernmost row and the easternmost column, and the
    terminus will be the northeast corner.  In a north-east binary tree
    maze, from any cell, it is very easy to find the terminus:

        While you can go either east or north:
            if you can go east, do so, otherwise go north.
        The cell you have reached is the terminus.

    To create a north-east binary tree in a 4-connected rectangular grid:

        For each cell in the grid:
            if there are neigbors to the north and east:
                flip a coin to choose north or east:
                carve a passage between the cell to the chosen neighbor
            else if there is a neighbor to the east:
                carve a passage between the cell and its east neighbor
            else if there is a neighbor to the north:
                carve a passage between the cell and its north neighbor.

    There are two directed versions of the algorithm.  They differ in that
    one is towards the terminus and the other is away from the terminus.
    The towards version reads like this: 

        For each cell in the grid:
            if there are neigbors to the north and east:
                flip a coin to choose north or east:
                carve an arc from the cell to the chosen neighbor
            else if there is a neighbor to the east:
                carve an arc from the cell going east
            else if there is a neighbor to the north:
                carve an arc from the cell going north.

    The away version reads like this:
    
        For each cell in the grid:
            if there are neigbors to the north and east:
                flip a coin to choose north or east:
                carve an arc from the chosen neighbor to the cell
            else if there is a neighbor to the east:
                carve an arc from the neighbor going west
            else if there is a neighbor to the north:
                carve an arc from the neighbor going south.

    The order in which cells are actually processed is not important.
    Using a different underlying grid implementation, the cells could
    be processed asynchronously in parallel.

Additional notes:

    If both the towards and away versions of the algorithm be run on
    the same grid in the same pair of direction, then from any cell
    there will be a directed path from the cell to the terminus and
    also a directed path from the terminus to the cell.

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

from random import random

class Directed_Binary_Tree:
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
            self.stat = 0

        def carve(self, cell, nbr):
            """carve the required arc"""
            if self.towards:
                cell.makePassage(nbr, twoWay=False)
            else:
                nbr.makePassage(cell, twoWay=False)

        def choose(self, cell):
            """choose the direction and carve an arc"""
            fwd = cell[self.forward]
            upw = cell[self.upward]
            if fwd:
                if upw:
                        # both neighbors exist, so choose the way
                    flip = random()
                    if flip <= self.bias:
                        self.carve(cell, fwd)
                    else:
                        self.carve(cell, upw)
                else:
                        # no upward neighbor
                    self.carve(cell, fwd)
            else:
                if upw:
                        # no forward neighbor
                    self.carve(cell, upw)
                else:
                        # terminus
                    self.termini.append(cell)

        def fixup(self):
            """subclass tweaking can be done here"""
            pass

        def run(self):
            """one pass of the algorithm"""
            for cell in self.grid.each():
                self.choose(cell)
            self.fixup()                # a hook for subclasses

        def run_both_ways(self):
            """two-way run"""
            print("\tPass 1...")
            self.run()
            self.towards = not self.towards
            self.termini = []
            print("\tPass 2...")
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
            print("\tRunning...")
            state.run()
        if len(state.termini) is 0:
            print("Topology warning: no terminus cell")
        elif len(state.termini) > 1:
            print("Topology warning: more than one terminus")
        else:
            print("Success!")
        state.stat = len(state.termini) - 1
        return state

class Set_Terminus_State(Directed_Binary_Tree.State):
    """A custom version of the algorithm to set any terminus"""

    def __init__(self, grid, terminus, towards=True,
                 directions=["east", "north"], bias=0.5):
        """constructor

        Mandatory arguments:
            grid - a grid on which carve a maze

        Optional arguments:
            towards - if False, carving will be away from terminus; 
                if True (default), towards the terminus.
            directions - a pair of carving directions:
                [forward, upward] (default: [east, north])
            bias - go forward probability (default=50%)
        """
        super().__init__(grid, towards, directions, bias)

        self.arcs = {}                  # a list of arcs
        self.terminus = terminus        # the desired terminus
        self.stat = 0

    def carve(self, cell, nbr):
        """pretend to carve the required arc

        The actual passage carving happens later.  For the moment
        we direct movement towards the upforwardmost corner.
        """
        self.arcs[cell] = nbr

    def fixup(self):
        """This is where the actual carving happens"""
        print("\tCarving...")
        backarcs = {}                   # the arcs
        if len(self.termini):
                # have an up/forward corner cell
                #
                # The backarcs will form a path from terminus to corner
            curr = self.terminus
            while curr and curr in self.arcs:
                next = self.arcs[curr]
                if next:
                    backarcs[(curr, next)] = 1
                curr = next
        for cell in self.arcs:
            source = cell
            sink = self.arcs[cell]
            if (source, sink) in backarcs:
                source, sink = sink, source
            if not self.towards:
                source, sink = sink, source
            source.makePassage(sink, twoWay=False)

# END: di_binary_tree.py
