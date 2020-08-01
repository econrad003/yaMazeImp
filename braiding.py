# -*- coding: utf-8 -*-
##############################################################################
# braiding.py - braiding algorithms for mazes
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
#     29 Jul 2020 - EC - Initial version (sparsify)
#     30 Jul 2020 - EC - Directionally biased braiding
##############################################################################
"""
braiding.py - basic braiding implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Miscellaneous algorithms for dead-end removal.  Some or all of these
are homework problems in [1].  The algorithm implementations are:

    Braiding.sparsify:
        Create sparse mazes by deleting dead ends

    Braiding.straightener:
        Create braid mazes with longer straight passages by attempting to
        extend dead ends by building in the direction of flow.

    Braiding.twister:
        Create braid mazes with twisty circuits by attempting to extend
        dead ends by turning.

The static methods are support calls.  The class methods, listed above,
are the algorithm implementations.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    These are the known problems:

    1) Running sparsify on a rectangular grid will cause the each_rowcol
    and each_colrow methods to fail.

    2) The number of dead ends removed by method straightener may be more or
    less than expected.  Some dead ends along the sides cannot be removed
    by straightening while those in the interior can always be removed.  In 
    some cases, two neighboring dead ends may be removed in one operation.

    2) The number of dead ends removed by method twister will generally be 
    more than expected, up to a maximum of 100%.  In some cases, two 
    neighboring dead ends may be removed in one operation.  In a masked
    grid, the number might be less than expected, but in a normal rectangular
    grid, turns are always possible.  If right turns or left turns are used
    instead of general turns, some dead ends on the sides cannot be removed,
    making the situation more like method straightener.
"""

from random import random, shuffle, choice

class Braiding:
    """a collection of braiding algorithms"""

    @staticmethod
    def isolate(cell):
        """isolate a cell by remove its passages"""
        passages = cell.passages()
        for nbr in passages:
            cell.erectWall(nbr)     # clear the passage

    @classmethod
    def sparsify(cls, grid, bias=1.0):
        """braid a maze by clipping dead ends"""
        if bias <= 0:
            print("Braiding.sparsify: Nothing to do!")

        toclip = grid.dead_ends()   # cells to clip
        clipped = {}                # cells that have been clipped

            # step 1: remove passages into dead ends
        for cell in toclip:
            if bias >= 1 or random() < bias:
                cls.isolate(cell)
                clipped[cell] = 1

            # step 2: remove references to clipped cells
        for cell in grid.each():
            directions = list(cell.topology.keys())
            for direction in directions:
                if cell[direction] in clipped:
                    cell[direction] = None   # remove direction from cell

            # step 3: remove the cells from the grid
        for cell in clipped:
            index = cell.index
            del grid.cells[index]               # remove cell from grid

    @staticmethod
    def opposites():
        """create a default directory of opposite directions"""
        opps = {}
        opps["north"] = "south"
        opps["south"] = "north"
        opps["east"] = "west"
        opps["west"] = "east"
        return opps

    @staticmethod
    def straight_thru(cell, opposites):
        """make paths pass straight through the given cell"""
        directions = list(cell.topology.keys())
        n = 0
        for direction in directions:
            if direction not in opposites:
                continue                    # no opposite direction
            opposite = opposites[direction]
            if opposite not in directions:
                continue                    # no neighbor opposite
            nbr1 = cell[direction]
            nbr2 = cell[opposite]
            if cell.have_passage(nbr1) and not cell.have_passage(nbr2):
                cell.makePassage(nbr2)
                n += 1
        return n

    @classmethod
    def straightener(cls, grid, bias=1.0, opposites=None):
        """braiding by making straight paths"""
        if bias <= 0:
            print("Braiding.straightener: Nothing to do!")

        todo = list(grid.dead_ends())
        n = len(todo)                       # of dead ends
        m = int(n * bias)                   # number to remove
        if not opposites:
            opposites = Braiding.opposites()

        k = 0                              # number of known removals
        shuffle(todo)
        for cell in todo:
            if k >= m:                      # mission accomplished
                break
            if len(cell.arcs) is not 1:     # no longer a dead end
                k += 1
                continue

            k += Braiding.straight_thru(cell, opposites)

            # return n, m, k
            #   n - number of dead ends
            #   m - number to remove
            #   k - number actually removed
            #   p - actual probability of removal
        k = n - len(grid.dead_ends())
        p = k / n
        return n, m, k, p

    @staticmethod
    def turns():
        """create a default directory of turning directions"""
        bends = {}
        bends["north"] = ["east", "west"]
        bends["south"] = ["east", "west"]
        bends["east"] = ["north", "south"]
        bends["west"] = ["north", "south"]
        return bends

    @staticmethod
    def right_turns():
        """create a directory of right turn directions
        
        This can be used in Braiding.twister in lieu of arbitrary turns"""
        bends = {}
        bends["north"] = ["west"]
        bends["south"] = ["east"]
        bends["east"] = ["north"]
        bends["west"] = ["south"]
        return bends

    @staticmethod
    def left_turns():
        """create a directory of left turn directions
        
        This can be used in Braiding.twister in lieu of arbitrary turns"""
        bends = {}
        bends["south"] = ["west"]
        bends["north"] = ["east"]
        bends["west"] = ["north"]
        bends["east"] = ["south"]
        return bends

    @staticmethod
    def turn_out(cell, turns):
        """make paths turn to leave the given cell"""
        directions = list(cell.topology.keys())
        n = 0
        for direction in directions:
            if direction not in turns:
                continue                # no turning direction
            nbr1 = cell[direction]
            if not cell.have_passage(nbr1):
                continue                # not a source
            exits = []
            for turn in turns[direction]:
                if turn in directions:
                    nbr2 = cell[turn]
                    if cell.have_passage(nbr2):
                        exits = []
                        break           # already turning out
                    exits.append(nbr2)
            if not exits:
                continue                # no turns or already turning

                # we have one or more possibilities
            nbr2 = choice(exits)
            cell.makePassage(nbr2)
            n += 1
        return n

    @classmethod
    def twister(cls, grid, bias=1.0, turns=None):
        """braiding by making turning paths"""
        if bias <= 0:
            print("Braiding.straightener: Nothing to do!")

        todo = list(grid.dead_ends())
        n = len(todo)                       # of dead ends
        m = int(n * bias)                   # number to remove
        if not turns:
            turns = Braiding.turns()

        k = 0                              # number of known removals
        shuffle(todo)
        for cell in todo:
            if k >= m:                      # mission accomplished
                break
            if len(cell.arcs) is not 1:     # no longer a dead end
                k += 1
                continue

            k += Braiding.turn_out(cell, turns)

            # return n, m, k
            #   n - number of dead ends
            #   m - number to remove
            #   k - number actually removed
            #   p - actual probability of removal
        k = n - len(grid.dead_ends())
        p = k / n
        return n, m, k, p

# END: braiding.py
