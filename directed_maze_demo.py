#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# directed_maze_demo.py - test the directed maze algorithms
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
#     13 Sep 2020 - Initial version (directed binary tree)
##############################################################################
"""
directed_maze_demo.py - test the hunt and kill implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import matplotlib as mpl
from matplotlib import pyplot as plt

import di_binary_tree as dBT

def make_grid(m, n, maze_name, inset):
    """create a grid"""
    print("%s: Rectangular_Grid(%d, %d)" % (maze_name, m, n))
    from rectangular_grid import Rectangular_Grid
    grid = Rectangular_Grid(m, n, name=maze_name, inset=inset)
    return grid

def make_weave_grid(m, n, maze_name, inset):
    """create a grid"""
    print("Weave grids are not yet supported...")
    print("  -- see can_tunnel methods")
    print("  -- these only work for two-way connections")
    print()
    print("%s: Weave_Grid(%d, %d)" % (maze_name, m, n))
    from weave_grid import Weave_Grid
    grid = Weave_Grid(m, n, name=maze_name, inset=inset)
    return grid

def make_binary_maze(grid, towards, state=None):
    """carve a directed binary tree maze"""
    print("%s: Directed_Binary_Tree(%s)" % (grid.name, towards))
    state = dBT.Directed_Binary_Tree.on(grid, state=state, 
        towards=towards)
    return state

def make_DFS_maze(grid, towards, state=None):
    """carve a directed sidewinder tree maze"""
    from di_recursive_backtracker import Directed_Recursive_Backtracker 

    desc = "%s: Directed Depth-First Search (%s)"
    print(desc % (grid.name, towards))
    state = Directed_Recursive_Backtracker.on(grid, state=state, 
        towards=towards)
    return state

def make_Aldous_Broder_maze(grid, towards, last_exit, state=None):
    """carve a directed sidewinder tree maze"""
    from di_aldous_broder import Directed_Aldous_Broder 

    print("%s: Directed Aldous Broder (%s)" % (grid.name, towards))
    state = Directed_Aldous_Broder.on(grid, state=state,
        towards=towards, last_exit=last_exit)
    return state

def create_layout(maze):
    """create the layout object"""
    print("%s: Layout" % maze.name)
    from layout_plot_digraph import Digraph_Layout
    layout = Digraph_Layout(maze, plt, title=maze.name)
    layout.ax.axis('off')
    layout.ax.set(aspect=1)
    return layout

def render_maze(layout, filename):
    """render the maze"""
    print("%s: Render" % layout.grid.name)
    layout.draw_grid()
    layout.render(filename)

def main_quick(args):
    """create a small maze to test basic drawing operations"""
    args.show = True
    maze = make_grid(3, 5, "Small Mostly One-Way Maze", args.inset)
    make_binary_maze(maze, "toward")
    ne = maze[2,4]
        # the NE corner connections are two-way
    ne["south"].makePassage(ne)
    ne["west"].makePassage(ne)
        # draw the maze
    layout = create_layout(maze)
    layout.set_palette_color(1, "yellow")
    layout.set_palette_color(2, "cyan")
    layout.set_palette_color(3, "magenta")
    for cell in maze.each():
        i, j = cell.index
        c = (i*3 + j) % 4
        if c:
            layout.set_color(cell, c)
    filename = "demos/di_quick_inset_demo.png" if args.inset \
        else "demos/di_quick_demo.png"
    render_maze(layout, filename)
    return layout

def main_quick2(args):
    """create a small maze to test basic drawing operations"""
    args.show = True
    maze = make_grid(3, 5, "Small Directed Maze", args.inset)
    make_binary_maze(maze, "both")
        # draw the maze
    layout = create_layout(maze)
    layout.set_palette_color(1, "yellow")
    layout.set_palette_color(2, "cyan")
    layout.set_palette_color(3, "magenta")
    for cell in maze.each():
        i, j = cell.index
        c = (i*3 + j) % 4
        if c:
            layout.set_color(cell, c)
    filename = "demos/di_quick2_inset_demo.png" if args.inset \
        else "demos/di_quick2_demo.png"
    render_maze(layout, filename)
    return layout

def main_quick3(args):
    """create a small maze to test basic drawing operations"""
    args.show = True
    maze = make_grid(3, 5, "Directed away from Orange Cell", args.inset)
    terminus = maze[1, 2]
    state = dBT.Set_Terminus_State(maze, maze[1,2])
    make_binary_maze(maze, "away", state)
        # draw the maze
    layout = create_layout(maze)
    layout.set_palette_color(1, "yellow")
    layout.set_palette_color(2, "cyan")
    layout.set_palette_color(3, "magenta")
    layout.set_palette_color(4, "orange")
    for cell in maze.each():
        i, j = cell.index
        c = (i*3 + j) % 4
        if c:
            layout.set_color(cell, c)
    layout.set_color(terminus, 4)
    filename = "demos/di_quick3_inset_demo.png" if args.inset \
        else "demos/di_quick3_demo.png"
    render_maze(layout, filename)
    return layout

def set_directions(args):
    """determine the arrow directions

    Ignore in the quick demos above.
    """
    if args.away or args.toward:
        if args.away and args.toward:
            return "both"
        if args.away:
            return "away"
        return "towards"
    return "both"

def main_binary(args):
    """create a directed binary tree maze"""
    m, n = args.dim
    maze = make_grid(m, n, "Directed Binary Tree Maze", 0.15)
    dirs = set_directions(args)
    make_binary_maze(maze, dirs)
    layout = create_layout(maze)
    mpl.rcParams['lines.linewidth'] = 0.5
    render_maze(layout, "demos/di_binary_tree_demo.png")
    return layout

def main_sidewinder(args):
    """directed sidewinder maze"""
    m, n = args.dim
    maze = make_grid(m, n, "Directed Sidewinder Maze", 0.15)
    dirs = set_directions(args)
    make_sidewinder_maze(maze, dirs)
    layout = create_layout(maze)
    mpl.rcParams['lines.linewidth'] = 0.5
    render_maze(layout, "demos/di_sidewinder_demo.png")
    return layout

def main_DFS(args):
    """directed depth-first search maze"""
    m, n = args.dim
        # change to make_weave_grid when weaving is supported:
    maze = make_grid(m, n, "Directed DFS Maze", 0.15)
    dirs = set_directions(args)
    state = make_DFS_maze(maze, dirs)
    terminus = state.terminus
    layout = create_layout(maze)
    layout.set_palette_color(4, "orange")
    layout.set_color(terminus, 4)
    mpl.rcParams['lines.linewidth'] = 0.5
    render_maze(layout, "demos/di_DFS_demo.png")
    return layout

def main_Aldous_Broder(args, last_exit=False):
    """directed Aldous/Broder maze"""
    m, n = args.dim
        # change to make_weave_grid when weaving is supported:
    maze = make_grid(m, n, "Directed Aldous/Broder Maze", 0.15)
    dirs = set_directions(args)
    terminus = make_Aldous_Broder_maze(maze, dirs, last_exit=last_exit)
    layout = create_layout(maze)
    layout.set_palette_color(4, "orange")
    layout.set_color(terminus, 4)
    mpl.rcParams['lines.linewidth'] = 0.5
    filename = "demos/di_AldousBroder_"
    if last_exit:
        filename += "LE_"
    filename += "demo.png"
    render_maze(layout, filename)
    return layout

def main(args):
    """main entry point"""
    print(args)
    args.inset = 0.15 if args.inset else 0
    
    if args.quick:
        main_quick(args)
    if args.quick2:
        main_quick2(args)
    if args.quick3:
        main_quick3(args)
    if args.AldousBroder:
        main_Aldous_Broder(args)
    if args.binary:
        main_binary(args)
    if args.dfs:
        main_DFS(args)
    if args.lastExit:
        main_Aldous_Broder(args, True)
    if args.sidewinder:
        main_sidewinder(args)
    if args.show:
        plt.show()

if __name__ == "__main__":
    import argparse

    desc = "Directed maze algorithm demonstrations"
    parser = argparse.ArgumentParser(description=desc)

    options = {}
    options['quick'] = "run a one-way 3 by 5 quick demo"
    options['quick2'] = "a different 3 by 5 quick demo"
    options['quick3'] = "a one-way 3 by 5 demo with a special terminus"
    options['binary'] = "run the directed binary tree algorithm"
    options['dfs'] = "run the depth-first search tree maze algorithm"
    options['sidewinder'] = "run the directed sidewinder algorithm"
    options['AldousBroder'] = "run the directed Aldous/Broder algorithm"
    options['lastExit'] = "use tha last exit version of Aldous/Broder"

    parser.add_argument('--dim', metavar=('ROWS', 'COLS'), \
        type=int, nargs=2, default=[20, 30],
        help="the numbers of rows and columns (default=20 30)")
    for option in options:
        parser.add_argument('--'+option, action='store_true', \
            help=options[option])
    parser.add_argument('--flip', type=float, default=0.5, \
        help="bias for a single coin flip (default=0.5)")
    parser.add_argument('--inset', action='store_true', \
        help="use an inset of 0.15 (ignored in some demos)")
    parser.add_argument('-a', '--away', action='store_true', \
        help="one way, away from terminus (ignored in some demos)")
    parser.add_argument('-t', '--toward', action='store_true', \
        help="one way, toward terminus (ignored in some demos)")
    parser.add_argument('--show', action='store_true', \
        help="show plots on exit")

    args = parser.parse_args()

    algorithm = args.quick2 or args.quick3 \
        or args.binary or args.dfs or args.sidewinder \
        or args.AldousBroder or args.lastExit
    if not algorithm:
        print("No algorithm selected, quick is assumed...")
        args.quick = True

    main(args)

# END: directed_maze_demo.py
