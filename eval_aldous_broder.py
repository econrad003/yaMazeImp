#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# eval_aldous_broder.py - evaluate the Aldous/Broder implementation
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
#     10 May 2020 - Initial version
##############################################################################
"""
eval_aldous_broder.py - evaluate the Aldous/Broder implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from rectangular_grid import Rectangular_Grid
from aldous_broder import Aldous_Broder
from evaluator_ortho import Ortho_Evaluator

rows, cols = 20, 30
runs = 40
filename = "stats/eval_aldous_broder.txt"
title = "Aldous/Broder algorithm (first entrance)"
parameters = "Rectangular_Grid(%d, %d)" % (rows, cols)
fmt1 = "%30s %13.6f %13.6f %13.6f"
fmt0 = "%30s %13s %13s %13s\n"

def creator():
    """create a maze"""
    print(".", end="", flush=True)
    grid = Rectangular_Grid(rows, cols)
    Aldous_Broder.on(grid)
    return grid

def format_title():
    """center the title"""
    filler = ' ' * int((72 - len(title)) / 2)
    return filler + title + filler

def report(test, key, denominator=None):
    """report on item by key"""
    p, mu, sigma = test.moments_to_means(key, denominator)
    label = test.legend[key]
    return fmt1 % (label, p, mu, sigma)

def eachrow_NE(maze):
    """north/east row major traversal"""
    for i in range(rows):
        yield i

def eachcol_NE(maze, i):
    """north/east column minor traversal"""
    for j in range(cols):
        yield maze[i, j]

def eachcol_EN(maze):
    """east/north column major traversal"""
    for j in range(cols):
        yield j

def eachrow_EN(maze, j):
    """east/north row minor traversal"""
    for i in range(rows):
        yield maze[i, j]

        # additional orthogonal statistics
M = [[eachrow_NE, eachcol_NE, "east", "horizontal"],
     [eachcol_EN, eachrow_EN, "north", "vertical"]]

test = Ortho_Evaluator(creator, runs, M)
print("Gathering statistics...")
test.run()
print("")

with open(filename, 'w') as fp:
    fp.write("%s\n\n" % format_title())
    fp.write("Parameters: %s\n" % parameters)
    fp.write("Sample size: %d\n\n" % runs)
    fp.write(fmt0 % ("Item", "p", "mu", "sigma"))
    fp.write(fmt0 % ("-"*30, "-"*13, "-"*13, "-"*13))
    keys = sorted(list(test.moments.keys()))
    for key in keys:
        s = report(test, key)
        fp.write(s + "\n")
    fp.write("\n\n================\n")
    fp.write("Expected values:\n")
    fp.write("    mu(v, e, k)=(%d, %d, %d) exactly!\n" \
        % (rows * cols, rows * cols - 1, 1))
print("Saved to " + filename)

# END: eval_aldous_broder.py
