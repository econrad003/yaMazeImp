#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# long_tunnel_demo.py - demonstrate the creation of long tunnels
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
#     5 Aug 2020 - Initial version
##############################################################################
"""
long_tunnel_demo.py - demonstrate creation of long tunnels
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation below of the function named
'render'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

import matplotlib.pyplot as plt
from kruskals import Kruskals

def make_weave_grid(m, n):
    """create a rectangular weave grid
    
    Arguments:
        m, n - respectively the number of rows and columns"""
    from weave_grid import Preweave_Grid

    print("Grid: Rectangular_Grid(%d, %d)" % (m, n))
    grid = Preweave_Grid(m, n, inset=0.25)
    return grid

def preconfigure(grid):
    """preconfigure the grid"""
    state = Kruskals.State(grid)
    return state

def preconfigure_tunnel(state, start, direction, length):
    """preconfigure a long tunnel"""
    print("long tunnel: start=%s, %s, length=%d" \
        % (str(start.index), direction, length))
    s = state.add_long_tunnel(start, direction, length)
    if s:
        print(s)
    else:
        print("Success!")

def generate_maze(grid, state):
    """generate a perfect maze on the grid"""
    print("Generate perfect maze using Kruskal's algorithm...")
    Kruskals.on(grid, state)
    print("Done!")

def tweak(fig, ax, title="Magical Chunnel Maze"):
    """a tweaking function to modify the plot"""
    ax.title.set_text(title)
    ax.set(aspect=1)
    ax.axis('off')
    fig.suptitle("Long Tunnel Demonstration")

def render(maze, filename, nodes=[], tweaker=tweak):
    """render a set of mazes
    
    This is the main entry point to this script.

    maze = a Preweave_Grid maze generated using Kruskal's algorithm
    filename = filename or pathname for output
    nodes = a list of nodes to be specially colored
    tweaker = the tweaking routine (default tweak).  This function takes
        three parameters: the number of mazes, a Figure object and array
        of Axes objects
    """
    from layout_plot_color import Color_Layout

        # generate the plot
    print("Plotting...")
    layout = Color_Layout(maze, plt)
    tweaker(layout.fig, layout.ax)
    layout.palette[0] = 'yellow'
    layout.palette[1] = 'green'
    layout.palette[2] = 'cyan'
    for cell in maze.each():
        if "underCell" in cell.kwargs:
            layout.color[cell] = 1
        elif cell in nodes:
            layout.color[cell] = 2
        else:
            layout.color[cell] = 0
    layout.draw_grid()
    print('saving figure to %s' % filename)
    layout.fig.savefig(filename, bbox_inches='tight', pad_inches=0.0, \
        dpi=200)
    # layout.render(filename, tight=True)
    # plt.show()

if __name__ == "__main__":
    print("Twisty Braid Maze Script...")
    maze = make_weave_grid(30, 40)
    state = preconfigure(maze)
    nodes = {}
    preconfigure_tunnel(state, maze[2, 2], "east", 35)
    state.force_connection(maze[2, 2], "south")
    state.force_connection(maze[2, 2], "north")
    nodes[maze[2, 2]] = 1
    state.force_connection(maze[2, 38], "south")
    state.force_connection(maze[2, 38], "north")
    nodes[maze[2, 38]] = 1
    preconfigure_tunnel(state, maze[28, 38], "west", 35)
    state.force_connection(maze[28, 2], "south")
    state.force_connection(maze[28, 2], "north")
    nodes[maze[28, 2]] = 1
    state.force_connection(maze[28, 38], "south")
    state.force_connection(maze[28, 38], "north")
    nodes[maze[28, 38]] = 1
    preconfigure_tunnel(state, maze[8, 10], "north", 10)
    state.force_connection(maze[8, 10], "east")
    state.force_connection(maze[8, 10], "west")
    nodes[maze[8, 10]] = 1
    state.force_connection(maze[19, 10], "east")
    state.force_connection(maze[19, 10], "west")
    nodes[maze[19, 10]] = 1
    preconfigure_tunnel(state, maze[20, 34], "south", 10)
    state.force_connection(maze[9, 34], "east")
    state.force_connection(maze[9, 34], "west")
    nodes[maze[9, 34]] = 1
    state.force_connection(maze[20, 34], "east")
    state.force_connection(maze[20, 34], "west")
    nodes[maze[20, 34]] = 1
    state.add_random_weaves(n=500)
    generate_maze(maze, state)
    filename = "demos/long_tunnel_demo.png"
    render(maze, filename, nodes=nodes)

# END: long_tunnel_demo.py
