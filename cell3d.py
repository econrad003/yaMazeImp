# -*- coding: utf-8 -*-
# cell3d.py - cubic cell class for three-dimensional oblong mazes
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
#     1 Sep 2020 - Initial version
"""
cell3d.py - cubic cell implementation for three-dimensional oblong mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Description:

    Standard cubic cells are (obvious) cubes in shape.  In addition,
    their sides are parallel to the coordinate axes.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    1. Parameters are not validated.
"""

from cell import Cell

class Cell3D(Cell):
    """square cell implementation"""

    def __init__(self, row, col, level, **kwargs):
        """constructor

        Mandatory arguments:
            row, col - the cell's row and column in the parent grid
            level - the level plane number (in a list)

        Optional named arguments:
            name - a name for the cell
            position - (x, y, z)-position of the center of the cell;
              the default position is (col, row, level);
              the last coordinate must be a non-negative integer.
            scale - larger than 0 - a scaling factor; the default is 1
            inset - a value in [0,1) - the default is 0

        For a typical three-dimensional maze, the level is the height
        above the x-y coordinate plane. Level 0 is the x-y coordinate
        plane.

        For mazes of dimension greater than three, there should be a
        bijection which maps the higher dimensional coordinates into
        a level number.

        For example, to map four-dimensional rectangular coordinates
        (x, y, z, w) into three-dimensional rectangular coordinates
        (p, q, r), assuming 0 ≤ w ≤ m and 0 ≤ z, the following map will
        suffice:

            p := x
            q := y
            r := mz + w

        To invert the map:

            x := p
            y := q
            z := r // m 
            w := r % m

        In a typical layout, the third and last coordinate (e.g. r)
        identifies the axes object containing the cell's level plane in
        an array of axes objects.
        """
            # initialize the base
        entry = level[:]
        entry.insert(0, col)
        entry.insert(0, row)
        index = tuple(entry)      # tuple
        self.level = level[:]     # list
        super().__init__(index, **kwargs)

        xy = (col, row)
        self.position = kwargs["position"] if "position" in kwargs else xy
        self.scale = kwargs["scale"] if "scale" in kwargs else 1
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

# END: cell3d.py
