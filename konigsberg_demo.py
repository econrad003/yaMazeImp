#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# konigsberg_demo.py - a maze based on Euler's Königsberg bridges problem
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
#     6 Aug 2020 - EC - initial version
##############################################################################
"""
konigsberg_demo.py - a maze based on Euler's Königsberg bridges problem
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

This program uses a template and the recursive backtracker (DFS)
algorithm to produce a maze based on the Königsberg bridges problem
discussed by Euler in a 1736 journal article.  The problem involves
seven bridges spanning the banks of and two islands in the Pregel
River running through the town of Königsberg in East Prussia.  To
insure that the bridges are passable, one pass of simple braiding is
done to connect, where possible, each dead end to a second grid
neighbor.  The resulting maze thus contains some circuits. 

In the problem, a townsperson is to walk through the town, crossing
each bridge exactly once, preferably returning to the point of
departure.  Euler demonstrated that neither the strong form (return
to start) nor the weak form (end anywhere) was soluble.  Euler
gave general conditions for similar problems, correctly stating
for conditions under which the problem could or could not be solved.
He gave a partial proof, specifically verifying sufficient conditions
for insolubility.  (The proof in the other direction, establishing
that these same conditions were also necessary, came in 1873, in a
posthumous paper by Carl Hierholzer.)

References:

    [1] Leonhard Euler (1736). "Solutio problematis ad geometriam situs
        pertinentis". Comment Acad Sci U Petrop 8, 128–40.

    [2] Carl Hierholzer (1873), "Ueber die Möglichkeit, einen Linienzug
        ohne Wiederholung und ohne Unterbrechung zu umfahren",
        Mathematische Annalen, 6 (1): 30–32, doi:10.1007/BF01442866.

Bugs:

    Unknown.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from weave_grid import Weave_Grid
from grid_template import Grid_Template
from recursive_backtracker import Recursive_Backtracker as DFS
from layout_plot_color import Color_Layout

def make_grid(m, n):
    """create a grid"""
    print("Create Weave_Grid(%d,%d) object..." % (m, n))
    print("    %d cells in grid" % (m*n))
    return Weave_Grid(m, n)

def categorize(cell, category, categories):
    """associate a cell with a part of the maze"""
    if not cell:
        return
    if category == ' ':
        return
    if category not in categories:
        categories[category] = []
    categories[category].append(cell)

def apply_mask(grid, filename):
    """apply the mask"""
    print("Apply mask:")
    categories = {}
    template = Grid_Template(grid)
    with open(filename, "r") as fp:
        lines = fp.readlines()
    i = 0
    for line in lines:
        for j in range(len(line)-1):
            cell = grid[i, j]
            categorize(cell, line[j], categories)
            if cell and line[j] == ' ':
                template.remove_cell(cell, logging=False)
        i += 1
    print("    %d cells in grid" % len(grid))
    return categories

def render(maze, categories, colors, filename, title):
    """plot the maze"""
    print("Rendering -- this may take some time!")
    print("    %d cells in maze" % len(maze))
    mpl.rcParams['lines.linewidth'] = 0.5
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_axis_off()
    layout = Color_Layout(maze, plt, figure=[fig, ax], title=title)
    for category in colors:
        layout.set_palette_color(category, colors[category])
    for category in categories:
        if category in colors:
            for cell in categories[category]:
                layout.set_color(cell, category)
    for cell in maze.each():
        if "underCell" in cell.kwargs:
            layout.set_color(cell, "under")
    layout.draw_grid()
    layout.fig.savefig(filename, bbox_inches='tight', pad_inches=0.0,
        dpi=300)
    # layout.plt.show()

if __name__ == "__main__":
    maze = make_grid(29, 140)
    categories = apply_mask(maze, "input/königsberg.txt")
    DFS.on(maze)
    maze.braid()        # this insures that all bridges can be crossed
    colors = {}
    colors["A"] = "olivedrab"
    colors["B"] = "yellowgreen"
    colors["C"] = "chartreuse"
    colors["D"] = "khaki"
    colors["b"] = "salmon"
    colors["under"] = "brown"
    render(maze, categories, colors, "demos/königsberg_maze.png", \
        "the Königsberg bridges")

# END: konigsberg_demo.py
