# -*- coding: utf-8 -*-
# complete_maze.py - create a complete relative maze on a grid
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
#     2 Sep 2020 - Initial version
"""
complete_maze.py - complete relative maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

This script is mainly for testing grids.  It makes a list
of all grid edges and arcs and then links them.

Bugs and Features:

    Unknown
"""

class Complete_Maze:
    """implementation of the complete maze algorithm"""

    @classmethod
    def on(cls, grid):
        """carve a complete maze from a grid"""
        arcs = {}
        edges = {}
                # identify the arcs and edges
        print("  -- studying the grid...")
        for cell in grid.each():
            nbrs = cell.neighbors()
            for nbr in nbrs:
                arc = (cell, nbr)
                arcs[arc] = 1
                back_arc = (nbr, cell)
                if back_arc in arcs:
                    edge = frozenset([cell, nbr])
                    edges[edge] = 1

            # add in the edges
        e = len(edges)
        de = len(arcs) - 2*e
        print("  -- %d edges and %d directed arcs" % (e, de))
        for edge in edges:
            u, v = edge
            u.makePassage(v)
            arc = (u, v)
            del arcs[arc]
            arc = (v, u)
            del arcs[arc]

            # add in the directed arcs
        assert len(arcs) == de, "incorrect arc count"
        for arc in arcs:
            u, v = arc
            u.makePassage(v, twoWay=False)

# END: complete_maze.py
