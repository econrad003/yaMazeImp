# -*- coding: utf-8 -*-
##############################################################################
# binary_tree2.py - binary spanning tree algorithm
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
#     26 Apr 2020 - Initial version
#     30 Apr 2020 - Correct the documentation
##############################################################################
"""
binary_tree.py - binary spanning tree implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Description:

    This is a greedy passage carving algorithm which attempts to find a
    perfect binary spanning maze.  There are situations where the algorithm
    can fail.

    The algorithm is independent of grid topology.  This is not the binary
    tree algorithm given in (1).

Algorithm:

    The cells of the grid are placed into a queue in random order.  When
    a cell reaches the front of the queue, passages are added from that
    cell to its neighbors subject to the following conditions:

        (a) the degree of the cell cannot exceed 3;
        (b) the degree of the neighbor cannot exceed 3; and
        (c) a passage cannot create a circuit.

Prerequisites:

    (1) The grid must be connected.

    (2) The grid must have a binary spanning tree.

    The simplest example of a graph which is connected but fails to have a
    binary spanning tree is the 4-star:
               2
               |
          3 -- 0 -- 1
               |
               4
              G0

Remarks:

    1) This is a greedy algorithm.  As each cell receives its turn to be
       serviced, it receives as many passages as possible.

    2) A necessary condition for the algorithm to fail on a connected grid
       is that it has a subgrid for which there is no binary spanning tree.
       (This is not a sufficient condition.)

         1 -- 2                  1 -- 2
         |    |                       |
         3 -- 4 -- 5             3 -- 4 -- 5
              |                       |
              6                       6
             G1                      G2

       The algorithm will sometimes fail on G1 and always fail on G2. Both
       have subgraphs isomorphic to G0.  In G2, there will always be exactly
       three passages from cell 4 to cells 2, 3, 5 and 6.  Thus one of the
       latter cannot be in the tree containing 4.  Adding a single edge gives
       the algorithm a possible avenue to success.

       For G1: If cell 4 arrives in the queue before there is a chain from
       cell 2 to cell 3 via cell 1, then the algorithm will fail if and only
       if cell 4 links with both cells 2 and cell 3.  The algorithm will
       succeed if and only a chain is established from cell 2 to cell 3
       via cell 1.  If cell 1 arrives first, the algorithm will always
       succeed.

    3) Considering the example G1 should lead to a proof that the algorithm
       will always succeed on a ractangular grid.  It can however fail on
       a cylindrical grid as a hard wall can be established (despite of the
       greedy condition) along an unbounded axis.  Since a Moebius strip
       is not orientable, I think the rectangular grid proof should extend to
       the Moebius grid.  My experiments on 5x7 grids suggest that failure
       is rare.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs and Features:

    See discussion above.
"""

class Binary_Tree:
    """implementation of the binary tree algorithm"""

        # pylint: disable=too-few-public-methods
        #     reason: potential for variants

    @classmethod
    def on(cls, grid):
        """carve a binary spanning tree maze (passage carver)

        Preconditions:
            For a rectangular grid, the grid must be devoid of passages.

        Arguments:
            grid - a grid
        """
        import random

        indices = list(grid.cells)
        random.shuffle(indices)
        components = {}
        relabels = {}
        n = 0
        e = 0             # number of passages

        for index in indices:
            cell = grid[index]
            if cell not in components:
                n += 1
                components[cell] = n
            x = components[cell]
            while x in relabels:
                x = relabels[x]
                components[cell] = x
            nbrs = cell.neighbors()
            random.shuffle(nbrs)
            for nbr in nbrs:
                        # maximum degree is 3
                if len(cell.arcs) > 2:
                    break
                if nbr in cell.arcs or len(nbr.arcs) > 2:
                    continue
                        # available for passage if not same component
                y = components[nbr] if nbr in components else None
                while y in relabels:
                    y = relabels[y]
                    components[y] = y
                if y is x:
                    continue      # same component
                cell.makePassage(nbr)
                e += 1
                if y is None:
                    components[nbr] = x
                elif y < x:
                    relabels[x] = y
                    x = y
                    components[cell] = y
                else:
                    relabels[y] = x

            # did we succeed? Yes if v-e is 1, otherwise not quite a tree
        return len(grid)-e        # number of components

# END: binary_tree.py
