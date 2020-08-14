# -*- coding: utf-8 -*-
# prims.py - Prim's minimum weight spanning tree algorithm
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
#     9 Aug 2020 - Initial version
#     10 Aug 2020 - Bug fix - remove start vertex from unvisited
"""
prims.py - Prim's minimum weight spanning tree algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Prim's Algorithm:

    Given an undirected edge-weigted graph G=(V, E) with vertex set V
    and weighted edge set E, we proceed from a designated start vertex
    as follows:

    (1) Initialization: Mark each vertex as unvisited.  Mark the start
        vertex v as visited.  Place all edges incident to v in a
        priority queue.

    (2) Repeat:
    
        (a) Remove the cheapest edge {u, v} from the priority queue.

        (b) If either u or v is unvisited:

            (i) add the edge to the spanning tree;

            (ii) adjust the labels so that v is the unvisited vertex;

            (iii) place all edges incident to v and an unvisited vertex
                in the priority queue;

            (iv) mark vertex v as visited.

    The algorithm terminates when the priority queue is empty.

Background:

    Prims's algorithm was first developed by Czech mathematician Vojtěch
    Jarník in 1930 and independently rediscovered by computer
    scientist Robert Prim in 1957.  [1, page 176]

Prerequisites:

    If the grid is not connected, the algorithm will only produce a tree
    spanning the component containing the start vertex.  This is easy to
    detect as, if the grid is disconnected, the set of unvisited vertices
    will not be empty.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    (1) The implementation assumes that all grid edges are undirected.
"""

from random import random, randint, choice
from queue import PriorityQueue

#   MISSING from Python3.6
# from dataclasses import dataclass, field
# from typing import Any

from functools import total_ordering

class Prims:
    """implementation of Prim's algorithms"""

#    @dataclass(order=True)
#    class Prioritized_Item:
#        priority: float
#        item: Any=field(compare=False)

    @total_ordering
    class Prioritized_Item:
        """a prioritized pair (priority, item)"""

        def __init__(self, priority, item):
            self.priority = priority
            self.item = item

        def __eq__(self, other):
            return self.priority == other.priority

        def __ne__(self, other):
            return self.priority != other.priority

        def __lt__(self, other):
            return self.priority < other.priority

    class State(object):
        """an object which holds the algorithm's current state"""

        def __init__(self, grid, weights={}):
            """constructor"""
            self.grid = grid
            self.unvisited = {}
            self.visited = {}
            self.weights = weights
            self.pq = PriorityQueue()

            for cell in grid.each():
                    # mark all vertices (cells) as unvisited
                self.unvisited[cell] = 1

        def weightOf(self, edge):
            """determine the weight of a cell"""
            if edge in self.weights:
                return self.weights[edge]
            return random()

        def extend_frontier(self, v):
            """extend the frontier
            
            Precondition:
                v is an unvisited cell
            """
                # look for edges on the frontier
            for w in v.neighbors():
                if w in self.unvisited:
                    e = frozenset({v, w})
                    wgt = self.weightOf(e)
                    self.pq.put_nowait(Prims.Prioritized_Item(wgt, e))

        def merge(self, u, v):
            """check and add the edge to the spanning tree"""
                # order cells consistently (u-visited, v-unvisited)
            if v in self.visited:
                u, v = v, u
            if v in self.visited:
                return        # nothing to do (both visited)

                # make sure the edge is still valid
            if v not in u.neighbors() or u not in v.neighbors():
                return

                # add the edge to the spanning tree
                #   then mark vertex v as visited
            u.makePassage(v)
            del self.unvisited[v]
            self.visited[v] = 1

                # look for edges on the frontier
            self.extend_frontier(v)

        def pop(self):
            """get an item from the priority queue"""
            if self.pq.empty():
                return None
            node = self.pq.get_nowait()
            return node.item

    @classmethod
    def on(cls, grid, start=None, state=None, loop=True, debug=False):
        """carve a spanning tree maze using Prim's algorithm"""

            # initialize the state matrix
        if not state:
            state = cls.State(grid)

        while state.unvisited:
            if debug:
                print("Prims: %d unvisited out of %d cells" \
                    % (len(state.unvisited), len(grid)))

                # get a starting cell
            if start not in state.unvisited:
                cells = list(state.unvisited.keys())
                start = choice(cells)

                # initialize the frontier (i.e. priority queue)
            state.extend_frontier(start)
            del state.unvisited[start]          # 10 Aug 2020
            state.visited[start] = 1            # 10 Aug 2020

            while not state.pq.empty():
                u, v = state.pop()
                state.merge(u, v)

            if not loop:
                    # in this case, only the start component is
                    # completed
                break

# END: prims.py
