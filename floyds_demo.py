#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# floyds_demo.py - test the Floyd-Warshall algorithm implementation
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
##############################################################################
# Maintenance History:
#     10 Sep 2020 - Initial version
##############################################################################
"""
floyds_demo.py - test the Floyd-Warshall algorithm implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Background:

    The Floyd-Warshall algorithm was developed independently by Robert
    Floyd in 1962, Bernard Roy in 1959, and Stephen Wasrhall in 1962.
    The triple loop formulation was described by Peter Ingerman, also
    in 1962.  The algorithm is closely related to Kleene's 1956
    algorithm for converting a DFA (deterministic finite automaton) into
    a regular expression.

References:

    [1] Wikipedia.  "Floyd-Warshall algorithm." 23 August 2020. Web,
        accessed 9 September 2020.

Bugs:

    Unknown, but the algorithm technically fails if the maze has negative
    weight cycles.  It does however fail safely in this case and can actually
    be used to detect negative weight cycles.
"""

    # pylint: disable=redefined-outer-name
    #     reason: grid, m and n are standard names for these variables

from layout_plot import Layout
from floyds import Floyds

def make_rectangular_maze(m, n, maze_name):
    """create a maze"""
    from rectangular_grid import Rectangular_Grid
    from hunt_and_kill import Hunt_and_Kill

    print("Create grid %s - %d rows, %d columns" % (maze_name, m, n))
    grid = Rectangular_Grid(m, n, name=maze_name)

    print("Carve maze %s - hunt and kill algorithm" % maze_name)
    Hunt_and_Kill.on(grid)
    return grid

def run_floyds(maze):
    """run the Floyd-Warshall algorithm and return the state"""
    print("Floyd-Warshall - maze %s" % maze.name)
    print("  -- be patient, running time is cubic!")
    state = Floyds.on(maze)
    print(" -- completed!")
    return state

def diagnose(floyds_state):
    """display diagnostic results"""
    print("Diagnostics:")
    maze = floyds_state.grid
    negwgt = False
    if floyds_state.query_negative_cycles():
        print("There is at least one negative weight cycle in %s." % \
            maze.name)
        negwgt = True
    u = maze.choice()
    print("Random cell u: index=%s" % str(u.index))
    if floyds_state.query_all_reachable_from(u):
        print("  1) All cells are reachable from the chosen cell.")
    else:
        print("  1) Some cells are not reachable from the chosen cell.")
    if floyds_state.query_reachable_from_all(u):
        print("  2) The chosen cell is reachable from all cells.")
    else:
        print("  2) The chosen cell is not reachable from somewhere.")

    if floyds_state.query_connected():
        print("The directed maze is connected.  " \
            + "All cells are reachable from anywhere.")
    else:
        print("The directed maze is disconnected.  " \
            + "There is a pair of cells with no connecting path.")

    w = maze.choice()
    print("Random cell w: index=%s" % str(w.index))

    path, weight = floyds_state.shortest_path(u, w)
    if path:
        foo = "path" if negwgt else "minimum weight path"
        print("There is a %s from u to w of weight %f." \
            % (foo, weight))
        print("Its length is %d." % (len(path)-1))
        if negwgt:
            print(("Since %s has a negative weight cycle, " \
                + "this might not be minimal") % maze.name)
        newpath = []
        for v in path:
            newpath.append(v.index)
        newpath[0] = "u"
        newpath[-1] = "w"
        print(newpath)
    else:
        print("There is no path from u to w.")

def test1(args):
    """a simple test to see if Floyd-Warshall is working"""
    m, n = args.dim
    name = "TEST1-Hunt_and_kill"
    maze = make_rectangular_maze(m, n, "TEST1-HuntKill")
    state = run_floyds(maze)
    diagnose(state)
    print(" ------------ Diagnostics --------------------------------------")
    print(" -- Verify above that path weight = path length.")
    assert not state.query_negative_cycles(), \
        "There should be no negative weight cycles in " + name + "."
    assert state.query_connected(), "The maze " + name + " should be connected."
    print(" ------------ Successful completion! ---------------------------")

def main(args):
    """main entry point"""
    print(args)
    if not args.skip1:
        test1(args)

if __name__ == "__main__":
    import argparse

    desc = "Floyd-Warshall algorithm demonstration"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--dim', metavar=('ROWS', 'COLS'), type=int, \
        nargs=2, default=[20,30], \
        help="the number of rows and columns (default='20 30')")
    parser.add_argument('--skip1', action='store_true',
        help="skip the first test (Floyd's on a hunt and kill maze)")

    args = parser.parse_args()
    main(args)

# END: floyds_demo.py
