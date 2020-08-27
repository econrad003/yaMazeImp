# -*- coding: utf-8 -*-
# multilevel_mst.py - minimum weight spanning tree algorithms for
#   multilevel mazes
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
#     18 Aug 2020 - Initial version
#     21 Aug 2020 - Kruskal's algorithm completed
#     26 Aug 2020 - Borůvka's algorithm completed
#           still needed: Prim's algorithm
"""
multilevel_mst.py - state classes for MST and growing tree algorithms
    for use with multilevel mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

A collection of State subclasses for use with multilevel mazes...
These provide ways of preconnecting existing stairwells in ways that
are compatible with the underlying algorithms.

Included are state classes for the following algorithms:

1. Kruskal's algorithm
    new_KruskalState(StateClass): cls -> cls

    typical usage:
        from kruskals import Kruskals
        from multilevel_mst import new_KruskalState
        StateSubclass = new_KruskalState(Kruskals.State)
        state = StateSubclass(grid)
        Kruskals.on(grid, state)

2. Borůvka's algorithm
    new_BoruvkaState(StateClass): cls -> cls

    typical usage:
        from boruvkas import Boruvkas
        from multilevel_mst import new_BoruvkaState
        StateSubclass = new_BoruvkaState(Boruvkas.State)
        state = StateSubclass(grid)
        Boruvkas.on(grid, state)

3. Prim's algorithm

    ------------------ TO DO! --------------------

Background:

    Kruskal's algorithm was developed by mathematician and scientist
    Joseph Kruskal in 1956. [1, page 158]

    Borůvka's algorithm was originally developed by Otakar Borůvka
    in 1926 for constructing an efficient electrical network in
    Moravia.  It was rediscovered several times: by Choquet (1938),
    Florek, Łukasiewicz et al (1951) and Sollin (1965).  It is
    sometimes called Sollin's algorithm. [2]

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] Wikipedia.  Borůvka's algorithm. Web, 17 December 2019.
        Accessed 26 March 2020.

Bugs:

    See discussion above.
  
    Issue #7 (affecting kruskals.py) affects KruskalState.add_weave().
    Code has been added to insure that stairwells are handled properly
    when connected a posteriori, but this is only a workaround.
"""

from random import random, shuffle, randint, choice

def add_shared_routines(StateClass):
    """add methods that are the the same in the various subclasses"""

    class Multilevel_Shared_State(StateClass):
        """contains shared multilevel maze preconfiguration methods"""

        def connect_a_stairwell(self, staircell):
            """attempt to connect a stairwell"""
                # not shared
            pass

        def connect_all_stairwells(self):
            """attempt to connect all stairwells"""
            for staircell in self.grid.stairs:
                self.connect_a_stairwell(staircell)

        def add_weave(self, cell, subgrid):
            """add a weave crossing before running the algorithm"""
                # note that subgrid is required
                # for Kruskal's algorithm, see issue #7
            return super().add_weave(cell, subgrid)

        def add_random_weaves(self, n=0):
            """attempt to add a number of weave crossings"""
            if n<1:
                n = len(self.grid)
            added = 0
            for m in range(n):
                subgrid = choice(self.grid.levels)
                i = randint(1, subgrid.rows-2)
                j = randint(1, subgrid.cols-2)
                cell = subgrid[i, j]
                if cell:
                    if self.add_weave(cell, subgrid):
                        added += 1
            return added

    return Multilevel_Shared_State

def new_KruskalState(Kruskal_State_Class):
    """create state class for Kruskal's algorithm for use with
          multilevel mazes

    Parameters:
        Kruskal_State_Class - a state class for Kruskal's algorithm

    Returns:
        a state subclass for Kruskal's algorithm
    """

    Shared_State = add_shared_routines(Kruskal_State_Class)

    class Multilevel_Kruskals_State(Shared_State):
        """a State object for multilevel mazes generated by
            Kruskal's algorithm"""

        def __init__(self, grid, crossings=None, connect_stairs=True):
            """constructor"""
            super().__init__(grid, crossings)

            if connect_stairs:
                    # connect the stairwells first (low weight edges!)
                    #
                    # note that connecting the stairwells will insure
                    # weaves don't conflict with stairwells
                self.connect_all_stairwells()

        def connect_a_stairwell(self, staircell):
            """attempt to connect a stairwell"""
            downcell = staircell["down"]
            upcell = staircell["up"]
            if self.ok_for_merge(staircell, downcell):
                self.merge(staircell, downcell)
            if self.ok_for_merge(staircell, upcell):
                self.merge(staircell, upcell)

    return Multilevel_Kruskals_State

def new_BoruvkaState(Boruvka_State_Class):
    """create state class for Borůvka's algorithm for use with
          multilevel mazes

    Parameters:
        Boruvka_State_Class - a state class for Borůvka's algorithm

    Returns:
        a state subclass for Borůvka's algorithm
    """

    Shared_State = add_shared_routines(Boruvka_State_Class)

    class Multilevel_Boruvkas_State(Shared_State):
        """a State object for multilevel mazes generated by
            Borůvka's algorithm"""

        def __init__(self, grid, crossings=None, connect_stairs=True):
            """constructor"""
            super().__init__(grid, crossings)

            if connect_stairs:
                    # connect the stairwells first (low weight edges!)
                    #
                    # note that connecting the stairwells will insure
                    # weaves don't conflict with stairwells
                self.connect_all_stairwells()

        def connect_a_stairwell(self, staircell):
            """attempt to connect a stairwell"""
                # if either end of the stairs has already been linked,
                # we need to make sure that linking the stairwell does
                # not create a circuit.

            downcell = staircell["down"]
            upcell = staircell["up"]

                # get component numbers
            kmid = self.cells[staircell]
            kdown = self.cells[downcell]
            kup = self.cells[upcell]
            if kdown is kup:
                    # connecting the stairwell would create a circuit
                return
            kleast = min(kmid, kdown, kup)

                # link the stairwell
            staircell.makePassage(downcell)
            staircell.makePassage(upcell)

                # join the components
            for k in [kdown, kup, kmid]:
                if k is kleast:
                    continue
                for cell in self.components[k]:
                    self.cells[cell] = kleast
                self.components[kleast] += self.components[k]
                del self.components[k]

    return Multilevel_Boruvkas_State

# END: multilevel_mst.py
