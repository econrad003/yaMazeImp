#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# multilevel_mst_demo.py - multilevel maze demonstration program -
#     generate mazes using minimal spanning tree and growing tree
#     algorithms
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
#     20 Aug 2020 - Initial version
"""
multilevel_mst_demo.py - multilevel maze demonstration program
    (generate multilevel mazes using minimal spanning tree and
    growing tree algorithms)
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

import matplotlib.pyplot as plt

# from rectangular_grid import Rectangular_Grid
from layout_plot_multilevel import \
    Multilevel_Layout, Multilevel_Projective_Layout
from layout_plot_color import Color_Layout

def render(args, grid, LayoutType, fig, axs):
    """plot the result"""
          # create the primary layout
    print("Creating the layout objects")
    ax = axs[-1]
    MultiLayoutType = Multilevel_Projective_Layout if args.projective \
        else Multilevel_Layout
    layout = MultiLayoutType(grid, plt, figure=(fig, ax))
    ax.title.set_text("schematic")
    ax.axis("off")

    levels = len(grid.levels)
    for level in range(levels):
        subgrid = grid.levels[level]
        ax = axs[level]
        sublayout = layout.add_layout_for_grid(subgrid, plt, \
            Color_Layout, figure=(fig, ax))
        ax.title.set_text(subgrid.name)
        ax.axis("off")

        if level == 0:
            sublayout.palette[1] = "red"
            sublayout.color[subgrid[0,0]] = 1
        elif level + 1 == levels:
            sublayout.palette[1] = "green"
            m, n = subgrid.rows-1,subgrid.cols-1
            sublayout.color[subgrid[m, n]] = 1

    layout.draw_grid()
    return layout

def create_grid(args):
    """create the grid"""
    from rectangular_grid import Rectangular_Grid
    from weave_grid import Preweave_Grid
    from multilevel_grid import Multilevel_Grid

    subgrids = []
    m, n = args.dim
    for level in range(args.levels):
        subgrid = Preweave_Grid(m, n) if args.weave \
            else Rectangular_Grid(m, n, inset=0.15)
        subgrids.append(subgrid)
        subgrid.name = "Floor #" + str(level) if level \
            else "Ground Floor"

    grid = Multilevel_Grid()
    for subgrid in subgrids:
        grid.add_grid(subgrid)
    return grid

def add_stairs_to_level(args, grid, level):
    """add stairwells to a level"""
    to_build = args.stairwells
    retries = 10
    subgrid = grid.levels[level]
    while to_build > 0 and retries > 0:
        downcell = subgrid.choice()
        if downcell["down"] or downcell["up"]:
                # there is already a stairwell here
            retries -= 1
            continue
        grid.add_stairs_upward(level, downcell)
        to_build -= 1

    if to_build > 0:
        print("WARNING: too many random hash collisions...")
        print("  -- Unable to build %d stairwells at level %d..." \
            % (to_build, level))
        print("  -- %d of %d stairwells built up from level %d." \
            % (args.stairwells - to_build, args.stairwells, level))

def force_stairwell_weaves(args, state):
    """attempt to force weaves at stairwell landings"""
    if args.weave:
        print("  -- forced weaves")
        added = 0
        rejects = 0
        grid = state.grid
        for staircell in grid.stairs:
            level = grid.stairs[staircell]  # lower level
            subgrid = grid.levels[level]
            landingcell = staircell["down"]
            if state.add_weave(landingcell, subgrid):
                added += 1
            else:
                rejects += 1
            level += 1                      # upper level
            subgrid = grid.levels[level]
            landingcell = staircell["up"]
            if state.add_weave(landingcell, subgrid):
                added += 1
            else:
                rejects += 1
        print("     %d added weaves (%d rejected)" % (added, rejects))
    if not args.disconnect:
        print("  -- connect stairs (no circuits)")
        state.connect_all_stairwells()

def boruvka_maze(args, maze):
    """Generate a multilevel maze using Borůvka's algorithm"""
    from boruvkas import Boruvkas
    from multilevel_mst import new_BoruvkaState

    print("Borůvka's algorithm...")
    print("  -- state matrix")
    StateSubclass = new_BoruvkaState(Boruvkas.State)
    connect = not args.disconnect and not args.force
    if connect:
        print("  -- connect stairwells")
    state = StateSubclass(maze, connect_stairs = connect)

    if args.force:
        force_stairwell_weaves(args, state)

    if args.weave:
        grid_len = len(maze)
        added = state.add_random_weaves()
        density = added / grid_len
        print("%d weaves added (weave density = %f)" \
            % (added, density))

    print("  -- create the minimal spanning tree")
    Boruvkas.on(maze, state)

def kruskal_maze(args, maze):
    """Generate a multilevel maze using Kruskal's algorithm"""
    from kruskals import Kruskals
    from multilevel_mst import new_KruskalState

    print("Kruskal's algorithm...")
    print("  -- state matrix")
    StateSubclass = new_KruskalState(Kruskals.State)
    connect = not args.disconnect and not args.force
    if connect:
        print("  -- connect stairwells")
    state = StateSubclass(maze, connect_stairs = connect)

    if args.force:
        force_stairwell_weaves(args, state)

    if args.weave:
        grid_len = len(maze)
        added = state.add_random_weaves()
        density = added / grid_len
        print("%d weaves added (weave density = %f)" \
            % (added, density))

    print("  -- create the minimal spanning tree")
    Kruskals.on(maze, state)

def algorithm_help(args, algorithms):
    """display the algorithm help"""
    if args.algorithm != 'help':
        print("Algorithm '%s' is not recognized by this script." \
                % args.algorithm)
    print("Here are the recognized algorithms:")
    print("%-20s %-50s" % ('name', 'description'))
    print("-" * 71)
    for name in algorithms:
        desc = algorithms[name][1]
        print("%-20s %s" % (name, desc))

def set_basename(args):
    """basename for the rendered plot"""
    if args.basename:
        return args.basename

    basename = "multilevel_mst"
    basename += "_" + args.algorithm
    if args.weave:
        basename += "_weave"
    if args.disconnect:
        basename += "_x"
    if args.force and args.weave:
        basename += "_f"
    basename += "_demo"
    return basename

def main(args):
    """Generate a maze"""
    algorithms = {}
    algorithms['boruvka'] = [boruvka_maze, "Borůvka's algorithm"]
    algorithms['kruskal'] = [kruskal_maze, "Kruskal's algorithm"]

    if args.algorithm not in algorithms:
        algorithm_help(args, algorithms)
        return

            # create the grid
    maze = create_grid(args)

            # add the stairwells
    levels = args.levels
    for level in range(levels-1):
        add_stairs_to_level(args, maze, level)

            # carve the maze
    f = algorithms[args.algorithm][0]
    f(args, maze)

            # render the plot
    fig, axs = plt.subplots(1, levels+1)
    layout = render(args, maze, Color_Layout, fig, axs)
    basename = set_basename(args)
    layout.render("demos/" + basename + ".png")

    if args.show:
        plt.show()

if __name__ == "__main__":
    import argparse

    desc = "Generate multilevel mazes using minimal spanning tree" \
        + " and growing tree\nalgorithms.  The levels can be either" \
        + " rectangular grids or weave grids."
    parser = argparse.ArgumentParser( \
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description=desc)
    parser.add_argument('-W', '--weave', action='store_true', \
        help='create a weave maze (default: rectangular grid)')
    parser.add_argument('-d', '--dim', metavar=('ROWS', 'COLS'), \
        nargs=2, default=[18, 8], type=int, \
        help='the numbers of rows and columns in each level')
    parser.add_argument('-l', '--levels', metavar='LEVELS', \
        default=3, type=int, \
        help='the number of levels in the maze')
    parser.add_argument('-s', '--stairwells', metavar='STAIRWELLS', \
        default=2, type=int, \
        help='the number of stairwells between consecutive floors')
    parser.add_argument('-p', '--projective', action='store_true',
        help='use the perspective projection in the schematic')
    parser.add_argument('--show', action='store_true',
        help='display the figure before exiting')
    parser.add_argument('--basename', metavar='LAYOUT', \
        default=None, \
        help='an optional name for the output')
    parser.add_argument('-a', '--algorithm', type=str, \
        default="kruskal", \
        help='the algorithm to use (default: kruskal) or "help"')
    parser.add_argument('--disconnect', action='store_true',
        help='leave stairwells unlinked in preprocessing')
    parser.add_argument('--force', action='store_true',
        help='attempt to force weaves at stairwells')
    args = parser.parse_args()

    print(args)
    m, n = args.dim
    assert m>1 and n>1, "Degenerate subgrids are not allowed here"
    assert args.levels > 1, "Need at least two levels"
    assert args.stairwells > 0, "Need at least one stairwell"
    assert args.stairwells < min(m, n), "Too many stairwells per level"

    main(args)

# END: multilevel_grid_demo.py
