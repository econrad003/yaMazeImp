#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# eval_aldous_broder_bias.py - evaluate the tweaked Aldous/Broder algorithm
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
eval_aldous_broder_bias.py - evaluate the tweaked Aldous/Broder algorithm
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Part of a homework problem in [1].

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from rectangular_grid import Rectangular_Grid
from aldous_broder_bias import Weighted_Aldous_Broder
from evaluator_ortho import Ortho_Evaluator

rows, cols = 20, 30
runs = 40
filenamefmt = "stats/eval_aldous_broder_%s_%f_%s.txt"
titlefmt = "Weighted Aldous/Broder (first entrance - %s bias %f - %s)"
parameters = "Rectangular_Grid(%d, %d)" % (rows, cols)
fmt1 = "%30s %13.6f %13.6f %13.6f"
fmt0 = "%30s %13s %13s %13s\n"
params = {}

def creator():
    """create a maze"""
    bias = params["bias"]
    tweak = params["tweak"]
    no_revisit = params["visit"]
    print(".", end="", flush=True)
    grid = Rectangular_Grid(rows, cols)
    if tweak is "straight":
        Weighted_Aldous_Broder.straight_on(grid, p=bias, \
            no_revisit=no_revisit)
    elif tweak is "right":
        Weighted_Aldous_Broder.right_on(grid, p=bias, \
            no_revisit=no_revisit)
    elif tweak is "left":
        Weighted_Aldous_Broder.left_on(grid, p=bias, \
            no_revisit=no_revisit)
    elif tweak is "turn":
        Weighted_Aldous_Broder.turn_on(grid, p=bias, \
            no_revisit=no_revisit)
    else:         # tweak is "magnet"
        if not no_revisit:
            bias /= 6
        Weighted_Aldous_Broder.magnet_on(grid, "east", p=bias, \
            no_revisit=no_revisit)
    return grid

def format_title(tweak, bias, no_revisit):
    """center the title"""
    revisit = "norevisit" if no_revisit else "revisit"
    title = titlefmt % (tweak, bias, revisit)
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

def results(tweak, bias, no_revisit):
    visit = "norevisit" if no_revisit else "revisit"
    filename = filenamefmt % (tweak, bias, visit)
    with open(filename, 'w') as fp:
        fp.write("%s\n\n" % format_title(tweak, bias, no_revisit))
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


        # additional orthogonal statistics
M = [[eachrow_NE, eachcol_NE, "east", "horizontal"],
     [eachcol_EN, eachrow_EN, "north", "vertical"]]

        # test vectors

biases = [0.25, 0.5]
tweaks = ["straight", "left", "right", "turn", "magnet"]
no_revisits = [True, False]

for bias in biases:
    params["bias"] = bias
    for tweak in tweaks:
        params["tweak"] = tweak
        for no_revisit in no_revisits:
            params["visit"] = no_revisit
            newbias = bias / 6 if tweak == "magnet" and not no_revisit \
                else bias

                # run the test
            test = Ortho_Evaluator(creator, runs, M)
            print("Weighted Aldous/Broder %s-%f-%s" \
                % (tweak, newbias, str(no_revisit)))
            print("Gathering statistics...")
            test.run()
            print("")

                # print the results
            results(tweak, newbias, no_revisit)

# END: eval_aldous_broder_bias.py
