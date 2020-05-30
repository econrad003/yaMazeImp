# -*- coding: utf-8 -*-
# evaluator_ortho.py - an evaluator for orthogonal maze algorithms
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
#     21 Apr 2020 - Initial version
#     15 May 2020 - Use cell topology management methods.
#     21 May 2020 - A run consists of at least two cells.  A single cell
#       does not make a run.
"""
evaluator_ortho.py - evaluator for orthogonal maze algorithms
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from evaluator import Evaluator

class Ortho_Evaluator(Evaluator):
    """base class for cells"""

    def __init__(self, f, n, M):
        """constructor

        Mandatory arguments:
            f - a procedure which returns a maze
            n - the number of mazes to evaluate
            M - a two-dimensional array of evaluation functions:
                each row has the following format:
                        [eachrow, eachcol, direction, label]
                where:
                    eachrow(maze) - a generator for the major directions
                    eachcol(maze, row) - a generator for run direction
                    direction - the run direction (e.g. north)
                    label - a label for the run direction (e.g. vertical);
                        if None, use the direction
        """
        super().__init__(f, n)
        self.M = M
            # legend
        for row in M:
            _, _, direction, label = row    # unpack
            if label is None:
                label = direction
            key = "run-%s" % direction
            v = "average %s run" % label
            self.make_key(key, v)
            key = "maxrun-%s" % direction
            v = "longest %s run" % label
            self.make_key(key, v)

    def additional_tests(self, maze):
        """additional tests for rectangular mazes"""
        super().additional_tests(maze)
        for row in self.M:
            eachrow, eachcol, direction, _ = row
            self.classify_runs(maze, eachrow, eachcol, direction)

    def classify_runs(self, maze, eachrow, eachcol, direction):
        """categorize the runs by average and maximum length"""
        n, v, run, maxrun = 0, 0, 0, 0
        for row in eachrow(maze):     # close out run
            for cell in eachcol(maze, row):
                run += 1
                if cell[direction] not in cell.arcs:    # 15-05-2020
                        # close out run
                    if run > maxrun:
                        maxrun = run
                    if run > 1:                         # 21-05-2020
                        v += run
                        n += 1
                    run = 0
                # close out run at end of row
            if run > maxrun:
                maxrun = run
            if run > 1:                                 # 21-05-2020
                v += run
                n += 1
            run = 0
        avgrun = v / n
        key = "run-%s" % direction
        self.make_moments(key, avgrun)
        key = "maxrun-%s" % direction
        self.make_moments(key, maxrun)

# END: evaluator.py
