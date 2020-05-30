# -*- coding: utf-8 -*-
# evaluator.py - an evaluator for maze algorithms
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
"""
evaluator.py - evaluator for maze algorithms
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""

from statistics import Maze_Statistics
from helpers import Helper
from norms import longest_path

class Evaluator(object):
    """base class for cells"""

    def __init__(self, f, n):
        """constructor

        Mandatory arguments:
            f - a procedure which returns a maze
            n - the number of mazes to evaluate
        """
        self.f = f
        self.n = n
        self.legend = {}
        self.moments = {}

    def run(self):
        """run the simulation"""
        for i in range(self.n):
            maze = self.f()                    # create a maze
            stats = Maze_Statistics(maze)
            v = self.vertices(stats)
            e = self.edges(stats)
            k = self.components(maze, v, e)
            self.diameter(maze)
            self.additional_tests(maze)

    def additional_tests(self, maze):
        """hook for derived classes"""
        pass

    def moments_to_means(self, key, n=None):
        """convert moments into means"""
        from math import sqrt

        if not n:
            n = self.n
        m0, m1, m2 = self.moments[key]      # unpack
        p = m0 / self.n
        mu = m1 / n
        if n < 2:
            return [p, mu, 0]
        sigma = sqrt((m2 - (m1 * m1 / n)) / (n-1))
        return [p, mu, sigma]

    def vertices(self, stats):
        """get vertex counts"""
        v = stats.size()
        key = 'v'
        if key not in self.legend:
            self.make_key(key, "Number of cells (v)")
        self.make_moments(key, v)
        return v

    def edges(self, stats):
        """get edge and vertex degree counts"""
        degseq = stats.degree_counts()      # degree sequence
        e = 0
        for p in degseq:
            e += p * degseq[p]
            key = "v%d" % p
            if key not in self.legend:
                if p is 1:
                    name = "Number of dead ends"
                elif p is 0:
                    name = "Number of isolated cells"
                else:
                    name = "Number of cells of degree %d" % p
                self.make_key(key, name)
            self.make_moments(key, degseq[p])
        e /= 2
        key = 'e'
        if key not in self.legend:
            self.make_key(key, "Number of passages (e)")
        self.make_moments(key, e)
        return e

    def components(self, maze, v, e):
        """component count and characteristic"""
        k, _ = Helper.find_components(maze)
        key = 'k'
        if key not in self.legend:
            self.make_key(key, "Number of components (k)")
        self.make_moments(key, k)
        chi = v - e - k
        key = 'chi'
        if key not in self.legend:
            self.make_key(key, "Maze characteristic (v-e-k)")
        self.make_moments(key, chi)
        return k

    def diameter(self, maze):
        """get diameter (incorrect if not a tree)"""
        d, _, _ = longest_path(maze.choice())
        key = 'd'
        if key not in self.legend:
            self.make_key(key, "Diameter (d)")
        self.make_moments(key, d)

    def make_key(self, key, name):
        """make a key in the legends and results tables"""
        self.legend[key] = name
        self.moments[key] = [0, 0, 0]       # moments

    def make_moments(self, key, x):
        """adjust the moments"""
        n, sx, sxx = self.moments[key]      # unpack
        n += 1                              # zeroth moment (count)
        sx += x                             # first moment (sum)
        sxx += x*x                          # second moment (sum of sq)
        self.moments[key] = [n, sx, sxx]    # pack

# END: evaluator.py
