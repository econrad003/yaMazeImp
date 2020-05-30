# -*- coding: utf-8 -*-
# aldous_broder.py - the Aldous-Broder algorithm
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
aldous_broder.py - the Aldous-Broder algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

First-Entrance Algorithm [1]:

    We perform a random walk of the entire grid.  Whenever we first arrive
    at a cell, we carve a passage from that cell to its predecessor in the
    walk.

Last-Exit Algorithm [2]:

    We again perform a random walk of the entire grid, this time keeping
    track of the most recent predecessor (i.e. the last exit to) for each
    cell.  When the walk is complete, we carve passages from each cell to
    its most recent predecessor.

    This is also known as "reverse Aldous/Broder".

Prerequisites:

    These algorithms work on any connected grid.  With a bad random sequence,
    one or the other might never terminate.

Remarks:

    Given a true uniform random number generator, these algorithms are
    unbiased in the sense that every spanning tree is generated with equal
    probability.  (Of course the pseudorandom number generator used here
    is not truly random.)

    According to [1], the algorithm is due to David Aldous (UC Berkeley) and,
    independently, to Andrei Broder (Google).

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Yiping Hu, Russell Lyons and Pengfei Tang.  A reverse Aldous/Broder
        algorithm.  Preprint.  Web: arXiv.org.  24 Jul 2019.
            http://arxiv.org/abs/1907.10196v1

Bugs:

    See discussion above.
"""

class Aldous_Broder:
    """implementation of the Aldous-Broder algorithms"""

    @classmethod
    def on(cls, grid, start=None):
        """carve a spanning tree maze using Aldous-Broder
        (random walk first entrance algorithm)

        Preconditions:
            The grid must be connected.

        Arguments:
            grid - a grid
            start - a starting cell - if none is specified, we choose
                a cell at random
        """
        import random

                # start somewhere
        cell = start if start else grid.choice()
        unvisited = len(grid) - 1

        while unvisited:
                    # go somewhere
            nbr = random.choice(list(cell.neighbors()))

            if not nbr.arcs:              # not yet visited
                unvisited -= 1
                cell.makePassage(nbr)

            cell = nbr                    # continue the random walk

    @classmethod
    def reverse_on(cls, grid, start=None):
        """carve a spanning tree maze using reverse Aldous-Broder
        (random walk last exit algorithm)

        Preconditions:
            The grid must be connected.

        Arguments:
            grid - a grid
            start - a starting cell - if none is specified, we choose
                a cell at random
        """
        import random

        last_exit = {}
        unvisited = len(grid) - 1

                # start somewhere
        cell = start if start else grid.choice()

                # random walk
        while unvisited:
                    # go somewhere
            nbr = random.choice(list(cell.neighbors()))
            last_exit[cell] = nbr
            if nbr not in last_exit:          # not yet visited
                unvisited -= 1
            cell = nbr                    # continue the random walk

                # passage carving
        for cell in last_exit:
            cell.makePassage(last_exit[cell])

# END: aldous_broder.py
