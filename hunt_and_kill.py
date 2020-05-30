# -*- coding: utf-8 -*-
# hunt_and_kill.py - the hunt and kill algorithm
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
#     1 May 2020 - Initial version
"""
hunt_and_kill.py - the hunt and kill algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Hunt and Kill Algorithm:

    (1) Kill mode: perform a random walk stepping only on unvisited cells.
        The walk ends when we reach a cell with no unvisited neighbors.
        Carve passages to make the path that results part of the maze.

    (2) Hunt mode: Scan the unvisited cells for a cell adjacent to a
        visited cell.  Carve a passage from this cell to a visited neighbor.
        Resume kill mode starting with this cell.

    The algorithm terminates when all cells have been visited.

    (Our version of the algorithm works on disconnected grids.)

Prerequisites:

    This algorithm works on any connected grid.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Yiping Hu, Russell Lyons and Pengfei Tang.  A reverse Aldous/Broder
        algorithm.  Preprint.  Web: arXiv.org.  24 Jul 2019.
            http://arxiv.org/abs/1907.10196v1

Bugs:

    See discussion above.
"""

class Hunt_and_Kill:
    """implementation of the Hunt and Kill algorithms"""

    @classmethod
    def on(cls, grid, start=None):
        """carve a spanning tree maze using the hunt and kill algorithm"""
        import random

                # start somewhere
        unvisited = []
        for cell in grid.each():
            unvisited.append(cell)
        random.shuffle(unvisited)

        cell = start if start else grid.choice()
        unvisited.remove(cell)

        while unvisited:
                    # Kill phase
            nbrs = []
            for nbr in list(cell.neighbors()):
                if nbr in unvisited:
                    nbrs.append(nbr)
            if nbrs:                      # unvisited neighbors
                nbr = random.choice(nbrs)
                cell.makePassage(nbr)
                cell = nbr
                unvisited.remove(cell)
                continue

                    # Hunt phase
            found = False
            for item in unvisited:
                cell = item                   # candidate
                nbrs = []
                for nbr in list(cell.neighbors()):
                    if nbr not in unvisited:
                        nbrs.append(nbr)
                if nbrs:                  # visited neighbors
                    nbr = random.choice(nbrs)
                    cell.makePassage(nbr)
                    unvisited.remove(cell)
                    found = True
                    break                 # success!
            if found:
                continue
            if not unvisited:
                break                     # no unvisited cells
            cell = unvisited.pop()        # disconnected grid

# END: hunt_and_kill.py
