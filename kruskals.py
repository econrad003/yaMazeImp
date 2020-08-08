# -*- coding: utf-8 -*-
# kruskals.py - Kruskal's minimum weight spanning tree algorithm
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
#     31 Jul 2020 - Initial version
#     1 Aug 2020 - Add code to enable weaving
#     4 Aug 2020 - Add long tunnels to State class
"""
kruskals.py - Kruskal's minimum weight spanning tree algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Kruskal's Algorithm:

    Given an undirected edge-weigted graph G=(V, E) with vertex set V
    and weighted edge set E, we proceed as follows.

    (1) Initialization: Give each vertex a unique color.  Mark each
        edge as unvisited.

    (2) Repeat:
    
        (a) Choose the cheapest unvisited edge {u, v} and mark it as
            visited.

        (b) If u and v have different labels:

            (i) add the edge to the spanning tree;

            (ii) letting X be the set of vertices having the same color
                as v, color each vertex in X with the color of u.

    The algorithm terminates when either |V|-1 edges have been added to
    the spanning tree (in which case the algorithm succeeds) or all
    edges have been visited (in which case G is not connected and we
    have a spanning forest consisting of minimum weight spanning trees
    in each component of G)

Prerequisites:

    This passage-carving algorithm works on any grid, even if the grid 
    is not connected.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    See discussion above.
"""

from random import random, shuffle, randint

class Kruskals:
    """implementation of Kruskal's algorithms"""

    class State(object):
        """an object which holds the algorithm's current state"""

        def __init__(self, grid, crossings=None):
            """constructor"""
            self.grid = grid
            self.crossings = crossings if crossings \
                else [["north", "south"], ["east", "west"]]

            n = 0
            self.colors = {}
            self.cells = {}
            self.unvisited = []

            for cell in grid.each():
                    # initialize each cell to a unique color
                self.colors[cell] = n     # color the cell
                self.cells[n] = [cell]    # reverse lookup
                n += 1                    # cell -> color is 1-1

            for cell in grid.each():
                    # mark each edge as unvisited...
                for nbr in cell.neighbors():
                        # note that edges are undirected and loops are
                        # not admissible, so our initial coloring
                        # uniquely directs each edge...
                    if self.colors[cell] < self.colors[nbr]:
                        self.unvisited.append([cell, nbr])

        def ok_for_merge(self, cell, nbr):
            """will adding the edge introduce a circuit?"""
            return self.colors[cell] != self.colors[nbr]

        def merge(self, cell, nbr):
            """recolor the merged components"""
            n = self.colors[cell]

            if nbr not in self.colors:        # nbr is an undercell
                self.colors[nbr] = n
                cell.makePassage(nbr)
                return

            m = self.colors[nbr]
            if n > m:
                  # this isn't strictly necessary...            
                self.merge(nbr, cell)
                return

            assert n < m, "Kruskal Error: merging same color!"
            # print("Merging components %d and %d" % (n, m))

            cell.makePassage(nbr)

                # recolor the nbr set:
            for item in self.cells[m]:
                self.colors[item] = n
                self.cells[n].append(item)

                # now no one has color m
            del self.cells[m]

        def ok_for_weave(self, cell):
            """will adding a weave crossing cause problems?"""
            if cell.passages():
                return False      # cell already has a link

                # check the directional neighbors
            for left, right in self.crossings:
                nbr1 = cell[left]         # e.g. north
                if not nbr1:
                    return False
                nbr2 = cell[right]        # e.g. south
                if not nbr2:
                    return False
                if not self.ok_for_merge(nbr1, nbr2):
                    return False

                # okay for weave
            return True

        def add_weave(self, cell):
            """add a weave crossing before running the algorithm"""
            if not self.ok_for_weave(cell):
                return False

                # mark the cell's grid edges as visited
            new_unvisited = []
            for edge in self.unvisited:
                if cell not in edge:
                    new_unvisited.append(edge)
            self.unvisited = new_unvisited

                # pick direction of weave
                #   up, down for undercell
                #   left, right for overcell
            if random() > 0.5:
                [[left, right], [up, down]] = self.crossings
            else:
                [[up, down], [left, right]] = self.crossings

            self.merge(cell, cell[left])
            self.merge(cell, cell[right])

            downcell = cell[down]
            upcell = cell[up]
            self.grid.tunnel_under(cell)
            undercell = upcell[down]
            self.merge(downcell, undercell)
            self.merge(upcell, undercell)
            return True

        def add_random_weaves(self, n=0):
            """attempt to add a number of weave crossings"""
            if n<1:
                n = len(self.grid)
            added = 0
            for m in range(n):
                i = randint(1, self.grid.rows-2)
                j = randint(1, self.grid.cols-2)
                cell = self.grid[i, j]
                if cell:
                    if self.add_weave(cell):
                        added += 1
            return added

        def add_long_tunnel(self, start, direction, length):
            """attempt to add a long tunnel"""
            s, undercells, last = \
                self.grid.add_long_tunnel(start, direction, length)
            if s:
                return s        # failure (message)

                # At this point the tunnel is complete.  Two things must
                # be done:
                #   1) Update the unvisited edges list
                #   2) Mark the cells in the tunnel and its entrances
                #     as connected

                # recover the former grid path
            oldpath = {}
            for cell in undercells:
                    # the undercell index is the parent overcell
                oldpath[cell.index] = 1
            oldpath[start] = 1
            oldpath[last] = 1

                # update the unvisited list
            new_unvisited = []
            for edge in self.unvisited:
                cell, nbr = edge
                if cell not in oldpath or nbr not in oldpath:
                    new_unvisited.append(edge)
            self.unvisited = new_unvisited

                # update the component list
            color, other = self.colors[start], self.colors[last]
            if color > other:
                color, other = other, color

            if color is not other:    # it it is, we've created a circuit
                for item in self.cells[other]:
                    self.colors[item] = color
                    self.cells[color].append(item)
                del self.cells[other]
            for undercell in undercells:
                self.colors[undercell] = color
                self.cells[color].append(undercell)
            return s            # success (empty string)

        def force_connection(self, cell, direction):
            """force a connection in the indicated direction"""
            nbr = cell[direction]
            self.merge(cell, nbr)
                # update the unvisited list
            new_unvisited = []
            for edge in self.unvisited:
                if cell not in edge or nbr not in edge:
                    new_unvisited.append(edge)
            self.unvisited = new_unvisited

    @classmethod
    def on(cls, grid, state=None):
        """carve a spanning tree maze using Kruskal's algorithm"""

        if not state:
            state = cls.State(grid)
        shuffle(state.unvisited)      # last unvisited is least weight

        while state.unvisited:
                # get the least weight edge
            cell, nbr = state.unvisited.pop()
            if state.ok_for_merge(cell, nbr):
                state.merge(cell, nbr)

# END: kruskals.py
