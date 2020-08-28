# -*- coding: utf-8 -*-
# ellers.py - Eller's tapestry spanning tree algorithm
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
#     27 Aug 2020 - Initial version
"""
ellers.py - Eller's tapesty spanning tree algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Eller's Algorithm:

    Given an undirected graph G=(V, E) with vertex set V and edge set
    E, with vertices partitioned into rows [R1, R2, ..., Rn] we proceed
    as follows.

    (1) Initialization: Assign each vertex in R1 a unique color.  Let
      the current row R be R1, i.e. let R = R1.  Initialize the forest
      to empty.

    (2) Repeat:
    
        (a) Let F be the set of edges {u, v} where u and v are both
          in the current row R. Let F' be a random subset of these
          edges.  For each {u, v} in F', if u and v have different
          colors:
              add edge {u, v} to the forest; and

              recolor all vertices having the same color as v
              with the color of u

        (b) Let S be the next row, if any. Color the vertices in S
          as follows: (i) for each color in R, choose at least one
          vertex u of that color and give a neighbor v in S the same
          color, then add edge {u, v} to the forest;
          (ii) for each uncolored vertex in S, assign a unique color;
          (iii) let R = S and continue with the next row.

    (3) At this point, R is the last row. Its vertices can be thought
      of as loose threads that may need to be joined.  So for each
      edge {u, v} with both vertices in row R, if u and v have
      different colors, add edge {u, v} to the forest and recolor the
      vertices having the same color as v so they now have the same
      color as u.

If all has gone well, all vertices have the same color and the forest
is a spanning tree.

Background:

    Eller's algorithm was developed by Marlin Eller in 1982.

Prerequisites:

    This passage-carving algorithm works on rectangular grids, 
    and can be adapted to work on grids satisfying certain row 
    conditions.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from random import random, shuffle, randint

class Ellers:
    """implementation of Eller's algorithm"""

    class State(object):
        """an object which holds the algorithm's current state"""

        def __init__(self, grid, **kwargs):
            """constructor"""
            self.grid = grid
            self.nextcolor = 0
            self.row = 0
            self.cells = {}       # cells[color] = {cell1, cell2, ...}
            self.colors = {}      # colors[cell] = color
            self.kwargs = kwargs
            self.configure()      # hook for subclasses

        def configure(self):
            """subclass configuration"""
            pass

        def assign_color(self, cell):
            """assign a unique color to a new cell"""
            color = self.nextcolor
            self.nextcolor += 1
            self.colors[cell] = color
            self.cells[color] = [cell]
            return color                      # return assigned color

        def row_index(self, cell):
            """return the row index of a cell"""
            i, j = cell.index
            return i                          # return row index

        def merge(self, cell, nbr):
            """recolor the merged components"""
                    # dynamic coloring check
            m = self.colors[cell] if cell in self.colors \
                else self.assign_color(cell)
            n = self.colors[nbr] if nbr in self.colors \
                else self.assign_color(nbr)

            if m is n:
                return False                  # already the same color

            cell.makePassage(nbr)             # add edge to the forest

                    # update the colorscheme
            for nbrnbr in self.cells[n]:
                self.cells[m].append(nbrnbr)
                self.colors[nbrnbr] = m
            del self.cells[n]

            return True                       # merge complete

        def next_row(self):
            """get the edges in the next row of the grid

            Here we are assuming rectangular grid topology.  Override
            this method for other topologies.
            """
            i = self.row
            self.row += 1

            rowEdges = []
            colEdges = []

            for j in range(self.grid.cols):
                u = self.grid[i, j]

                    # get neighbors
                v = u["north"]
                if v:
                    colEdges.append(frozenset([u, v]))
                v = u["east"]
                if v:
                    rowEdges.append(frozenset([u, v]))

            if rowEdges:
                shuffle(rowEdges)
            if colEdges:
                shuffle(colEdges)
            return (rowEdges, colEdges)

        def row_merge(self, rowEdges, bias):
            """link some adjacent entries in a given row"""
            for edge in rowEdges:
                if random() < bias:
                    continue              # don't link
                u, v = edge
                self.merge(u, v)          # link (ignore status)

        def row_merge_all(self, rowEdges):
            """close out the last row"""
            for edge in rowEdges:
                u, v = edge
                self.merge(u, v)          # link (ignore status)

        def drop_merge(self, colEdges, bias):
            """link some current row cells with some in the next

            A requirement is that each color must drop into the
            next row at least once.
            """
            colors_dropped = {}
            i = self.row                  # next row index 
            for edge in colEdges:
                    # u - current row; v - next row
                u, v = edge               # unpack
                if self.row_index(u) is i:
                    u, v = v, u

                    # require at least one of a color
                color = self.colors[u] if u in self.colors \
                    else self.assign_color(u)

                if color not in colors_dropped or random() < bias:
                    self.merge(u, v)
                    colors_dropped[color] = 1

    @classmethod
    def on(cls, grid, state=None, bias1=0.5, bias2=0.5):
        """carve a spanning tree maze using Eller's algorithm"""

        if not state:
            state = cls.State(grid)

            # access the first row and its neighborhood
        rowEdges, colEdges = state.next_row()

        while colEdges:
            state.row_merge(rowEdges, bias1)
            state.drop_merge(colEdges, bias2)
                # access the current row and its neighborhood
            rowEdges, colEdges = state.next_row()

        state.row_merge_all(rowEdges)

        print("Number of components on completion: %d" % len(state.cells))
        return len(state.cells)

# END: ellers.py
