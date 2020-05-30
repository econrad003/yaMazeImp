#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# texturizer.py - create a texture vector for an algorithm
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

valid_algorithms = set(['AldousBroder', 'AB', 'ReverseAldousBroder', 'RAB', \
    'AldousBroderWilson', 'ABW', 'BT', 'BinaryTree', 'BT2', 'BinaryTree2', \
    'DFS', 'RBT', 'RecursiveBackTracker', 'HK', 'HuntKill', 'HuntAndKill', \
    'NRDFS', 'Labyrinth', 'SW', 'Sidewinder', 'BFS', 'BreadthFirstSearch',
    'HEAP', 'HeapSearch', 'W', 'Wilson'])

def make_epilog():
    """create the help epilog"""
    import textwrap
    algorithms = sorted(list(valid_algorithms))
    epilog = "The supported algorithm strings are %s." \
        % str(algorithms)
    epilog = textwrap.fill(epilog)
    return epilog

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
        basename = "AldousBroderWilson"
        if bias is None:
            bias = 0.5
        else:
            basename += "-bias%f" % bias
        ABW.hybrid_on(grid, cutoff=bias)
    elif algorithm in ['BT', 'BinaryTree']:
        from binary_tree import Binary_Tree
        basename = "BinaryTree"
        if bias is None:
            bias = 0.5
        else:
            basename += "-bias%f" % bias
        Binary_Tree.on(grid, bias=bias)
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
        basename = "Sidewinder"
        if bias is None:
            bias = 0.5
        else:
            basename += "-bias%f" % bias
        Sidewinder.on(grid, bias=bias)
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

def define_color(dist, maxdist):
    """associate a color with a distance"""
    ratio = dist / (maxdist + 1)
    red = 0.5 + ratio / 2
    green = 1 - ratio / 2
    blue = green
    return (red, green, blue)

def render_plot(m, n, algorithm, bias):
    """render the maze using matplotlib"""
    import matplotlib.pyplot as plt
    from layout_plot_color import Color_Layout
    from norms import distances

    fig, axs = plt.subplots(2, 3)
    x0, y0 = int(m/2), int(n/2)
    basename = algorithm
    for i in range(2):
        for j in range(3):
            grid = make_grid(m, n)

            center = grid[x0, y0]
            assert center, "Undefined grid center cell"

            basename = generate_maze(algorithm, grid, bias)
            ax = axs[i, j]
            layout = Color_Layout(grid, plt, figure=[fig, ax])

                # We use the distance from a middle cell as the
                # palette index
            norms = distances(center)
            furthest = norms.furthest_from_root()
            maxdist = norms[furthest]
            for dist in range(maxdist + 1):
                layout.set_palette_color(dist, define_color(dist, maxdist))
            for cell in grid.each():
                dist = norms[cell]
                if dist is not None:
                    layout.set_color(cell, dist)

            ax.set(aspect=1)
            ax.axis('off')
            layout.draw_grid()
    fig.suptitle(basename)
    filename = "demos/" + basename + "-array.png"
    print("Saved to " + filename)
    plt.subplots_adjust(hspace=.001, wspace=.001)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(filename, bbox_inches='tight', pad_inched=0.0)

def main(args):
    """Generate a maze"""
        # do some validation of the command line arguments
    m, n = args.dim
    assert m > 1 and n > 1, \
        "rows=%d, columns=%d: Dimensions must be greater than 1" % (m, n)
    algorithm = args.alg
    assert algorithm in valid_algorithms, \
        "%s is not a valid algorithm string" % algorithm
    bias = args.bias

    render_plot(m, n, algorithm, bias)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser( \
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog=make_epilog())
    parser.add_argument('--dim', metavar=('ROWS', 'COLS'),
                        nargs=2, default=[20, 20], type=int,
                        help='the numbers of rows and columns')
    parser.add_argument('--alg', metavar='ALGORITHM',
                        default='BinaryTree',
                        help='the maze generation algorithm')
    parser.add_argument('--bias', type=float,
                        help='a probability, where applicable')
    args = parser.parse_args()

    main(args)

# END: make_maze.py
