#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# multilevel_grid_demo.py - multilevel grid demonstration program
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
#     17 Aug 2020 - Initial version
"""
multilevel_grid_demo.py - multilevel grid demonstration program
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
from multilevel_grid import Multilevel_Grid
from layout_plot_multilevel import \
    Multilevel_Layout, Multilevel_Projective_Layout
from layout_plot_color import Color_Layout
from recursive_backtracker import Recursive_Backtracker as DFS

def build_level(multigrid, m, n, name=None, stairwells=0,
                warnings=True):
    """generate a floor"""
            # build the level
    level = len(multigrid.levels)
    if not name:
        name = "Floor #" + str(levels)
    upstairs = multigrid.add_level(m, n, name=name)

            # Ground level?
    if level is 0:
        if warnings and stairwells > 0:
            print("Warning: Cannot build stairs up to ground floor")
        return upstairs

            # add stairwells
    if stairwells and stairwells < 1:
        if warnings:
            print("Warning: no stairs up to level %d" % level)
        return upstairs

    downstairs = multigrid.levels[level-1]

    retries = 10
    collisions = 0
    errors = 0
    requested = stairwells
    while stairwells > 0 and retries > 0:
        downcell = downstairs.choice()
        if downcell["up"] or downcell["down"]:
                # already have a stairwell here; try again
            retries -= 1
            collisions += 1
            continue
        i, j = downcell.index
        upcell = upstairs[i, j]
        if not upcell:
                # no corresponding upcell
            retries -= 1
            errors += 1
            continue
        multigrid.add_stairs_upward(level-1, downcell)
        stairwells -= 1

    created = requested - stairwells
    if stairwells > 0 and (site_errors > 0 or warnings):
        print("Warning: unable to create requested stairwells...")
        print("  requested %d, created %d" % (requested, created))
        print("  collisions %d, errors %d" % (collisions, errors))
    return upstairs

def make_multigrid(levels, m, n, stairwells):
    """generate a multilevel grid"""

        # create the main grid
    print("Create multigrid: %d levels (%d×%d); %d stairwells per" \
        % (levels, m, n, stairwells))
    grid = Multilevel_Grid()

        # create the ground floor grid
    build_level(grid, m, n, name="Ground Floor")

    print("Ground floor only: %d cells (expected %d×%d = %d)" \
        % (len(grid), m, n, m*n))
    assert len(grid) == m*n, "Problem in grid creation"

    return grid

def make_upper_levels(grid, levels, m, n, stairwells):
    """create the upper levels"""
        # create upper levels
    for i in range(1, levels):
        if i is 1:
            name = "First Floor"
        elif i is 2:
            name = "Second Floor"
        else:
            name = "Floor #" + str(i)
        build_level(grid, m, n, name, stairwells)

    staircells = (levels - 1) * stairwells
    expected = m * n * levels + staircells
    print("%s: %d cells including %d stairs; (expected %d, %d)" \
        % ("Complete grid:", \
        len(grid), len(grid.stairs), expected, staircells))
    assert len(grid) == expected, "Problem in grid creation"

def render(grid, LayoutType, fig, axs, projective):
    """plot the result"""
          # create the primary layout
    print("Creating the layout objects")
    ax = axs[-1]
    MultiLayoutType = Multilevel_Projective_Layout if projective \
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

def main(args):
    """Generate a maze"""
    m, n = args.dim
    assert m>1 and n>1, "Degenerate subgrids are not allowed here"
    assert args.levels > 1, "Need at least two levels"
    assert args.stairwells > 0, "Need at least one stairwell"
    assert args.stairwells < min(m, n), "Too many stairwells per level"

        # create the maze
    grid = make_multigrid(args.levels, m, n, args.stairwells)
    make_upper_levels(grid, args.levels, m, n, args.stairwells)
    DFS.on(grid)

        # create the subplots
    levels = len(grid.levels)
    fig, axs = plt.subplots(1, levels+1)
    layout = render(grid, Color_Layout, fig, axs, args.projective)

    default = "multilevel_grid"
    if args.projective:
        default += "_proj"
    default += "_demo"
    basename = args.basename if args.basename else default
        
    layout.render("demos/" + basename + ".png")
    if args.show:
        plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser( \
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description="a simple multilevel maze demonstration")
    parser.add_argument('-d', '--dim', metavar=('ROWS', 'COLS'), \
        nargs=2, default=[10, 5], type=int, \
        help='the numbers of rows and columns')
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
        default=None,
        help='an optional name for the output')
    args = parser.parse_args()

    main(args)

# END: multilevel_grid_demo.py
