# -*- coding: utf-8 -*-
##############################################################################
# helpers_rect.py - friend methods for grids and mazes
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
##############################################################################
# Maintenance History:
#     23 Apr 2020 - Initial version (for cylindrical mazes)
#         methods: orientation, random_vertical_walls, find_circuit,
#             find_components
#     24 Apr 2020 - helpers for Moebius type grids
#         methods: random_vertical_walls_Moebius
#     15 May 2020 - Use cell topology management methods.
##############################################################################
"""
helpers_rect.py - rectangular grid helper routines
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Class Helper contains a number of static methods that are used in processing
instances of Grid and its subclasses. 

More information:

    see grid.py and cell.py for more information.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

class Helper:
    """grid helper"""

    @staticmethod
    def orientation(forward):
        """convert forward direction to orientation

        For rectangular grids and subclasses.
        """
        VERTICALS = ['v', 'n', 's', 'V', 'N', 'S']
        VH = ('north', 'east')
        HV = ('east', 'north')
        orientation = VH if forward[0] in VERTICALS else HV
        return orientation

    @staticmethod
    def random_vertical_walls(grid):
        """erect a vertical wall somewhere in each row of the grid

        For rectangular grids and subclasses.

        if there is already a wall or a boundary to the west of the chosen
        location, then no wall is erected in that row.

        Returns:
            a list of offsets of vertices immediately east of a wall or boundary 
        """
        from random import randrange

        offsets = []
        for i in range(grid.rows):
            j = randrange(grid.cols)
            offsets.append(j)
            cell = grid[i, j]
            if cell["west"]:
                nbr = cell["west"]
                cell.erectWall(nbr)
        return offsets

    @staticmethod
    def random_vertical_walls_Moebius(grid):
        """erect a vertical wall somewhere in each Moebius row

        For rectangular grids and subclasses.

        if there is already a wall or a boundary to the west of the chosen
        location, then no wall is erected in that row.

        Returns:
            a list of offsets of vertices immediately east of a wall or boundary 
        """
        from random import randrange

        offsets = []
        oddrow = grid.rows % 2        # 0 if even, 1 if odd
        rows = grid.rows // 2         # rounded down
        for i in range(rows+oddrow):
            j = grid.cols if i is rows else 2*grid.cols
            j = randrange(j)
            offsets.append(j)
            cell = grid[i, j]
            if cell["west"]:
                nbr = cell["west"]
                cell.erectWall(nbr)
        return offsets

    @staticmethod
    def detect_circuit_dfs(grid):
        """detect a circuit using depth-first search
        
        This will work on any connected maze.
        """
        visited = {}
        parent = None                           # root node
        cell = grid.choice()                    # random first node
        stack = [[parent, cell]]
        while stack:
            parent, cell = stack.pop()
            if cell in visited:                 # we detected a circuit
                return [parent, cell, visited]
            visited[cell] = parent
            for nbr in cell.arcs:               # iterate over passages
                if nbr is parent:                   # ignored
                    continue
                stack.append([cell, nbr])
        print("No circuit found")
        return None                         # disconnected or acyclic

    @staticmethod
    def ancestry(visited, seed):
        """created an ancestry chain starting with a given list
        
        Parameters:
            visited - a DFS ancestry tree (dictionary)
                format: visited[cell] = parent
            start - a nonempty list of cells
        """
        L = seed[:]
        ancestor = L[-1]
        while ancestor:
            ancestor = visited[ancestor]
            L.append(ancestor)
        # print("Ancestry chain length %d" % len(L))  # debugging
        return L

    @staticmethod
    def trim_paths(firstway, secondway):
        """simplify a circuit by trimming dupicates
        
        Parameters:
            firstway - a trail (list) from A to B
            secondway - another trail from A to B

        Preconditions:
            firstway[1] is not secondway[1]

        Returns:
            A non-trivial circuit (list) through A
        """
            # verify preconditions
        if firstway[0] is not secondway[0]:
            raise(ValueError, "Source cell mismatch.")
        if firstway[-1] is not secondway[-1]:
            raise(ValueError, "Terminus cell mismatch.")
        if firstway[1] is secondway[1]:
            raise(ValueError, "Precondition fails: Second cells match.")

            # trim the root nodes
        tail = None
        while firstway[-1] is secondway[-1]:
              # loop invariants:
              #     firstway = A...x
              #     secondway = A...y
              #     A...x, tail, y...A is a (not necessarily simple) circuit
            tail = firstway.pop()
            secondway.pop()
        secondway.reverse()
        circuit = firstway + [tail] + secondway
        
        # print("Circuit length %d" % len(circuit))     # debugging
        return circuit

    @staticmethod
    def find_circuit(grid):
        """locate a circuit using depth-first search
        
        This will work on any connected maze.
        """
        result = Helper.detect_circuit_dfs(grid)
        if not result:
            return None                   # disconnected or acyclic

        leaf, parent, visited = result    # unpack detector package

            # we have two paths leading from leaf to root
            # via different parents
        chain = Helper.ancestry(visited, [leaf])
        backchain = Helper.ancestry(visited, [leaf, parent])
        return Helper.trim_paths(chain, backchain)

    @staticmethod
    def find_components(grid):
        """identify the components of the maze using depth-first search
        
        Returns (k, visited):
            k - the number of connected components
            visited - dictionary - maps cell to components
                format: visited[cell] = s, where s is in 0..k-1
        """
        visited = {}
        k = 0
        for node in grid.each():
            if node in visited:           # already classified
                continue
            stack = [node]
            while stack:                  # depth-first search (DFS)
                cell = stack.pop()
                visited[cell] = k             # classify the cell
                for nbr in cell.arcs:         # classify maze neighbors
                    if nbr not in visited:
                        stack.append(nbr)
            k += 1                        # number of components
        return k, visited

# END: helpers_rect.py
