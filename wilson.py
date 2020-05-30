# -*- coding: utf-8 -*-
# wilson.py - Wilsons algorithm
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
#     10 May 2020 - Initial version
"""
wilson.py - Wilson's algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Wilson's Algorithm:

    We perform a "circuit-erased" random walk of the entire grid.  We start
    by marking a single cell as visited. Subsequently, we pick a random
    unvisited cell and, via a random walk, we attempt to find a simple path 
    starting from the selected cell, passing through unvisited cells, and
    ending in a visited cell.  In the course of the walk, we may encounter
    a cell $v$ already in the path.  (The effect is a simple circuit $C$
    starting at cell $v$.)  We delete the path $C\\v$ from the walk and
    continue the walk from cell $v$.  (This is "erasure" of the circuit.)

    In [1], simple circuits are called "loops".  In graph theory, a loop
    typically refers to a simple circuit consisting of a single cell.

Prerequisites:

    This algorithm works on any connected grid.  With a bad random sequence,
    it might never terminate.

Remarks:

    Given a true uniform random number generator, this algorithm is
    unbiased in the sense that every spanning tree is generated with equal
    probability.  (Of course the pseudorandom number generator used here
    is not truly random.)

    According to [1], the algorithm was developed by David Bruce Wilson
    (Microsoft; University of Washington).

Comparison with Aldous/Broder:

    Wilson's Algorithm tends to start slowly with the walks tending to
    cross themselves to create circuits before finding their ways to visited 
    cells.  This leads to time-expensive circuit erasures.  As more cells are
    visited, the circuit erasures become less likely, so the algorithm tends
    to end fairly quickly. Note that with as few as two unvisited neighboring
    cells, circuit erasures can still occur.  If the unvisited subgrid
    consists entirely of isolated cells, circuit erasures will no longer
    occur.  

    The analysis of the walk in Aldous/Broder in progress can be viewed as
    akin to randomly painting an entire canvas with a single extended stroke
    of a wide brush.  As we proceed further to extend the painted portion of
    the canvas, it will tend to be harder to avoid painted parts.

    Wilson's algorithm tends to start slowly and end quickly while both
    versions of Aldous/Broder tend to start quickly and end slowly.

Also:

    From a homework problem in [1], we consider a hybrid of the first entrance
    algorithm (Aldous/Broder) and Wilson's algorithm.  It is not clear that
    this will [in principle] guarantee a uniformly random spanning tree.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    See discussion above.
"""

class Wilson:
    """implementation of Wilson's algorithm and a hybrid algorithm"""

    @staticmethod
    def populate(grid):
        """create a list of unvisited cells"""
        unvisited = []
        for cell in grid.each():
            unvisited.append(cell)
        return unvisited

    @staticmethod
    def circuit_erased_path(path, nbr):
        """extend simple path with circuit erasure

        Arguments:
            path - a simple path (list of cells)
            nbr - an element to add to path (cell)

        Returns:
            the updated path
        """
        path.append(nbr)        # add the cell to the simple path
        n = path.index(nbr) + 1
        if n < len(path):
                # we have a simple circuit in the tail of the walk
            path = path[:n]         # erase the circuit
        return path

    @staticmethod
    def carve_path(grid, path, unvisited):
        """carve a simple path into the visited part of the grid

        Arguments:
            grid - the maze to update
            path - the path to carve (the last cell is the only
                   visited cell)
            unvisited - the unvisited part of the grid (list)

        Side effects:
            The grid and the list of unvisited cells are updated

        Returns:
            Nothing
        """
        for index in range(len(path) - 1):
            cell = path[index]
            nbr = path[index + 1]
            unvisited.remove(cell)        # side effect - unvisited
            cell.makePassage(nbr)         # side effect - grid

    @classmethod
    def on(cls, grid, start=None):
        """carve a spanning tree maze using Wilson's algorithm

        Preconditions:
            The grid must be connected.

        Arguments:
            grid - a grid
            start - a starting cell - if none is specified, we choose
                a cell at random
        """
        import random

                # preparation
        unvisited = cls.populate(grid)
        cell = start if start else grid.choice()
        unvisited.remove(cell)

        while unvisited:
                    # start somewhere in the mists
            cell = random.choice(unvisited)
            path = [cell]
            while cell in unvisited:
                        # random walk
                nbr = random.choice(list(cell.neighbors()))
                path = cls.circuit_erased_path(path, nbr)
                cell = nbr            # continue
 
                    # carve the path and update unvisited
            cls.carve_path(grid, path, unvisited)

    @classmethod
    def hybrid_on(cls, grid, start=None, cutoff=0.5):
        """carve a spanning tree maze using a hybrid algorithm

        Preconditions:
            The grid must be connected.

        Arguments:
            grid - a grid
            start - a starting cell - if none is specified, we choose
                a cell at random
            cutoff - the proportion of cell to process using Aldous/Broder;
                the remainder will be processed using Wilson.

        Note:
            if cutoff is greater than or equal to 1, the result is just
            Wilson's algorithm.  If cutoff is less than or equal to 0,
            the result is the first-entrance Aldous/Broder algorithm.
        """
        import random

                # preparation
        unvisited = cls.populate(grid)
        cell = start if start else grid.choice()
        unvisited.remove(cell)
        cutoff_count = int(len(grid) * cutoff) if cutoff > 0 else 0

                # Aldous/Broder (first entrance random walk)
        while len(unvisited) > cutoff_count:
                    # go somewhere
            nbr = random.choice(list(cell.neighbors()))

            if not nbr.arcs:              # not yet visited
                unvisited.remove(nbr)
                cell.makePassage(nbr)

            cell = nbr                    # continue the random walk

                # Wilon (circuit-erased random walk)
        while unvisited:
                    # start somewhere in the mists
            cell = random.choice(unvisited)
            path = [cell]
            while cell in unvisited:
                        # random walk
                nbr = random.choice(list(cell.neighbors()))
                path = cls.circuit_erased_path(path, nbr)
                cell = nbr            # continue
 
                    # carve the path and update unvisited
            cls.carve_path(grid, path, unvisited)

# END: wilson.py
