# -*- coding: utf-8 -*-
# edgewise_growing_tree.py - offshoots of Prim's algorithm
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
"""
edgewise_growing_tree.py - variants of Prim's algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

We supply several alternative weight functions to modify the
behavior of Prim's Algorithm.

This is a solution to an exercise at the end of Chapter 11 of [1].

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from random import random, randint, choice, shuffle
from prims import Prims

class LIFO_State(Prims.State):
    """A last-in first-out implementation"""

    def __init__(self, grid, bias=0.5):
       """constructor"""
       super().__init__(grid)
       self.bias = 0.5      # hook (not used for LIFO)
       self.pq = []         # stack

    def extend_frontier(self, v):
        """extend the frontier

        Precondition:
            v is an unvisited cell
        """
            # look for edges on the frontier
        nbrs = v.neighbors()      # ok if empty
        shuffle(nbrs)
        for w in nbrs:
            if w in self.unvisited:
                e = frozenset({v, w})
                self.pq.append(e)

    def pop(self):
        """get an item from the stack"""
        if self.pq:
            return self.pq.pop()
        return None

class FIFO_State(LIFO_State):
    """A first-in first-out implementation"""

    def pop(self):
        """get the first item from the queue"""
        if self.pq:
            return self.pq.pop(0)
        return None

class MIFO_State(LIFO_State):
    """A median-in first-out implementation"""

    def pop(self):
        """get the median item from the queue"""
        if self.pq:
            median = len(self.pq) // 2
            return self.pq.pop(median)
        return None

class RIFO_State(LIFO_State):
    """A random-in first-out implementation"""

    def extend_frontier(self, v):
        """extend the frontier

        Since we always pick a cells at random, it is not necessary to
        shuffle the neighborhoods.

        Precondition:
            v is an unvisited cell
        """
            # look for edges on the frontier
        for w in v.neighbors():
            if w in self.unvisited:
                e = frozenset({v, w})
                self.pq.append(e)

    def pop(self):
        """get a random item from the queue"""
        if self.pq:
            index = randint(0, len(self.pq)-1)
            return self.pq.pop(index)
        return None

class Mixed_State(LIFO_State):
    """Randomly choose between LIFO amd RIFO
    
    We use the bias parameter here.
    """

    def pop(self):
        """get the desired queue item"""
        if not self.pq:
            return None
        flip = random()
        if flip <= self.bias:
            return self.pq.pop()        # heads => LIFO
        index = randint(0, len(self.pq)-1)
        return self.pq.pop(index)       # tails => RIFO

class Edge_Growing_Tree:
    """implementation of edgewise growing tree algorithms"""

    @classmethod
    def on(cls, grid, state, start=None, loop=True, debug=False):
        """carve a spanning tree maze using Prim's algorithm"""

            # initialize the state matrix
        while state.unvisited:
            if debug:
                print("Edge Growing Tree: %d unvisited/%d cells" \
                    % (len(state.unvisited), len(grid)))

                # get a starting cell
            if start not in state.unvisited:
                cells = list(state.unvisited.keys())
                start = choice(cells)

                # initialize the frontier (i.e. priority queue)
            state.extend_frontier(start)

            while state.pq:
                u, v = state.pop()
                state.merge(u, v)

            if not loop:
                    # in this case, only the start component is
                    # completed
                break

# END: edgewise_growing_tree.py
