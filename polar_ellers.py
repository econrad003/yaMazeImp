# -*- coding: utf-8 -*-
# polar_ellers.py - Eller's tapestry spanning tree algorithm adapted
#     for polar mazes
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
#     27 Aug 2020 - Initial version
"""
polar_ellers.py - Eller's tapesty spanning tree algorithm adapted for
    polar mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

This package provides a state subclass Polar_Eller_State for
use with the implementation of Eller's Algorithm.

Background:

    Eller's algorithm was developed by Marlin Eller in 1982.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from random import random, shuffle, randint
from ellers import Ellers

class Polar_Ellers_State(Ellers.State):
    """an object which holds the algorithm's current state"""

    def configure(self):
        """subclass configuration"""
        pass

    def next_row(self):
        """get the edges in the next row of the grid

        This overrides the rectangular grid topology.
        Here we assume polar grid topology.
        """
        i = self.row
        self.row += 1

        rowEdges = []
        colEdges = []

            # get edges in the current row
        for u in self.grid.latitude[i]:
            v = u["ccw"]      # corresponds to East/West (row)
            if v:
                rowEdges.append(frozenset([u, v]))

            # get outward edges
        if i+1 in self.grid.latitude:
            for v in self.grid.latitude[i+1]:
                u = v["inward"]   # corresponds to North/South (column)
                if u:
                    colEdges.append(frozenset([u, v]))

        if rowEdges:
            shuffle(rowEdges)
        if colEdges:
            shuffle(colEdges)
        return (rowEdges, colEdges)

# END: polar_ellers.py
