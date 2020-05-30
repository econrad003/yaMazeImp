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
#     23 Apr 2020 - Initial version
#     3 May 2020 - Remove tweaked algorithms
##############################################################################
"""
cylinder_grid.py - cylindrical grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A cylindrical maze is a maze with square cells (using the NSEW topology)
arranged in a rectangle in which one pair of opposite sides have been
'glued' together with no twists.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

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
            # pylint: disable=arguments-differ
            #     reason: added column_offsets as an optional parameter
            #         as there are no natural column bounds in the
            #         cylinder topology)
        if not column_offsets:
            column_offsets = [0] * self.rows
        for i in range(self.rows):
            L = []
            for j in range(self.cols):
                L.append(self[i, j+column_offsets[i]])
            yield L

    def each_column(self, column_offsets=None):
        """iterate column by column"""
            # pylint: disable=arguments-differ
            #     reason: added column_offsets as an optional parameter
            #         as there are no natural column bounds in the
            #         cylinder topology)
        if not column_offsets:
            column_offsets = [0] * self.rows
        for j in range(self.cols):
            L = []
            for i in range(self.rows):
                L.append(self[i, j+column_offsets[i]])
            yield L

    def each_rowcol(self, column_offsets=None):
        """iterate by row and column (row major order)"""
            # pylint: disable=arguments-differ
            #     reason: added column_offsets as an optional parameter
            #         as there are no natural column bounds in the
            #         cylinder topology)
        if not column_offsets:
            column_offsets = [0] * self.rows
        for i in range(self.rows):
            for j in range(self.cols):
                yield self[i, j+column_offsets[i]]

    def each_colrow(self, column_offsets=None):
        """iterate by column and row (column major order)"""
            # pylint: disable=arguments-differ
            #     reason: added column_offsets as an optional parameter
            #         as there are no natural column bounds in the
            #         cylinder topology)
        if not column_offsets:
            column_offsets = [0] * self.rows
        for j in range(self.cols):
            for i in range(self.rows):
                yield self[i, j+column_offsets[i]]

# END: cylinder_grid.py
