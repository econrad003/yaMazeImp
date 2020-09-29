# -*- coding: utf-8 -*-
# recursive_backtracker.py - the recursive backtracker (dfs) algorithm
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
#     15 May 2020 - Initial version
"""
recursive_backtracker.py - the recursive backtracker (dfs) algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    Push the starting cell onto the stack.
    While the stack is not empty:
        let the current cell be the top cell in the stack;
        mark the current cell as visited;
        if the current cell has an unvisited neighbor:
            push that neighbor onto the stack;
            carve a passage to that neighbor;
        else:
            pop the current cell from the stack

Remarks:

    The algorithm as given here and in (1) is a passage carver.

    This algorithm is an example of depth-first search.  If the grid is
    disconnected, the resulting maze will be a depth-first search tree
    on the component containing the starting cell.  If the grid is
    connected, the result is a depth-first spanning search tree.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    See discussion above.
"""

from random import choice
from abc import ABC, abstractmethod

class AbstractQueue(ABC):
    """an abstract queue object"""

    def __init__(self):
        """constructor"""
        self.initialize()

    @abstractmethod
    def initialize():
        """create the structure"""

    @abstractmethod
    def not_empty(self):
        """returns True if not empty and False if empty"""
        pass

    @abstractmethod
    def enter(self, package):
        """places a package in the queue"""
        pass

    @abstractmethod
    def first(self):
        """retrieve the package which is first in queue"""
        pass

    @abstractmethod
    def serve(self):
        """remove the package from the queue"""
        pass

class Stack(AbstractQueue):
    """the default queue discipline: LIFO (stack)"""

    def initialize(self):
        """constructor - create an empty queue"""
        self.stack = []

    def not_empty(self):
        """returns True if not empty and False if empty"""
        return bool(self.stack)

    def enter(self, package):
        """places a package in the queue"""
        self.stack.append(package)

    def first(self):
        """retrieve the package which is first in queue"""
        package = self.stack[-1]
        return package

    def serve(self):
        """remove the package from the queue"""
        package = self.stack.pop()
        return package

class Queue(AbstractQueue):
    """the alternative queue discipline: FIFO (queue)"""

    def initialize(self):
        """constructor - create an empty queue"""
        self.queue = []

    def not_empty(self):
        """returns True if not empty and False if empty"""
        return bool(self.queue)

    def enter(self, package):
        """places a package in the queue"""
        self.queue.append(package)

    def first(self):
        """retrieve the package which is first in queue"""
        package = self.queue[0]
        return package

    def serve(self):
        """remove the package from the queue"""
        package = self.queue.pop(0)
        return package

class Directed_Recursive_Backtracker:
    """implementation of the directed recursive backtracker algorithm"""

    class State(object):
        """a state matrix for algorithm customization"""

        def __init__(self, grid, terminus=None, towards=True,
                     deterministic=False, QueueType=Stack):
            """constructor"""
            self.grid = grid
            self.terminus = terminus if terminus \
                else grid.choice()
            self.towards = towards
            self.take_first = deterministic
            self.QueueType = QueueType

                # queue management

        def priority(self, target, sender):
            """get the package priority"""
            return None         # ignored for LIFO or FIFO

        def wrap_package(self, target, sender=None):
            """prepare a package for the queue

            Required arguments:
                target - the target cell

            Optional arguments:
                sender - the source cell if any

            For a simple stack or queue implementation, no additional
            information is needed.  For a priority queue implementation, 
            arc or edge weights can be recovered from the (target,
            sender) pair.

            If the sender is None, the target should be the terminus.
            """
            priority = self.priority(target, sender)
            package = [priority, [target, sender]]
            self.queue.enter(package)

        def inspect_package(self):
            """inspect next package and identify the target

            Returns:
                the target, sender pair

            Note that the package is not removed from the queue at
            this point.
            """
            package = self.queue.first()
            return package[1]

                # support routines

        def first_unvisited(self, cell):
            """choose the first unvisited neighbor"""
            for nbr in cell.each_neighbor():
                if nbr in self.visited:
                    continue                  # already visited
                if nbr is cell:
                    continue                  # loop in grid
                return nbr                # found - Success!
            return None               # Failure!

        def choose_unvisited(self, cell):
            """choose a random unvisited neighbor"""
            nbrs = []
            for nbr in cell.each_neighbor():
                if nbr in self.visited:
                    continue                  # already visited
                if nbr is cell:
                    continue                  # loop in grid
                nbrs.append(nbr)          # found - not yet visited

            if nbrs:
                # unvisited_str = "%d unvisited neighbors;" % len(nbrs)
                # tunnel_str = "tunnel? " + str(cell.can_tunnel_south())
                # print("cell:", cell.index, unvisited_str, tunnel_str)
                return choice(nbrs)       # Success!
            return None               # Failure!

        def pick_unvisited(self, cell):
            """pick an unvisited neighbor"""
            nbr = self.first_unvisited(cell) if self.take_first \
                else self.choose_unvisited(cell)
            return nbr

        def carve(self, cell, nbr):
            """carve the required arc"""
            if self.towards:
                cell.makePassage(nbr, twoWay=False)
            else:
                nbr.makePassage(cell, twoWay=False)
            self.visited.add(nbr)

                # one pass of the algorithm
            
        def run(self):
            """one pass of the algorithm"""
                # start at the terminus
            self.queue = self.QueueType()
            self.wrap_package(self.terminus)
            self.visited = {self.terminus}
            print("terminus:", self.terminus.index)

            while self.queue.not_empty():
                cell, _ = self.inspect_package()
                # print("cell:", cell.index)

                nbr = self.pick_unvisited(cell)
                if nbr:
                    # print("  -> cell", nbr.index)
                    self.wrap_package(nbr, cell)  # place in queue
                    self.carve(cell, nbr)         # carve passage
                else:
                    self.queue.serve()        # all neighbors visited

        def run_both_ways(self):
            """two-way run"""
            print("\tPass 1...")
            self.run()
            self.towards = not self.towards
            print("\tPass 2...")
            self.run()
            print("Done!")

    @classmethod
    def on(cls, grid, state=None, towards="both", terminus=None):
        """carve a directed DFS maze (passage carver)

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            state - a state matrix
            towards - one of "towards", "away" or "both" (default: both);
                the first letter suffices
            bias - coin fairness changer
        """
        if not state:
            state = cls.State(grid)

        state.towards = towards[0] not in {'a', 'A'}
        if towards[0] in {'b', 'B'}:
            state.run_both_ways()
        else:
            state.run()
        state.stat = 0
        return state

# END: recursive_backtracker.py
