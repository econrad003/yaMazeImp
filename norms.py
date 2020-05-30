# -*- coding: utf-8 -*-
# norms.py - norms (distances from root) class for cells
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
#     30 May 2020 - Initial version
"""
norms.py - cell norms implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A norms class for cells and an algorithm to inject the norms.

The class (Distances) may be used with other norms besides distance from
root.  Pseudonorms can also be used.

The associated algorithm is Dijkstra's algorithm.  It computes the
distance from root norm.

Definitions:

    A map d:V ⨯ V -> R ∪ {∞} is a metric (or distance function) on a vertex
    set V if and only if the following conditions hold:
        (1) for all u,v in V, d(u,v)≥0;
        (2) for all u,v in V, d(u,v)=0 if and only if u=v;
        (3) for all u,v in V, d(u,v)=d(v,u); and
        (4) for all u,v,w in V, d(u,v) + d(v,w) ≥ d(u,w).

    For a pseudometric, condition (2) is relaxed.  A map d:V ⨯ V -> R ∪ {∞}
    is a pseudometric on a vertex set V if and only if the following
    conditions hold:
        (1) for all u,v in V, d(u,v)≥0;
        (2') for all u,v in V, if u=v then d(u,v)=0;
        (3) for all u,v in V, d(u,v)=d(v,u); and
        (4) for all u,v,w in V, d(u,v) + d(v,w) ≥ d(u,w).

    Condition (3) is the symmetric identity.  Condition (4) is the triangle
    inequality.  Taken together, conditions (1) and (2) are the positive
    definite conditions, while the weakened pair (1) and (2') are the
    positive semi-definiteness conditions.

    For our purposes, a map N:V -> R ∪ {∞} is a metric norm (resp:
    metric pseudonorm) on V if there exists r in V and a metric (resp:
    pseudometric) d on V such that N(v)=d(v,r) for all v in V.  (NB: Most
    of sources place additional conditions on the norm function N
    and the underlying set V.)

    A metric or pseudometric is discrete if the infimum of the nonzero
    subset of the range is positive.  This will hold for any finite
    set, for example the vertex set of a graph, so for our purposes
    here, the metrics and peudometrics are all discrete.

Example 1:
    The map d(u,v) which gives the path distance from u to v is a metric on
    V.  (This is the usual path metric on V.  Since V is finite, this is a
    discrete metric.)

Example 2:
    The map d(u,v) which is 0 if u=v, 1 if u and v are distinct elements in
    the same component, and infinity if u and v are in different components,
    is a metric on V.  (This is another discrete metric on V.)

Example 3:
    The map d(u,v) which is 0 if u=v and 1 otherwise, is a metric on V.
    (This is _the_ discrete metric on V.)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
    [2] Wikipedia contributors. "Dijkstra's algorithm." Wikipediaa.
        Accessed 1 May 2020. Web.

Bugs:

    Unknown.
"""

class Distances(object):
    """base class for distances"""

    def __init__(self, root):
        """constructor

        Arguments:
            root - the root cell for distance calculations
        """
        self.root = root
        self.metrics = {}           # dictionary: cell->distance(cell, root)
        self.metrics[root] = 0      # distance(root, root) is 0

    def __getitem__(self, cell):
        """return the distance from cell to root

        Returns:
            None - if distance is undefined (i.e. cell is not is the same
                component as root)
            distance(cell, root) - if distance is defined
        """
        if cell in self.metrics:
            return self.metrics[cell]   # when distance is defined
        return None                 # when distance is not defined

    def __setitem__(self, cell, metric):
        """set the distance from cell to root"""
        self.metrics[cell] = metric

    def component(self):
        """return all cells related to root by the norm"""
        return list(self.metrics.keys())

    def path_to_root(self, cell):
        """use the distances to find a path to the root from the given cell

        The distance metric must be a reasonable distance metric"""
        if cell not in self.metrics:
            return []                  # can't get there from here

        L = []
        while cell is not self.root:
            L.append(cell)
            found = False
            for nbr in cell.arcs:
                if nbr not in self.metrics:       # forbidden node
                    continue
                if self[nbr] + 1 == self[cell]:   # one step closer
                    cell = nbr
                    found = True
                    break
            if not found:
                return []                     # failure
        L.append(self.root)
        return L

    def furthest_from_root(self):
        """find a cell at maximum distance from root"""
        furthest = self.root                  # initial guess
        d = 0
        for cell in self.metrics:
            if d < self.metrics[cell]:
                furthest = cell
                d = self.metrics[cell]
        return furthest

def distances(root):
    """calculate distances using Dijkstra's algorithm"""
    norms = Distances(root)

    frontier = [root]
    while frontier:
        new_frontier = []
        for cell in frontier:
            for nbr in cell.arcs:
                if norms[nbr] is None:    # be careful here - 0 is false!
                    norms[nbr] = 1 + norms[cell]
                    new_frontier.append(nbr)
        frontier = new_frontier

    return norms

def longest_path(root):
    """find a longest path in the maze or component containing root

    Parameters:
        root - a cell in a tree to serve as a root in the first pass

    Returns:
        list containing:
            (1) diameter (i.e. length of longest simple path)
            (2) a longest simple path
            (3) the distances from the new root cell
    """
    norms = distances(root)               # pass 1: Dijkstra from root
    new_root = norms.furthest_from_root() # pass 2: furthest
    norms = distances(new_root)           # pass 3: Dijkstra from new
    furthest = norms.furthest_from_root() # pass 4: furthest
    path = norms.path_to_root(furthest)   # pass 5: find path
    return [len(path), path, norms]       # pack and return

# END: norms.py
