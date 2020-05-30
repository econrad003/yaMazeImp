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

class Recursive_Backtracker:
    """implementation of the recursive backtracker algorithm"""

    @classmethod
    def on(cls, grid, start=None):
        """carve a spanning tree maze using random depth-first search"""
        import random

                # start somewhere
        cell = start if start else grid.choice()
        stack = [cell]

        while stack:
            cell = stack[-1]              # look at the top of the stack

            nbrs = []
            for nbr in cell.each_neighbor():
                if nbr.passages():
                    continue                  # already visited
                if nbr is cell:
                    continue                  # loop in grid
                nbrs.append(nbr)          # not yet visited

            if nbrs:                      # there are unvisited neighbors
                nbr = random.choice(nbrs)     # pick one
                stack.append(nbr)
                cell.makePassage(nbr)
            else:                         # dead end
                stack.pop()

    @classmethod
    def deterministic_on(cls, grid, 
                         directions=["east", "north", "west", "south"],
                         start=None):
        """carve a spanning tree maze using nonrandom depth-first search"""
                # start somewhere
        cell = start if start else grid.choice()
        stack = [cell]

        while stack:
            cell = stack[-1]              # look at the top of the stack

            nbr = None
            for direction in directions:  # we query the supplied directions
                candidate = cell[direction]
                if not candidate:
                    continue                  # missing direction
                if candidate.passages():
                    continue                  # already visited
                if candidate is cell:
                    continue                  # loop in grid
                nbr = candidate           # not yet visited
                break                     # found!

            if nbr:                       # first unvisited neighbor
                stack.append(nbr)
                cell.makePassage(nbr)
            else:                         # dead end
                stack.pop()

# END: recursive_backtracker.py
