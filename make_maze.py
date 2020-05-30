#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# make_maze.py - a rectangular maze generator
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
#     16 May 2020 - Initial version
##############################################################################
"""
make_maze.py - a rectangular maze generator
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

valid_layouts = set(['ASCII', 'unicode', 'graphviz', 'plot'])
valid_algorithms = set(['AldousBroder', 'AB', 'ReverseAldousBroder', 'RAB', \
    'AldousBroderWilson', 'ABW', 'BT', 'BinaryTree', 'BT2', 'BinaryTree2', \
    'DFS', 'RBT', 'RecursiveBackTracker', 'HK', 'HuntKill', 'HuntAndKill', \
    'NRDFS', 'Labyrinth', 'SW', 'Sidewinder', 'BFS', 'BreadthFirstSearch',
    'HEAP', 'HeapSearch', 'W', 'Wilson'])

def make_epilog():
    """create the help epilog"""
    import textwrap
    layouts = sorted(list(valid_layouts))
    epilog1 = "The supported rendering layouts are %s." % str(layouts)
    epilog1 = textwrap.fill(epilog1)
    algorithms = sorted(list(valid_algorithms))
    epilog2 = "The supported algorithm strings are %s." \
        % str(algorithms)
    sep = "\n\n"
    return epilog1 + sep + epilog2

def make_grid(m, n):
    """create a rectangular grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from rectangular_grid import Rectangular_Grid

    print("Grid: Rectangular_Grid(%d, %d)" % (m, n))
    grid = Rectangular_Grid(m, n)
    return grid

def generate_maze(algorithm, grid, bias):
    """generate a maze"""
    print("Algorithm = %s, bias = %s" % (algorithm, str(bias)))
    basename = None

    if algorithm in ['AB', 'AldousBroder']:
        from aldous_broder import Aldous_Broder
        Aldous_Broder.on(grid)
        basename = "AldousBroder"
    elif algorithm in ['RAB', 'ReverseAldousBroder']:
        from aldous_broder import Aldous_Broder
        Aldous_Broder.reverse_on(grid)
        basename = "ReverseAldousBroder"
    elif algorithm in ['ABW', 'AldousBroderWilson']:
        from wilson import Wilson as ABW
        if bias is None:
            bias = 0.5
        ABW.hybrid_on(grid, cutoff=bias)
        basename = "AldousBroderWilson"
    elif algorithm in ['BT', 'BinaryTree']:
        from binary_tree import Binary_Tree
        if bias is None:
            bias = 0.5
        Binary_Tree.on(grid, bias=bias)
        basename = "BinaryTree"
    elif algorithm in ['BT2', 'BinaryTree2']:
        from binary_tree2 import Binary_Tree
        Binary_Tree.on(grid)
        basename = "BinaryTree2"
    elif algorithm in ['DFS', 'RBT', 'RecursiveBackTracker']:
        from recursive_backtracker import Recursive_Backtracker
        Recursive_Backtracker.on(grid)
        basename = "RecursiveBacktracker"
    elif algorithm in ['HK', 'HuntKill', 'HuntAndKill']:
        from hunt_and_kill import Hunt_and_Kill
        Hunt_and_Kill.on(grid)
        basename = "HuntAndKill"
    elif algorithm in ['NRDFS', 'Labyrinth']:
        from recursive_backtracker import Recursive_Backtracker
        Recursive_Backtracker.deterministic_on(grid)
        basename = "Labyrinth"
    elif algorithm in ['SW', 'Sidewinder']:
        from sidewinder import Sidewinder
        if bias is None:
            bias = 0.5
        Sidewinder.on(grid, bias=bias)
        basename = "Sidewinder"
    elif algorithm in ['BFS', 'BreadthFirstSearch']:
        from tree_search import Tree_Search
        Tree_Search.bfs_on(grid)
        basename = "BreadthFirstSearch"
    elif algorithm in ['HEAP', 'HeapSearch']:
        from tree_search import Tree_Search
        Tree_Search.heap_on(grid)
        basename = "HeapSearch"
    elif algorithm in ['W', 'Wilson']:
        from wilson import Wilson
        Wilson.on(grid)
        basename = "Wilson"
    print("maze generation: complete!")
    return basename

def render_ASCII(grid, basename, test):
    """render the maze in ASCII"""
    maze = str(grid)
    print(maze)

    folder = "demos/ascii/" if test else "examples/ascii/"
    pathname = folder + basename + "-str.txt"

    with open(pathname, 'w') as fp:
        fp.write(maze)
    print("saved to " + pathname)

def render_unicode(grid, basename, test):
    """render the maze in unicode"""
    maze = grid.unicode()
    print(maze)

    folder = "demos/unicode/" if test else "examples/unicode/"
    pathname = folder + basename + "-unicode.txt"

    with open(pathname, 'w') as fp:
        fp.write(maze)
    print("saved to " + pathname)

def render_graphviz(grid, basename, test):
    """render the maze using GraphViz/dot"""
    from layout_graphviz import Layout

    folder = "demos/graphviz/" if test else "examples/graphviz/"
    pathname = folder + basename + ".gv"

    dot = Layout(grid, engine='fdp', filename=pathname)
    dot.set_square_cells()
    dot.draw()
    dot.render()

def render_plot(grid, basename, test):
    """render the maze using matplotlib"""
    import matplotlib.pyplot as plt
    from layout_plot import Layout

    folder = "demos/" if test else "examples/plot/"
    pathname = folder + basename + "-plot.png"

    layout = Layout(grid, plt, title=basename)
    layout.ax.set(aspect=1)
    plt.axis('off')
    layout.draw_grid()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    layout.render(pathname, tight=True)

def render_maze(layout, basename, grid, test):
    """output the maze"""
    if layout == "ASCII":
        render_ASCII(grid, basename, test)
    elif layout == "unicode":
        render_unicode(grid, basename, test)
    elif layout == "graphviz":
        render_graphviz(grid, basename, test)
    elif layout == "plot":
        render_plot(grid, basename, test)

def main(args):
    """Generate a maze"""
        # do some validation of the command line arguments
    m, n = args.dim
    assert m > 1 and n > 1, \
        "rows=%d, columns=%d: Dimensions must be greater than 1" % (m, n)
    algorithm = args.alg
    assert algorithm in valid_algorithms, \
        "%s is not a valid algorithm string" % algorithm
    layouts = args.layout
    for layout in layouts:
        assert layout in valid_layouts, \
            "%s is not a valid layout string" % layout
    bias = args.bias

    grid = make_grid(m, n)
    algorithm = generate_maze(algorithm, grid, bias)
    assert algorithm, "No maze was generated."

    basename = algorithm if bias is None else "%s-%.3f" % (algorithm, bias)
    if args.basename:
        basename = args.basename

    for layout in layouts:
        render_maze(layout, basename, grid, args.test)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser( \
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog=make_epilog())
    parser.add_argument('--dim', metavar=('ROWS', 'COLS'),
                        nargs=2, default=[5, 7], type=int,
                        help='the numbers of rows and columns')
    parser.add_argument('--alg', metavar='ALGORITHM',
                        default='BinaryTree',
                        help='the maze generation algorithm')
    parser.add_argument('--layout', metavar='LAYOUT',
                        default=['unicode'], nargs='+',
                        help='the layout rendering engine')
    parser.add_argument('--basename', metavar='LAYOUT',
                        default=None, nargs='+',
                        help='an optional name for the output')
    parser.add_argument('--bias', type=float,
                        help='a probability, where applicable')
    parser.add_argument('-t', '--test', action='store_true',
                        help='test run')
    args = parser.parse_args()

    main(args)

# END: make_maze.py
