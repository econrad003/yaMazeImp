# -*- coding: utf-8 -*-
# tree_search.py - generate mazes using tree search algorithms
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
#     21 May 2020 - Initial version
"""
tree_search.py - generate mazes using tree search algorithms
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

As with recursive backtracker (depth-first search), we use tree search
algorithms to produce mazes.

Algorithms:

    Breadth-first search:
        Place the start cell at the end of the queue.
        While the queue is not empty:
            remove the cell in the front of the queue
            for each unvisited neighbor of this cell:
                carve a passage from the cell to the neighbor
                place the neighbor at the end of the queue

        (Note: A cell has been visited if it is incident to a passage.)

    We modify the algorithm slightly to adapt it to a vertex priority
    queue...

    Heap search:
        Place the pair (NIL, start cell) in the heap.
        While the heap is not empty:
            remove the entry at the front of the heap
            unpack the entry as (previous, current)
            if the current cell has been visited:
                continue
            if the previous cell is not NIL:
                carve a passage from the previous cell to the current cell
            for each neighbor of the current cell:
                place the pair (current, neighbor) in the heap

        (Note: The priority of a heap entry is the priority of the second 
        element, namely the current cell.)

Remarks:

    The algorithms given here are implemented as passage carvers.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Wikipedia contributors. "Breadth-first search." Wikipedia.
        27 Apr. 2020. Web. Accessed 21 May. 2020. Web.

    [3] Wikipedia contributors. "Dijkstra's algorithm." Wikipedia.
        19 May. 2020. Web. Accessed 21 May. 2020. Web. 

Bugs:

    See discussion above.
"""
import random

class Tree_Search:
    """implementation of some tree search algorithms"""

    @classmethod
    def bfs_on(cls, grid, start=None, randomize=True):
        """carve a spanning tree maze using breadth-first search"""
                # BFS:
                #   Place the start cell at the end of the queue.
        cell = start if start else grid.choice()
        queue = [cell]

                #   While the queue is not empty:
                #     remove the cell in the front of the queue
                #     for each unvisited neighbor of this cell:
                #       carve a passage from the cell to the neighbor
                #       place the neighbor at the end of the queue

        while queue:
            cell = queue.pop(0)   # service the front

                # visit the neighbors
            nbrs = cell.neighbors()
            if randomize:
                random.shuffle(nbrs)
            for nbr in nbrs:
                if nbr.passages():
                    continue                  # already visited
                if nbr is cell:
                    continue                  # loop in grid
                cell.makePassage(nbr)
                queue.append(nbr)             # enter the neighbor

    @classmethod
    def heap_on(cls, grid, start=None, priorities={}):
        """carve a spanning tree maze using a heap"""
        import heapq

        pq = []
        d = {}
        d['count'] = 1

        def enter(cell, nbr):
            """enter a cell into the priority queue"""
            if nbr not in priorities:
                priorities[nbr] = random.random()
            priority = priorities[nbr]
            entry = [priority, d['count'], cell, nbr]
            d['count'] += 1
            heapq.heappush(pq, entry)

        cell = start if start else grid.choice()
        enter(None, cell)

        while pq:
            _, _, cell, nbr = heapq.heappop(pq)
            if nbr.passages():
                continue                    # already visited
            if nbr is cell:
                continue                    # we don't carve loops

            if cell:                        # not None
                cell.makePassage(nbr)
            cell = nbr

            for nbr in cell.each_neighbor():
                if not nbr.passages():
                    enter(cell, nbr)

# END: tree_search.py
