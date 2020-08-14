# -*- coding: utf-8 -*-
# recursive_division.py - carving a spanning tree by recursive division
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
#     12 Aug 2020 - Initial version
"""
recursive_division.py - carving a spanning tree by recursive division
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    The algorithm is straightforward -- we divide the grid
    horizontally and dividing vertically into two rectangles.
    If we are left with a rectangle of width or height 1, we
    connect all its cells.  After dividing, we carve a passage
    to connect the two rectangles.

    In [1], recursive division is implemented as a wall adder.
    It is implemented here as a passage carver.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs and Features:

    Unknown.
"""

from math import sqrt
from random import randint, choice
from rectangular_grid import Rectangular_Grid
from sidewinder import Sidewinder 

class Recursive_Division:
    """implementation of the recursive division algorithm"""

    class State:
        """to allow reconfiguration of the algorithm

        Arguments:
            grid - a grid to transform into a maze

        Optional arguments:
            delta - the diameter inferior (integer, default 1)
            algorithm - an algorithm to use to carve mazes from subgrids
                smaller than or equal in diameter to the diameter
                inferior (default Sidewinder)

        As configured here, it is assumed that the maze is rectangular
        and that the subgrid partitions (or "shapes") will also be
        rectangular with sides parallel to the axes.  The diameter of
        a subgrid is the mininum of the number of rows and the number
        of columns in the subgrid.

        For carving a maze from a subgrid, see methods "carve" and
        and "carve_shadow".  For creating a door between two partitions,
        see "make_doorway".

        Method "carve_shadow" creates a grid of the required shape
        and creates a maze on the grid using the "on" class-method
        of the indicated algorithm:

            algorithm.on(grid)

        If delta=1 and partitions are the default rectangles, any
        fast perfect maze algorithm will do for carving mazes on the
        minimal partitions as the only trees of diameter inferior 1
        are chains.  Either Sidewinder or Binary_Tree is ideal.

        For delta>1, the choice of algorithm will affect the texture
        of the mazes inside the minimal partitions and also the
        overall texture of the completed maze.
        """

        def __init__(self, grid, **kwargs):
            """constructor"""
            self.grid = grid
            self.kwargs = kwargs
            self.delta = kwargs["delta"] if "delta" in kwargs else 1
            if self.delta < 1:
                self.delta = 1
            self.initialize()
            self.stack = []

        def initialize(self):
            """for use by subclasses"""
            pass

                # partitioning rules

        def partition(self, shape):
            """for picking a dividing wall
            
            This method assumes that partitioning is into rectangles
            with sides parallel to the axes.

            Parameters:
                shape - a rectangle specified by (row,column) indices
                  in format [[r0,c0],[r1,c1]] where (r0,c0) is the
                  lower left corner and (r1,c1) is the upper right
                  corner.

            Preconditions:
                Both r1-r0 and c1-c0 is at least delta

            Returns:
                Two shapes and the indices of the door cells.
            """
            [[r0, c0], [r1, c1]] = shape      # a rectangle

            if r1 - r0 > c1 - c0:             # more rows than columns
                r2 = randint(r0 + 1, r1)          # partition row
                shape1 = [[r0, c0], [r2-1, c1]]
                shape2 = [[r2 ,c0], [r1, c1]]
                c2 = randint(c0, c1)
                door = [[r2-1, c2], [r2, c2]]
            else:
                c2 = randint(c0 + 1, c1)          # partition column
                shape1 = [[r0, c0], [r1, c2-1]]
                shape2 = [[r0 ,c2], [r1, c1]]
                r2 = randint(r0, r1)
                door = [[r2, c2-1], [r2, c2]]
            return (shape1, shape2, door)

                # sizing criteria

        def diameter(self, shape):
            """determine the diameter of the shape
            
            This method assumes that partitioning is into rectangles
            with sides parallel to the axes.

            Parameters:
                shape - a rectangle specified by (row,column) indices
                  in format [[r0,c0],[r1,c1]] where (r0,c0) is the
                  lower left corner and (r1,c1) is the upper right
                  corner.

            Returns:
                Tne smaller of the row width and the column width.
            """
            [[r0, c0], [r1, c1]] = shape
            delta1 = r1 - r0      # number of rows - 1
            delta2 = c1 - c0      # number of columns - 1
            return min(delta1, delta2) + 1

        def make_doorway(self, door):
            """determine the diameter of the shape
            
            This method assumes that partitioning is into rectangles
            with sides parallel to the axes.

            Parameters:
                door - a two-cell rectangle specified by (row,column)
                  indices.
            """
            [[r0, c0], [r1, c1]] = door
            cell = self.grid[r0, c0]
            nbr = self.grid[r1, c1]
            cell.makePassage(nbr)

                # carving small shapes

        def carve_shadow(self, shadow_grid):
            """carve a shadow maze"""

                # if delta is 1, then the required spanning tree is
                # a chain.  Sidewinder should be satisfactory for
                # small grids.

            algorithm = self.kwargs["algorithm"] \
                if "algorithm" in self.kwargs else Sidewinder
            algorithm.on(shadow_grid)

        def carve(self, shape):
            """carve a maze in the given partition
            
            This method assumes that partitioning is into rectangles
            with sides parallel to the axes.

            Parameters:
                shape - a rectangle specified by (row,column) indices
                  in format [[r0,c0],[r1,c1]] where (r0,c0) is the
                  lower left corner and (r1,c1) is the upper right
                  corner.
            """
            [[r0, c0], [r1, c1]] = shape
            shadow_maze = Rectangular_Grid(r1-r0+1, c1-c0+1)
            self.carve_shadow(shadow_maze)

                # get the edges in the shadow
            edges = {}
            for i in range(r0, r1+1):
                for j in range(c0, c1+1):
                    cell = shadow_maze[i-r0, j-c0]
                    for nbr in cell.passages():
                        edge = frozenset([cell, nbr])
                        edges[edge] = 1

                # carve the shadowed edges in the grid
            for edge in edges:
                cell, nbr = edge
                i, j = cell.index
                h, k = nbr.index
                cell = self.grid[i+r0, j+c0]
                nbr = self.grid[h+r0, k+c0]
                cell.makePassage(nbr)

                # when do we recurse? This is the heart of the
                # matter

        def decision_procedure(self, shape):
            """for determining what needs to be done

            Parameters:
                shape - e.g. a rectangle specified by (row,column)
                  indices in format [[r0,c0],[r1,c1]] where (r0,c0)
                  is the lower left corner and (r1,c1) is the upper
                  right corner.

            Returns:
                Two shapes and a door.  These are all None if the
                the shape is too small.
            """
                # decide what to do
            if self.diameter(shape) <= self.delta:
                    # e.g. single row or single column
                self.carve(shape)
                return (None, None, None)

                # returns (shape1, shape2, door)
            return self.partition(shape)

    @classmethod
    def on(cls, grid, state=None, **kwargs):
        """carve a spanning tree using recursive division

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            state - a state matrix (default=None)

        Optional arguments if state is None:
            delta - the diameter inferior (default: delta=1)
            algorithm - an algorithm for carving mazes in minimal
                partitions (default: algorithm=Sidewinder)
        """
        if not state:
            state = cls.State(grid, **kwargs)

        shape = [[0, 0], [grid.rows-1, grid.cols-1]]
        state.stack.append(shape)
        while state.stack:
            #print("POP: %s" % shape)
            shape = state.stack.pop()
            shape1, shape2, door = state.decision_procedure(shape)
            #print("PARTITION: %s, %s, %s" % (shape1, shape2, door))
            if door:
                state.make_doorway(door)
            if shape1:
                state.stack.append(shape1)
            if shape2:
                state.stack.append(shape2)

# ---------------------------------------------------------------------
# Additional state classes
# ---------------------------------------------------------------------

class Golden_State(Recursive_Division.State):
    """puts a few restrictions on the partitioning"""

    def initialize(self):
        """compute the partitioning bounds"""
        phi = (1+sqrt(5))/2       # golden section, mean-extreme ratio
        self.hi = phi - 1         # = 1/phi ≈ 0.618
        self.lo = 1 - self.hi     # ≈ 0.382
            # normal setting: golden=True
        self.kwargs["golden"] = \
            "golden" not in self.kwargs or self.kwargs["golden"]

    def partition(self, shape):
        """for picking a dividing wall

        This differs from the base class by insuring that the larger
        partition is either no wider or no taller than 0.618 times
        the original shape.
            
        This method assumes that partitioning is into rectangles
        with sides parallel to the axes.

        Parameters:
            shape - a rectangle specified by (row,column) indices in
              format [[r0,c0],[r1,c1]] where (r0,c0) is the lower left
              corner and (r1,c1) is the upper right corner.

        Preconditions:
            Both r1-r0 and c1-c0 are more than delta

        Returns:
            Two shapes and the indices of the door cells.
        """
        if not self.kwargs["golden"]:
                # simple partitioning if golden is False
            return super().partition(shape)

            # quasi-Fibonacci partitioning
        [[r0, c0], [r1, c1]] = shape      # a rectangle

        if r1 - r0 > c1 - c0:             # more rows than columns
            a = int(self.lo * (r1 - r0 + 1)) + 1
            b = int(self.hi * (r1 - r0 + 1))
            r2 = randint(a, b) if a<b else (r1 - r0 + 1) // 2
            r2 += r0                          # partition row
            shape1 = [[r0, c0], [r2-1, c1]]
            shape2 = [[r2 ,c0], [r1, c1]]
            c2 = randint(c0, c1)
            door = [[r2-1, c2], [r2, c2]]
        else:
            a = int(self.lo * (c1 - c0 + 1)) + 1
            b = int(self.hi * (c1 - c0 + 1))
            c2 = randint(a, b) if a<b else (c1 - c0 + 1) // 2
            c2 += c0                          # partition column
            shape1 = [[r0, c0], [r1, c2-1]]
            shape2 = [[r0 ,c2], [r1, c1]]
            r2 = randint(r0, r1)
            door = [[r2, c2-1], [r2, c2]]
        return (shape1, shape2, door)

class Random_Texture_State(Golden_State):
    """chooses random algorithms to carve mazes in minimal partitions

    The algorithm argument is ignored.  The default for delta is 5.

    The optional arguments are:
        algorithms - a list of algorithms to use for carving mazes
            in minimal partitions
        golden - if true, method "partition" works like the partitioning
            in Golden_State.  If false, it works like the partitioning
            in Recursive_Division.State.  (default: golden=False)
    """
    def initialize(self):
        """initializations"""
        if "algorithms" not in self.kwargs:
            from binary_tree import Binary_Tree
            from aldous_broder import Aldous_Broder
            from prims import Prims
            from recursive_backtracker import Recursive_Backtracker
            from hunt_and_kill import Hunt_and_Kill

            self.kwargs["algorithms"] = \
                [Binary_Tree, Sidewinder, Aldous_Broder, Prims, \
                    Recursive_Backtracker, Hunt_and_Kill]

            # normal setting: golden=False
        self.kwargs["golden"] = \
            "golden" in self.kwargs and self.kwargs["golden"]

            # require delta >= 2 (default delta=5)
        if self.delta < 2:
            self.delta = 5

    def carve_shadow(self, shadow_grid):
        """carve a shadow maze"""
        self.kwargs["algorithm"] = choice(self.kwargs["algorithms"])
        super().carve_shadow(shadow_grid)

# END: recursive_division.py
