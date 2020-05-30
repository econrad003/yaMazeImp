# -*- coding: utf-8 -*-
##############################################################################
# moebius_grid.py - grid class for Moebius strip mazes with square tiles
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
#     24 Apr 2020 - EC - Initial version (adapted from cylinder_grid.py)
# Credits:
#     EC - Eric Conrad
##############################################################################
"""
moebius_grid.py - Moebius strip grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A Moebius strip maze is a maze with square cells (using the NSEW topology)
arranged in a rectangle in which one pair of opposite sides have been
'glued' together with one twist.  Note that 'north' and 'south' are only
meaninful when the strip is unglued.  When the strip is glued, there is
a single edge.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from square_cell import Square_Cell
from cylinder_grid import Cylinder_Grid

class Moebius_Grid(Cylinder_Grid):
    """Moebius grid implementation"""
    
        ###
        # Initialization
        ###
        #   essentially as for parent class Rectangular_Grid...
        #
        #   The difference is that the east boundary is 'twisted' and
        #   and then 'glued' to the west boundary.  After gluing, the
        #   strip has just one edge.  A compass won't work on a Moebius
        #   strip.
        #
        #   We handle this gluing using the indexing.

    def __getitem__(self, index):
        """get cell by index
        
        The east and west boundaries are glued together with a twist.
        """
        i, j = index          # unpack coordinates
            # twist and glue
        j %= 2*self.cols
        if j >= self.cols:
            i = self.rows - i - 1   # twist
            j -= self.cols          # glue
        index = i, j          # pack coordinates
        return super().__getitem__(index)

    def __setitem__(self, index, cell):
        """set cell by index
        
        The east and west boundaries are glued together.
        """
        i, j = index          # unpack coordinates
            # twist and glue
        j %= 2*self.cols
        if j >= self.cols:
            i = self.rows - i - 1   # twist
            j -= self.cols          # glue
        index = i, j          # pack coordinates
        return super().__setitem__(index, cell)

# END: Moebius_grid.py
