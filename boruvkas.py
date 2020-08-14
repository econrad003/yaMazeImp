# -*- coding: utf-8 -*-
# boruvkas.py - Borůvka's minimum weight spanning tree algorithm
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
#     11 Aug 2020 - Initial version
"""
boruvkas.py - Borůvka's minimum weight spanning tree algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Borůvka's Algorithm:

    Given an undirected edge-weigted graph G=(V, E) with vertex set V
    and weighted edge set E with an injective weight function, we 
    proceed as follows.

    (1) Initialization: Give each vertex a unique color.  Mark each
        edge as unvisited. Let F={V, Ø} and Available=E.

    (2) While k(F)>1:
    
        (a) For each component K of F, set C(K) = None

        (b) For each edge e = {u, v} in Available:

            if K(u) != K(v):
            
                (i) if C(K(u)) is None or e is cheaper than C(K(u)),
                    set C(K(u)) to e;

                (ii) if C(K(v)) is None or e is cheaper than C(K(v)),
                    set C(K(v)) to e;

        (c) For each component K of F, if C(K) is not None, add
            C(K) to E(F).

    Since the algorithm identifies all edges before any edges are
    added, it cannot produce weaves in woven grids.  The method
    Boruvkas.State.add_weave can produce preweaves in a manner
    that is consistent with the algorithm.

Background:

    Borůvka's algorithm was originally developed by Otakar Borůvka
    in 1926 for constructing an efficient electrical network in
    Moravia.  It was rediscovered several times: by Choquet (1938),
    Florek, Łukasiewicz et al (1951) and Sollin (1965).  It is
    sometimes called Sollin's algorithm.

References:

    [1] Wikipedia.  Borůvka's algorithm. Web, 17 December 2019.
        Accessed 26 March 2020.

Bugs:

    See discussion above.
"""

from random import random, shuffle, randint

class Boruvkas:
    """implementation of Borůvka's algorithm"""

    class State(object):
        """an object which holds the algorithm's current state"""

        def __init__(self, grid, crossings=None):
            """constructor"""
            self.grid = grid
            self.crossings = crossings if crossings \
                else [["north", "south"], ["east", "west"]]
            
                # get the edge set and assign the weights
                # Note: since edges are collected here, method
                #   weave_cell.Overcell.can_tunnel_under always fails.
                #   Thus, no weaves can be created here.
            self.edges = {}
            for cell in grid.each():
                for nbr in cell.neighbors():
                    e = frozenset([cell, nbr])
                    self.edges[e] = -1
            self.assign_weights()

                # initialize the forest
            self.cells = {}
            self.components = {}
            k = 0                       # number of components
            for cell in grid.each():
                k += 1
                self.cells[cell] = k          # component number
                self.components[k] = [cell]   # cells in component
            self.k = k                  # k = #{cells}

        def assign_weights(self):
            """the weights must be unique"""
            weights = [*range(0, len(self.edges))]
            shuffle(weights)
            for e in self.edges:
                self.edges[e] = weights.pop()

        def cheaper(self, e1, e2):
            """compare the edge weights"""
            return self.edges[e1] < self.edges[e2]

        def initialize_labels(self):
            """step 2(a) above"""
            self.labels = {}
            for k in self.components:
                self.labels[k] = None

        def merge(self, e):
            """one iteration of step 2(b) above"""
            u, v = e
            ku = self.cells[u]
            kv = self.cells[v]
            if ku is kv:
                return            # same component - nothing to do

                # make sure this edge was not destroyed in a weave
            if u not in v.neighbors():
                return

                # update cheapest edge in K(u)
            f = self.labels[ku]
            if f is None or self.cheaper(e, f):
                self.labels[ku] = e

                # update cheapest edge in K(v)
            f = self.labels[kv]
            if f is None or self.cheaper(e, f):
                self.labels[kv] = e

        def merge_all(self):
            """steps 2(b) and 2(c) above"""
                # step 2(b)
            for e in self.edges:
                self.merge(e)

                # step 2(c)
            self.to_do = {}
            for k in self.labels:
                e = self.labels[k]
                if e:
                    self.to_do[e] = 1
            for e in self.to_do:
                del self.edges[e]           # used
                u, v = e
                u.makePassage(v)            # add to forest
                    # join the components
                ku = self.cells[u]
                kv = self.cells[v]
                if ku > kv:
                    u, v = v, u
                    ku, kv = kv, ku
                for cell in self.components[kv]:
                    self.cells[cell] = ku
                self.components[ku] += self.components[kv]
                del self.components[kv]
                self.k -= 1

            return len(self.to_do)          # of updates

                # these next three methods are adapted from Kruskal's
                # algorithm as implemented in kruskals.py --
                # They depend on a Preweave_Grid object

                # 1) ok_for_weave: adapted with one small change

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
                if self.cells[nbr1] == self.cells[nbr2]:
                    return False

                # okay for weave
            return True

                # 2) add_weave: adapted

        def add_weave(self, cell):
            """add a weave crossing before running the algorithm"""
            if not self.ok_for_weave(cell):
                return False

                # pick direction of weave
                #   up, down for undercell
                #   left, right for overcell
            if random() > 0.5:
                [[left, right], [up, down]] = self.crossings
            else:
                [[up, down], [left, right]] = self.crossings

                # identify the four neighbors
            upcell, downcell = cell[up], cell[down]
            leftcell, rightcell = cell[left], cell[right]
            #print("weave: %s, U %s, D %s, L %s, R %s" %
            #    (str(cell.index), str(upcell.index), \
            #    str(downcell.index), str(leftcell.index), \
            #    str(rightcell.index)))

                # create the passages
            cell.makePassage(leftcell)
            cell.makePassage(rightcell)
            self.grid.tunnel_under(cell)    # Preweave.State method
            undercell = upcell[down]
            upcell.makePassage(undercell)
            downcell.makePassage(undercell)
 
                # update the data structure
            ku = self.cells[cell]           # cell's component
            for nbr in [upcell, downcell, leftcell, rightcell]:
                    # remove the original edges from consideration
                del self.edges[frozenset([cell, nbr])]

                    # correct the components information
                    # for the overpass
            for nbr in [leftcell, rightcell]:
                kv = self.cells[nbr]        # nbr's component
                if ku > kv:
                    ku, kv = kv, ku         # order: ku<kv
                for w in self.components[kv]:
                    self.cells[w] = ku
                self.components[ku] += self.components[kv]
                del self.components[kv]
                self.k -= 1

                    # and for the tunnel
            ku = self.cells[downcell]       # downcell's component
            kv = self.cells[upcell]         # upcell's component
            if ku > kv:
                ku, kv = kv, ku             # order: ku<kv
            for w in self.components[kv]:
                self.cells[w] = ku
            self.components[ku] += self.components[kv]
            del self.components[kv]

            self.cells[undercell] = ku
            self.components[ku].append(undercell)
            self.k -= 1
 
            return True

                # 3) add_random_weaves - no change

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

    @classmethod
    def on(cls, grid, state=None):
        """carve a spanning tree maze using Borůvka's algorithm"""

        if not state:
            state = cls.State(grid)

        updates = 1
        while state.k > 1 and updates > 0:
            state.initialize_labels()
            updates = state.merge_all()
            print("%s: %d edges added, %d components in forest" \
                % ("Borůvka's algorithm", updates, state.k))

# END: boruvkas.py
