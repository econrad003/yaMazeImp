# -*- coding: utf-8 -*-
# polar_cell.py - polar cell class for mazes
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
#     31 May 2020 - Initial version
"""
polar_cell.py - polar cell implementation for mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Description:

    Polar cells are sectors of circles, in most cases, bounded by two
    circular arcs and two radial vectors, all with th same center.  The
    two special cases are (1) a pole cell, a disk centered at the pole,
    bounded by a circle, and (2) cells incident to the pole, wedges bounded
    by a single circular arc and two radial vectors.  The latter may be
    viewed as degenerate cases of the main type.  Pole cells can be viewed
    as a degenerate case of a cell incident at the pole.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from cell import Cell

class Polar_Cell(Cell):
    """polar cell implementation"""

    def __init__(self, index, directions, outwards, celltype, **kwargs):
        """constructor

        Mandatory arguments:
            index - the cell's index in the parent grid
            directions - a list of labels (strings) for the directions,
              for example, ['ccw', 'cw', 'inward', 'outward1', 'outward2'].
              The names 'ccw', 'cw', and 'inward' are treated as
              reserved.  Any other name is assumed to be an outward wall.
            outwards - the number of outward walls
            celltype - parameters describing the geometry of the cell.
              There are three formats:
                      ('circle', r) - a circle of radius r centered at the
                          pole;
                      ('wedge', r, theta1, theta2) - a wedge of radius r
                          subtending an arc from theta1 to theta2
                      ('sector', r1, r2, theta1, theta2) - a sector
                          subtending the area in wedge(r2, theta1, theta2)
                          that is not in wedge(r1, theta1, theta2)
              The types 'circle' and 'wedge' respesent degenerate
              types (1) and (2) as described in the preamble.

        Optional named arguments:
            name - a name for the cell
            inset - a value in [0,1) - the default is 0
        """
            # initialize the base
        super().__init__(index, **kwargs)

        self.directions = directions
        self.outwards = outwards
        self.celltype = celltype
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

# END: polar_cell.py
