# -*- coding: utf-8 -*-
# di_aldous_broder.py - the directed Aldous-Broder algorithm
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
#     26 Sep 2020 - Initial version
"""
di_aldous_broder.py - the directed Aldous-Broder algorithm
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

In the directed version, the carving is unidirectional, with the carved
passages directed so that all paths either lead to the starting cell or
all paths lead away from the starting cell. 

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

from random import choice

class Directed_Aldous_Broder:
    """implementation of the Aldous-Broder algorithms"""

    class State(object):
        """the state matrix for the algorithm"""

        def __init__(self, grid, start_cell=None, last_exit=False):
            """constructor"""
            if not start_cell:
                start_cell = grid.choice()
                    # the grid instance is no longer needed
            self.start_cell = start_cell
            self.last_exit = last_exit
 
        @staticmethod
        def component_of(start_cell):
            """breadth-first search to identify the component

            BFS is used to insure every unvisited cell is reachable
            """
            queue = [start_cell]
            component = set([])
            while queue:
                cell = queue.pop(0)
                if cell not in component:
                    component.add(cell)
                    queue += cell.neighbors()
            return component

        def carve(self, cell, nbr, away):
            """carve a directed passage"""
            if nbr is self.start_cell:
                return
            if away:
                cell.makePassage(nbr, twoWay=False)
            else:
                nbr.makePassage(cell, twoWay=False)

        def run(self, away):
            """one pass of the algorithm"""
            walk = {}
            cell = self.start_cell
                # Note: Aldous-Broder will never terminate if an
                #     unvisited cell is unreachable from start.
            unvisited = self.component_of(cell)
            unvisited.discard(cell)

            alg = "last exit" if self.last_exit else "first entrance"
            print("\trandom walk (%s)..." % alg)
            while unvisited:
                nbr = choice(cell.neighbors())
                unvisited.discard(nbr)
                    # here we choose the version of the algorithm
                if self.last_exit:    # LAST-EXIT
                    walk[cell] = nbr      # last exit from current cell
                elif nbr not in walk: # FIRST-ENTRANCE
                    walk[nbr] = cell      # first entrance to neighbor
                cell = nbr

            print("\tprocess walk...")
            if self.last_exit:
                for cell in walk:
                    nbr = walk[cell]
                    self.carve(cell, nbr, away)
            else:
                for nbr in walk:
                    cell = walk[nbr]
                    self.carve(cell, nbr, away)

    @classmethod
    def on(cls, grid, towards, start_cell=None, state=None,
           last_exit=False):
        """carve a spanning tree maze using Aldous-Broder
        (random walk first entrance algorithm)

        Required Arguments:
            grid - a grid
            towards - a direction ("towards", "away", "both")

        Optional arguments:
            start_cell - a cell (if none is specified, we choose
                one at random)
            state - if none is given, one is created
            last_exit:
                True - use the last exit algorithm
                False - use the first entrance algorithm

        Only the first letter of the towards string is used.

        If start_cell is given, the grid is never used as the
        list of unvisited cells is built from the start_cell.

        If the state is given, only the towards string is used.

        The grid argument is required even if it is never used.
        If a starting cell or a state is supplied, grid can be
        given as None.
        """
        if not state:
            state = cls.State(grid, start_cell, last_exit)

        towards = towards[0]
        if towards == 'a':
            state.run(True)
        elif towards == 't':
            state.run(False)
        else:     # assume two ways
            state.run(True)
            state.run(False)
        return state.start_cell

# END: di_aldous_broder.py
