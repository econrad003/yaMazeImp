# -*- coding: utf-8 -*-
# square_cell.py - square cell class for rectangular mazes
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
#     21 Apr 2020 - Initial version
"""
square_cell.py - square cell implementation for rectangular mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Description:

    Standard square cells are (obvious) square in shape.  In addition,
    their sides are parallel to the coordinate axes.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    1. Parameters are not validated.
"""

from cell import Cell

class Square_Cell(Cell):
    """square cell implementation"""

    def __init__(self, row, col, **kwargs):
        """constructor

        Mandatory arguments:
            row, col - the cell's row and column in the parent grid

        Optional named arguments:
            name - a name for the cell
            position - (x, y)-position of the center of the cell;
              the default position is (col, row)
            scale - larger than 0 - a scaling factor; the default is 1
            inset - a value in [0,1) - the default is 0
        """
            # initialize the base
        index = (row, col)
        super().__init__(index, **kwargs)

        self.position = kwargs["position"] if "position" in kwargs else index
        self.scale = kwargs["scale"] if "scale" in kwargs else 1
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

# END: square_cell.py
