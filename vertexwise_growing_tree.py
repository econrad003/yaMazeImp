# -*- coding: utf-8 -*-
# vertexwise_growing_tree.py - spanning tree algorithms based on Prim's
#     algorithm
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
#     10 Aug 2020 - Initial version
"""
vertexwise_growing_tree.py - spanning tree algorithms based on Prim's
    algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Instead of edge weights, this algorithm associates a cost with each
vertex.  At each step in the algorithm, the spanning tree is grown by
by adding a frontier vertex of least cost.  In Chapter 11 of [1], the
algorithm is variously referred to as 'True Prim', or when all
vertices have the equal weight, as 'Simple Prim'.  (The same
source refers to Prim's algorithm as 'Truest Prim'.)

Since every spanning tree of every connected graph contains every
one of the graphs vertices, the total weight of the vertices in
the spanning will equal the total weight of the vertices in the
graph.  The notion of minimum weight spanning tree is not
useful in this context.  Vertex-weighted Prim does, however,
generate a spanning tree, and changing the weight function does,
under a wide range of situations, change the edges in the
spanning tree.

Vertex-weighted Prim's algorithm:

    (N.B.: This is not Prim's algorithm!)

    Given an undirected edge-weigted graph G=(V, E) with weighted vertex
    set V and weighted edge set E, we proceed from a designated start
    vertex as follows:

    (1) Initialization: Let the growing tree consist of the start
        vertex.  Mark all other vertices as unvisited.  Place the 
        neighbors of the start vertex v in the frontier visited.

    (2) Repeat:
    
        (a) Remove a lowest cost vertex v from the frontier.

        (b) If v is unvisited:

            (i) locate a neighbor u in the growing tree;

            (ii) add the edge {u, v} and the vertex v to the
                growing tree and mark v as visited;

            (iii) place all unvisited neighbors w of v in the
                frontier.

    The algorithm terminates when the frontier is empty.

Background:

    In maze construction, "Prim's algorithm" often refers this
    algorithm. [1, Chapter 11]  This is loose terminology. Note
    that Prim's algorithm uses edge weight while this algorithm 
    uses vertex costs.

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

from random import random, randint, choice, shuffle
from queue import PriorityQueue

#   MISSING from Python3.6
# from dataclasses import dataclass, field
# from typing import Any

from functools import total_ordering

class Vertex_Prims:
    """implementation of Prim's algorithms"""

#    @dataclass(order=True)
#    class Prioritized_Item:
#        priority: float
#        item: Any=field(compare=False)

    @total_ordering
    class Queue_Node:
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
        """an object which holds the algorithm's current state
        
        Subclasses can be developed by changing costOf and totalCostTo,
        or push and pop.  Normally a change is needed to initialize.
        """

        def __init__(self, grid):
            """constructor"""
            self.grid = grid
            self.unvisited = {}
            self.frontier = {}
            self.visited = {}
            self.pq = PriorityQueue()

            for cell in grid.each():
                    # mark all vertices (cells) as unvisited
                self.unvisited[cell] = 1
            self.initialize()

        def initialize(self):
            """hook for subclasses"""
            pass

        def costOf(self, cell):
            """the cost of a cell when placed in the frontier"""
            return 1                                  # uniform cost

        def totalCostTo(self, via, to, visited):
            """the path cost from start to the given cell"""
            return visited[via] + self.costOf(to)     # total cost

        def extend_frontier(self, v):
            """extend the frontier
            
            Precondition:
                v is a newly visited cell
            """
                # look for edges on the frontier
            nbrs = v.neighbors()
            shuffle(nbrs)
            for w in nbrs:
                if w in self.unvisited and w not in self.frontier:
                    cost = self.costOf(w)
                    self.push(cost, w)
                    self.frontier[w] = cost

        def merge(self, via, to):
            """check and add the edge to the spanning tree"""
                # order of cells: via in visited, to in frontier)

                # add the edge to the spanning tree
                #   then mark vertex v as visited
            via.makePassage(to)
            del self.unvisited[to]
            del self.frontier[to]
            self.visited[to] = self.totalCostTo(via, to, self.visited)

                # look for edges on the frontier
            self.extend_frontier(to)

        def push(self, cost, w):
            """push a cell onto the priority queue"""
            self.pq.put_nowait(Vertex_Prims.Queue_Node(cost, w))

        def pop(self):
            """get an item from the priority queue"""
            if self.pq.empty():
                return None
            node = self.pq.get_nowait()
            return node.item

        def minimize_total_cost(self, to):
            """find a via vertex which minimizes total cost"""
            vias = []
            via = None
            for nbr in to.each_neighbor():
                if nbr not in self.visited:
                    continue
                if not via:
                    via = nbr
                    vias = [nbr]
                    continue
                if self.costOf(via) < self.costOf(nbr):
                    continue
                if self.costOf(via) > self.costOf(nbr):
                    via = nbr
                    vias = [nbr]
                    continue
                vias.append(nbr)
            return choice(vias)

    @classmethod
    def on(cls, grid, start=None, state=None, loop=True, debug=False):
        """carve a spanning tree maze using Prim's algorithm"""

            # initialize the state matrix
        if not state:
            state = cls.State(grid)

        while state.unvisited:
            if debug:
                print("Vertex_Prims: %d unvisited out of %d cells" \
                    % (len(state.unvisited), len(grid)))

                # get a starting cell
            if start not in state.unvisited:
                cells = list(state.unvisited.keys())
                start = choice(cells)

                # adjust visited, unvisited, frontier and priority queue
            state.visited[start] = 0
            del state.unvisited[start]
            state.extend_frontier(start)

            while state.frontier:
                v = state.pop()
                u = state.minimize_total_cost(v)
                state.merge(u, v)

            if not loop:
                    # in this case, only the start component is
                    # completed
                break

# some state classes developed by adjusting cost...

class Random_Cost_State(Vertex_Prims.State):
    """random vertex cost"""

    def initialize(self):
        """initialize the costs"""
        self.costs = {}
        for cell in self.grid.each():
            self.costs[cell] = random()

    def costOf(self, cell):
        """the cost of a cell when placed in the frontier"""
        return self.costs[cell]

class LIFO_Cost_State(Vertex_Prims.State):
    """most recent in frontier are least cost"""

    def initialize(self):
        """initialize the costs"""
        self.base_cost = len(self.grid)
        self.costs = {}

    def costOf(self, cell):
        """the cost of a cell when placed in the frontier"""
        if cell not in self.costs:
            self.costs[cell] = self.base_cost
            self.base_cost -= 1       # next one will be cheaper
        return self.costs[cell]

class FIFO_Cost_State(Vertex_Prims.State):
    """oldest in frontier are least cost"""

    def initialize(self):
        """initialize the costs"""
        self.base_cost = 1
        self.costs = {}

    def costOf(self, cell):
        """the cost of a cell when placed in the frontier"""
        if cell not in self.costs:
            self.costs[cell] = self.base_cost
            self.base_cost += 1       # next one will be pricier
        return self.costs[cell]

    # we can instead work with push and pop to change the queue
    # discipline...

class LIFO_Queue_State(Vertex_Prims.State):
    """replacing the priority queue with a stack"""

    def initialize(self):
        """initialize the stack"""
        self.pq = []

    def push(self, cost, v):
        """push a vertex onto the stack, ignoring cost"""
        self.pq.append(v)

    def pop(self):
        """remove a vertex from the stack"""
        return self.pq.pop()

class FIFO_Queue_State(LIFO_Queue_State):
    """replacing the priority queue with a FIFO queue"""

    def pop(self):
        """remove a vertex from the stack"""
        return self.pq.pop(0)

class RIFO_Queue_State(LIFO_Queue_State):
    """replacing the priority queue with a random queue"""

    def pop(self):
        """remove a vertex from the stack"""
        index = randint(0, len(self.pq)-1)
        return self.pq.pop(index)

# END: vertexwise_growing_tree.py
