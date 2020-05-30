# -*- coding: utf-8 -*-
# polygonal_cell.py - polygonal cell class for mazes
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
#     27 May 2020 - Initial version
"""
polygonal_cell.py - polygonal cell implementation for mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Description:

    Polygonal cells are (obviously) polygonal in shape.  In addition, they
    are convex.  They are not necessarily regular.  While standard square
    cells have a straighforward NSEW orientation, this is not in general 
    true for polygonal cells.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from cell import Cell

class Polygonal_Cell(Cell):
    """polygonal cell implementation
    
    With non-square cells, the cells of a maze will typically have either more
    than one shape (as in upsilon [octagon-square] mazes) or more than one
    orientation (as in delta [triangle] mazes and in sigma [hexagon] mazes).

    In a typical implementation, a grid class might create polygonal cells of 
    two or more subclasses.
    """

    def __init__(self, index, directions, walls, **kwargs):
        """constructor

        Mandatory arguments:
            index - the cell's index in the parent grid
            directions - a list of labels for the directions,
              for example, ['E', 'NW', 'S']
            walls - the vertices of the polygon

            If the outward directions are ['E', 'NW', 'S'] and the vertices
            are [P, Q, R], where P=(1,0), Q=(1,1) and R=(0,0), then the walls
            are respectively: 'E':PQ, 'NW':QR and 'S':RP.  Directions and
            walls may be given simultaneously either counterclockwise (as 
            in this example) or clockwise. The coordinates of the vertices
            may be integers or floats.

        Optional named arguments:
            name - a name for the cell
            inset - a value in [0,1) - the default is 0
        """
            # initialize the base
        super().__init__(index, **kwargs)

        self.directions = directions
        self.walls = walls
        self.inset = kwargs["inset"] if "inset" in kwargs else 0

# END: polygonal_cell.py
