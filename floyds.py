# -*- coding: utf-8 -*-
# floyds.py - The Floyd-Walshall minimum weight path algorithm
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
#     9 Sep 2020 - Initial version
"""
floyds.py - The Floyd-Warshall minimum weight path algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Floyd-Warshall Algorithm:

    Given an directed edge-weigted graph G=(V, A) with vertex set V
    and weighted arc set A with no negative weight cycles, we proceed
    as follows.

    (1) Initialization: Start with a map d:V×V → R ∪ {∞} by setting
        d(u,v) := ∞ whenever u ≠ v and d(u,v) := 0 otherwise, for
        each vertex u and v.
        
        (The initial state says that a vertex is immediately reachable
        in zero steps from itself and not from any other vertex.)

    (2) For each edge (u, v):
          d(u, v) := weight(u, v)     # enter the weights

    (3) For each vertex v:            # intermediate vertex
          for each vertex u:
              for each vertex w:
                  if d(u,w) > d(u,v) + d(v,w):
                      d(u,w) := d(u,v) + d(v,w)

        (At the moment of a change, d(u,v) has the smallest known weight
        for a path from u to w.  Moreover, this is on a path that take
        u to w via vertex v.)
    
    If there is a negative weight cycle, the algorithm will terminate
    with at least one vertex u such that d(u,u) < 0.  Otherwise, the
    shortest paths can be reconstructed by keeping track of the via
    vertices v found in the inner loop.

Background:

    The Floyd-Warshall algorithm was developed independently by Robert
    Floyd in 1962, Bernard Roy in 1959, and Stephen Wasrhall in 1962.
    The triple loop formulation was described by Peter Ingerman, also
    in 1962.  The algorithm is closely related to Kleene's 1956
    algorithm for converting a DFA (deterministic finite automaton) into
    a regular expression.

Adaptation:

    Here we consider a directed maze on a grid.

References:

    [1] Wikipedia.  "Floyd-Warshall algorithm." 23 August 2020. Web,
        accessed 9 September 2020.

Bugs:

    Unknown, but see above for negative cycles.
"""

class Floyds:
    """implementation of the Floyd-Warshall algorithm"""

    class State(object):
        """an object which holds the algorithm's current state"""

        def __init__(self, grid):
            """constructor"""
            self.grid = grid
            self.dist = {}          # the distance function
            self.via = {}           # for path reconstruction
            self.configure()
            print("  initialization complete!")

        def configure(self):
            """initialize the distances"""
            for u in self.grid.each():
                for v in self.grid.each():
                    if u.have_passage(v):
                        self.dist[(u, v)] = self.weight(u, v)
                self.dist[(u, u)] = 0

        def weight(self, cell, nbr):
            """determine the weight of a directed arc
            
            In the base class, all arcs have unit weight.
            """
            assert cell.have_passage(nbr), "Undefined arc weight"
            return 1

        def compare(self, u, v, w):
            """is the chosen route an improvement"""
                    # Is there a way from u to w via v?
            if (u, v) not in self.dist:
                return        # dead end
            if (v, w) not in self.dist:
                return        # dead end
                    # There is a way...
            d1 = self.dist[(u, v)]
            d2 = self.dist[(v, w)]
            d = self.dist[(u, w)] if (u, w) in self.dist \
                else d1 + d2 + 1
                    # But is it an improvement?
            if d > d1 + d2:
                self.dist[(u, w)] = d1 + d2
                self.via[(u, w)] = v

        def triple_loop(self):
            """The characteristic cubic loop"""
            print("  Progress bar [one dot per cell, %d cells]:" % len(self.grid))
            for v in self.grid.each():          # intermediate (via)
                print(".", end="", flush=True)
                for u in self.grid.each():      # source
                    for w in self.grid.each():  # sink
                        self.compare(u, v, w)
            print("")

                # standard things to ask after running Floyd's

        def query_negative_cycles(self):
            """Check for negative weight cycles"""
            for u in self.grid.each():
                if self.dist[(u, u)] < 0:
                    return True
            return False

        def query_all_reachable_from(self, cell):
            """Is every cell reachable from a given cell?"""
            for w in self.grid.each():
                if (cell, w) not in self.dist:
                    return False
            return True

        def query_reachable_from_all(self, cell):
            """Is a given cell reachable from every cell?"""
            for u in self.grid.each():
                if (u, cell) not in self.dist:
                    return False
            return True

        def query_connected(self):
            """Is every cell reachable from every other cell?"""
                # if we can go from v to any cell and return,
                # then the entire maze is reachable from anywehere.
                #
                # Proof: Choose any two vertices u and w. The
                #   claim is that there is a path from u to w.
                #   But there is a path P from u to v and a
                #   path Q from v to w, so the path P + Q is a
                #   path from u to w.
            u = self.grid.choice()
            if not self.query_all_reachable_from(u):
                return False
            if not self.query_reachable_from_all(u):
                return False
            return True

        def shortest_path(self, u, w):
            """Find the shortest path from u to w

            Returns the path if any and its weight
            """
            if u == w:
                return [u], 0         # ignore any negative cycles
            if (u, w) not in self.via:
                if u.have_passage(w):
                    return [u, w], self.weight(u, w)

                    # this does not occur when recursion depth > 0
                return None, None

                # recursion
            v = self.via[(u, w)]      # intermediate element
            path1, wgt1 = self.shortest_path(u, v)
            path2, wgt2 = self.shortest_path(v, w)
            path = path1[:-1] + path2
            wgt = wgt1 + wgt2
            return path, wgt

    @classmethod
    def on(cls, grid, state=None):
        """evaluate a maze using the Floyd-Warshall algorithm

        The state matrix is returned.
        """

        if not state:
            state = cls.State(grid)
        state.triple_loop()
        return state

# END: floyds.py
