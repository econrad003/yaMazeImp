# -*- coding: utf-8 -*-
##############################################################################
# cylinder_grid.py - grid class for cylindrical mazes with square tiles
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
#     23 Apr 2020 - EC - Initial version
# Credits:
#     EC - Eric Conrad
##############################################################################
"""
cylinder_grid.py - cylindrical grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A cylindrical maze is a maze with square cells (using the NSEW topology)
arranged in a rectangle in which one pair of opposite sides have been
'glued' together with no twists.

Three classes are implemented:
    (1) Cylinder_Grid - a grid and maze implementation
    (2) Binary_Tree_Cyl - a binary tree algorithm for cylinder grids
    (3) Sidewinder_Cyl - a sidewinder algorithm for cylinder grids

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from square_cell import Square_Cell
from rectangular_grid import Rectangular_Grid

class Cylinder_Grid(Rectangular_Grid):
    """cylindrical grid implementation"""
    
        ###
        # Initialization
        ###
        #   essentially as for parent class Rectangular_Grid...
        #
        #   The difference is that the east and west walls are 'glued'
        #   together. We handle this gluing using the indexing.

    def __getitem__(self, index):
        """get cell by index
        
        The east and west boundaries are glued together.
        """
        i, j = index          # unpack coordinates
        j %= self.cols        # glue east and west boundaries
        index = i, j          # pack coordinates
        return super().__getitem__(index)

    def __setitem__(self, index, cell):
        """set cell by index
        
        The east and west boundaries are glued together.
        """
        i, j = index          # unpack coordinates
        j %= self.cols        # glue east and west boundaries
        index = i, j          # pack coordinates
        return super().__setitem__(index, cell)

        # for traversals by row/column (or column/row) we add optional
        # column offsets...

    def each_row(self, column_offsets=None):
        """iterate row by row"""
        if not column_offsets:
            column_offsets = [0] * self.rows
        for i in range(self.rows):
            L = []
            for j in range(self.cols):
                L.append(self[i, j+column_offsets[i]])
            yield L

    def each_column(self, column_offsets=None):
        """iterate column by column"""
        if not column_offsets:
            column_offsets = [0] * self.rows
        for j in range(self.cols):
            L = []
            for i in range(self.rows):
                L.append(self[i, j+column_offsets[i]])
            yield L

    def each_rowcol(self, column_offsets=None):
        """iterate by row and column (row major order)"""
        if not column_offsets:
            column_offsets = [0] * self.rows
        for i in range(self.rows):
            for j in range(self.cols):
                yield self[i, j+column_offsets[i]]

    def each_colrow(self, column_offsets=None):
        """iterate by column and row (column major order)"""
        if not column_offsets:
            column_offsets = [0] * self.rows
        for j in range(self.cols):
            for i in range(self.rows):
                yield self[i, j+column_offsets[i]]

        # simple maze algorithms
        #
        #   The binary tree and sidewinder algorithms need to be adapted to
        #   work on a cylindrical grid.  We do that here...

class Binary_Tree_Cylinder(object):
    """binary tree algorithm for cylindrical mazes
    
    The algorithm is implemented as a wall builder.
    """
    
    @classmethod
    def on(cls, grid, forward="forward", bias=0.5):
        """binary tree for cylindical grid
        
        Two orientations are supported:
            forward = "horizontal" (default)
                corresponds to forward=east and upward=north
            forward = "vertical"
                corresponds to forward=north and upward=east
        """

            # The Binary_Tree algorithm _almost_ works.  To make it
            # work, we need a small tweak...
            #
            #         ANALYSIS
            # What can go wrong without tweaking?
            #   (1) In the top row, we will always have an empty row.
            #       Problem: guaranteed circuit in top row!
            #   (2) In other rows, with a bad series of coin flips,
            #       we might always go eastward.
            #       Problem: possible circuits in other rows...
            # Proposed solution:
            #   erect a wall somewhere in each row
            #
            # Can something go wrong with this strategy?
            #   (1) The walls might line up vertically.
            #       Not a problem: Maze is topologically rectangular.
        from binary_tree import Binary_Tree
        from helpers import Helper as helper

            # erect a wall somewhere in each row
        helper.random_vertical_walls(grid)        # return value ignored

            # now run the binary tree algorithm
        forward, upward = helper.orientation(forward)
        Binary_Tree.wallBuilder_on(grid, forward=forward,
                                   upward=upward, bias=bias)        

class Sidewinder_Cylinder(object):
    """binary tree algorithm for cylindrical mazes
    
    The algorithm is implemented as a wall builder.
    """

    @classmethod
    def on_eastward(cls, grid, bias):
        """cylinder sidewinder with forward=eastward and upward=northward

        Row major processing.  We erect a wall somewhere in the row, and
        run sidewinder on the row starting to the right of the wall.
        """

        import random
        from helpers import Helper as helper

            #         ANALYSIS
            # What can go wrong without tweaking when (forward=east)?
            #
            #   (1) In the top row will be empty in E/N orientation.
            #
            #       Problem: guaranteed circuit in top row for E/N!
            #
            #   (2) In other rows, with a bad sequence of coin flips,
            #       we might always go eastward.
            #
            #       Problems:
            #         a) a circuit in that row
            #         b) a graph disconnection
            #
            #       Note: more general disconnection are possible
            #           with the hard internal wall zig-zagging
            #           eastward.
            #
            # Proposed solution (forward=east):
            #   erect a wall somewhere in each row.  Row processing
            #   starts to the right of the wall.  This guarantees that 
            #   there will be a cell where we are forced to go
            #   northward.
            #
            # Objections to this strategy?
            #   There might be vertical wall.
            #       Not a problem:
            #           The maze would still be a tree.

        offsets = helper.random_vertical_walls(grid)

        for i in range(grid.rows):
            offset = offsets[i]                 # start east of the wall
            run = []
            for j in range(grid.cols):
                cell = grid[i, j+offset]

                if cell.status('north'):        # can erect upward wall
                    run.append([cell, cell.topology['north']])

                nbr = cell.topology['east'] if cell.status('east') \
                    else None                   # can erect forward wall

                if nbr and run:
                        # flip a coin
                        #    heads: continue; tails: close
                    if random.random() < bias:      # heads
                        continue

                        # tails - close the run
                    cell.erectWall(nbr)

                if run:                       # tails or blocked by east wall
                        # close the run
                    n = random.randrange(len(run))
                    run.pop(n)
                    for cell1, cell2 in run:
                        cell1.erectWall(cell2)
                    run = []

    @classmethod
    def on_northward(cls, grid, bias):
        """cylinder sidewinder with forward=eastward and upward=northward

        Row major processing.  We erect a wall somewhere in the row, and
        run sidewinder on the row starting to the right of the wall.
        """

        import random
        from helpers import Helper as helper
        from sidewinder import Sidewinder

            #         ANALYSIS
            # What can go wrong without tweaking?
            #
            #   (1) With a bad sequence of coin flips, the resulting
            #       maze might be disconnected.
            #
            #   (2) The algorithm will erect exact exactly one less
            #       than the required number of walls.
            #
            # If k is the number of components in the resulting
            # maze, we must carve k-1 passages to reconnect the maze
            # and then erect k walls to remove the circuits.

            # Step 1: run sidewinder with no preprocessing
        
        def component_reduction(component):
            """add passage to reduce the number of components by 1
            
            If there is a single component, this will do nothing
            """
            for cell in component:
                for direction in cell.topology:
                    nbr = cell.topology[direction]
                    if component[cell] is not component[nbr]:
                        cell.makePassage(nbr)
                        return          # that's all folks

        def circuit_elimination(circuit):
            """eliminate a simple circuit"""
            n = random.randrange(len(circuit)-1)
            cell, nbr = circuit[n], circuit[n+1]
            cell.erectWall(nbr)

        print("Running sidewinder N/E on cylinder grid")
        Sidewinder.wallBuilder_on(grid, forward="north", 
                                  upward="east", bias=bias)

            # Step 2: component reduction
        k, visited = helper.find_components(grid)
        c = k                   # number of circuits
        while k > 1:
            print("Component reduction: %d -> %d" % (k, k-1))
            component_reduction(visited)
            k, visited = helper.find_components(grid)

            # Step 3: Circuit elimination
        while c > 0:
            print("Circuit elimination: %d -> %d" % (c, c-1))
            circuit = helper.find_circuit(grid)
            circuit_elimination(circuit)
            c -= 1

    @classmethod
    def on(cls, grid, forward="forward", bias=0.5):
        """sidewinder algorithm for cylindrical grid

        Two orientations are supported:
            forward = "horizontal" (default)
                corresponds to forward=east and upward=north
            forward = "vertical"
                corresponds to forward=north and upward=east
        """
            #         ANALYSIS
            # What can go wrong without tweaking?
            #   (1) In the top row will be empty in E/N orientation.
            #       Problem: guaranteed circuit in top row for E/N!
            #   (2) In other rows, with a bad series of coin flips,
            #       we might always go eastward.
            #       Problem: possible circuits in other rows...
            #   (3) When forward is vertical, we will produce a
            #       connected graph with exactly one too many edges
            #       implying the existence of a circuit.
            # Proposed solution when forward is horizontal:
            #   erect a wall somewhere in each row.  Row processing
            #   starts to the right of the wall.
            # Can something go wrong with this strategy?
            #   (1) The walls might line up vertically.
            #       Not a problem: Maze is topologically rectangular.
            # Proposed solution when forward is vertical:
            #   After running sidewinder, use dfs to find and cut the
            #   circuit an erect.


            #   (2) When forward is northward, we will have a cycle:
            #       in each column we will erect m-1 walls including the
            #       preset walls, for a total of (m-1)n=mn-n walls.
            #       We need exactly |V|-1=mn-1 passages.  Euler counting
            #       the number of grid edges:
            #           #northward arcs = mn-n = #southward arcs
            #           #eastward arcs = mn = #westward arcs
            #       Add the numbers of arcs and divide by 3...
            #       There are 2mn-n grid edges.  Thus we have mn passages,
            #       implying the existence of a circuit.
            #           So yes, one thing can go wrong...
        from helpers import Helper as helper

            # now run the sidewinder algorithm
        forward, _ = helper.orientation(forward)
        if forward == 'east':
            Sidewinder_Cylinder.on_eastward(grid, bias)
        else:
            Sidewinder_Cylinder.on_northward(grid, bias)

# END: cylinder_grid.py
