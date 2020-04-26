# -*- coding: utf-8 -*-
# statistics.py - statistics class for mazes
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
statistics.py - statistics gathering
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

No assumptions are made here about the physical representation of the grid,
its passages or its walls.  All we do here is gather statistics.

Definitions:

    A grid is a graph G=(C,E) consisting of a finite set C of cells and
    a set E of edges, where an edge is an unordered pair of distinct cells.
    In other words, a grid is a simple graph as loops and parallel edges are
    not admitted.

    A maze on a grid is a spanning subgraph of the grid.  In a maze, the
    the edge set of the grid is partitioned into two subsets, the walls and
    the passages.  The passages are edges in the spanning subgraph.

Variations and Generalizations:

    Generalizations and variations might need tweaking or might have little
    support in this module.  These should be handled in subclasses.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

class Maze_Statistics(object):
    """base class for statistics on grids and mazes"""

    def __init__(self, grid, **kwargs):
        """constructor

        Mandatory arguments:
            grid - a grid containing a maze
        """
        self.grid = grid            # the parent grid
        self.name = grid.name
        self.kwargs = kwargs

    def size(self):
        """the number of cells in the grid"""
        return len(self.grid)

    def Euler_edge_counts(self):
        """the Euler counts of edges in the grid

        Description:
            This gives Euler counts of directed edges by class.  For undirected
            edges, divide these counts by two.  Loops, wherever they occur, are
            counted with multiplicity 2.  See notes 2 and 3 below for more
            information.)

        Returns:
            the tuple (passages, walls, neighbors)

        Remarks:
            1. If all passages are within neighborhoods, then:
                    passages + walls = neighbors

            2. In his paper on the Königsberg Bridge Problem, Leonhard Euler
               (1707-1783) made the following observation:
                    In any undirected graph, $G=(V, E)$:
                        $\\sum_{v\\in V} |E(v)| = 2|E|$
                            where $E(v)$ is the set of edges incident to v.
               The proof is straightforward.  Assign each edge a direction
               at random.  Then sum over the vertices.  This sum is the left
               hand side.  To obtain the right hand side, note that each edge
               is counted twice in the sum, once as an in-vertex and once as
               an out-vertex.

            3. In Euler's edge counting theorem, loops (i.e. edges of the form
               {v, v} are counted on the with multiplicity 2, so we need to
               count a loop twice on the right hand side as well.  Loops
               are not common in mazes, but we do admit them as a possibility
               here.
        """
        p = 0
        w = 0
        n = 0
        for cell in self.grid.each():
            p += len(cell.arcs)
            if cell in cell.arcs:
                p += 1                  # loop (see note 3 above)
            for direction in cell.topology:
                n += 1
                nbr = cell.topology[direction]
                if nbr is cell:
                    n += 1                  # loop (see note 3 above)
                if nbr not in cell.arcs:
                    w += 1
                    if nbr is cell:
                        w += 1              # loop (see note 3 above)
        return (p, w, n)

    def degree_counts(self):
        """count the vertices by passage degree (degree sequence)

        Loops are counted with multiplicity 2.

        Returns:
            a hash object mapping degree to the number of cells having
            the given passage degree.  Missing keys denote passage degrees
            with no representative cell, i.e. 0 cells have the indicated
            passage degree.

        Degree 0 - isolated vertices
        Degree 1 - dead ends
        """
        degrees = {}
        for cell in self.grid.each():
            p = len(cell.arcs)              # number of available passages
            if cell in cell.arcs:
                p += 1                      # for a loop
            if p in degrees:
                degrees[p] += 1             # subsequent cell with degree
            else:
                degrees[p] = 1              # first cell in degree class
        return degrees

# END: statistics.py
