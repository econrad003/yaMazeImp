# -*- coding: utf-8 -*-
# stairwell_cell.py - up-down cell class for multi-level mazes
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
#     14 Aug 2020 - Initial version
"""
stairwell_cell.py - up-down cell class for multi-level mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

This cell has two grid neighbors, an upcell and a downcell.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown
"""

from cell import Cell

class Stairwell_Cell(Cell):
    """class for up-down cells in multi-level mazes"""

    def __init__(self, index, downcell, upcell, **kwargs):
        """constructor

        Mandatory arguments:
            index - the cell's index in the parent grid
            upcell - the cell at the top of the stairs
            downcell - the cell at the bottom of the stairs

        Optional named arguments:
            name - a name for the cell

        If upcell or downcell is None, the grid object is responsible
        for configuring the neighborhood.  This can be done by calling
        configure.
        """
        super().__init__(index, **kwargs)
        self.kwargs["stairwell"] = 1
        self.configure(downcell, upcell)

    def configure(self, downcell, upcell):
        """configure a stairwell"""

            # configure the cell's neighborhood
        self.topology["down"] = downcell
        if downcell:
            downcell.topology["up"] = self

        self.topology["up"] = upcell
        if upcell:
            upcell.topology["down"] = self

# END: stairs_cell.py
