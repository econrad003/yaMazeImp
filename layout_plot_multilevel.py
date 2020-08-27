# -*- coding: utf-8 -*-
# layout_plot_multilevel.py - a layout class for multilevel rectangular mazes
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
#     15 Aug 2020 - Initial version
"""
layout_plot_multilevel.py - basic plotting with color for rectangular mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] David Lay. Linear Algebra and Its Applications.  Second Edition.
        1996 (Addison Wesley).  Book (0-201-82478-7).

Bugs:

    Unknown.
"""

import matplotlib.patches as patches
from layout_plot import Layout

class Multilevel_Layout(Layout):
    """layout for multilevel mazes"""

    def __init__(self, multigrid, plt, **kwargs):
        """create the multigrid layout

        Optional arguments:
            schematic - if False, then no schematic will be produced.
                (default: True)
        """
            # initialize a figure for a schematic
        schematic = False if "schematic" in kwargs and \
            not kwargs["schematic"] else True
        kwargs["schematic"] = schematic
        if schematic:
                # default title = "schematic"
            if "title" not in kwargs:
                kwargs["title"] = "schematic"
        else:
                # we don't want to create a figure if there is
                # no schematic
            kwargs["figure"] = None, None
            if "title" in kwargs:
                del kwargs["title"]

        super().__init__(multigrid, plt, **kwargs)

            # each member grid needs a layout
            # this will be supplied later
        self.layouts = {}

    def add_layout_for_grid(self, grid, plt, LayoutClass, **kwargs):
        """add a layout for a specific grid"""

        class Single_Level_Layout(LayoutClass):
            """layout for a single level"""

            def draw_stairwell(self, staircell, color):
                """mark a stairwell"""
                downcell = staircell.topology["down"]
                if staircell.have_passage(downcell):
                    if downcell in self.grid.cells.values():
                        self.draw_downstairs(downcell, color)

                upcell = staircell.topology["up"]
                if staircell.have_passage(upcell):
                    if upcell in self.grid.cells.values():
                        self.draw_upstairs(upcell, color)

            def draw_upstairs(self, upcell, color):
                """mark the upstairs end of a stairwell"""
                x, y = upcell.position
                half = upcell.scale / 2
                if half > upcell.inset:
                    half -= upcell.inset

                        # landing (current level)
                X = [x - 0.4*half, x + 0.4*half, x + 0.3*half,
                     x - 0.5*half, x - 0.4*half]
                Y = [y, y, y + 0.2*half, y + 0.2*half, y]
                layout.draw_polyline(X, Y, color)

                        # drop
                X = [x + 0.3*half, x + 0.3*half, x - 0.5*half,
                     x - 0.5*half]
                Y = [y + 0.2*half, y + 0.4*half, y + 0.4*half,
                     y + 0.2*half]
                layout.draw_polyline(X, Y, color)

                        # step down (towards bottom)
                X = [x + 0.3*half, x + 0.2*half, x - 0.6*half,
                     x - 0.5*half]
                Y = [y + 0.4*half, y + 0.6*half, y + 0.6*half,
                     y + 0.4*half]
                layout.draw_polyline(X, Y, color)

            def draw_downstairs(self, downcell, color):
                """mark the upstairs end of a stairwell"""
                x, y = downcell.position
                half = downcell.scale / 2
                if half > downcell.inset:
                    half -= downcell.inset

                        # landing (current level)
                X = [x - 0.4*half, x + 0.4*half, x + 0.5*half,
                     x - 0.3*half, x - 0.4*half]
                Y = [y, y, y - 0.2*half, y - 0.2*half, y]
                layout.draw_polyline(X, Y, color)

                        # rise
                X = [x + 0.5*half, x + 0.5*half, x - 0.3*half,
                     x - 0.3*half]
                Y = [y - 0.2*half, y - 0.4*half, y - 0.4*half,
                     y - 0.2*half]
                layout.draw_polyline(X, Y, color)

                        # step up (towards top)
                X = [x + 0.5*half, x + 0.6*half, x - 0.2*half,
                     x - 0.3*half]
                Y = [y - 0.4*half, y - 0.6*half, y - 0.6*half,
                     y - 0.4*half]
                layout.draw_polyline(X, Y, color)

        level = self.grid.levelOf[grid]
        layout = Single_Level_Layout(grid, self.plt, **kwargs)
        self.layouts[level] = layout
        return layout

    def add_layouts(self, LayoutClass, **kwargs):
        """add a layout for each grid"""
        for grid in self.grid.levels:
            add_layout_for_grid(grid, LayoutClass, **kwargs)

    def draw_grid(self, linecolor="black", deadcolor="red"):
        """plot the grid"""
                # plot the member grids
        for level in self.layouts:
            layout = self.layouts[level]
            print("Plotting level %d...%s" % (level, layout.grid.name))
                # first ignoring stairwells...
            layout.draw_grid(linecolor)
                # now fill in the stairwells...
                # here we are assuming the number of stairwells is small
            for staircell in self.grid.stairs:
                layout.draw_stairwell(staircell, linecolor)
        if self.kwargs["schematic"]:
            self.draw_schematic(linecolor, deadcolor)

    def draw_schematic(self, linecolor="black", deadcolor="red"):
        """draw a simple schematic showing levels and stairwells

        Coordinate conversion:

            For more background, see any introductory text on linear
            algebra.  (Topics: systems of equations, echelon for,
            elementary row operations.) In Lay [2], all the relevant
            background is in Chapter 1.

            We want to convert (row, column, level) or (i, j, L)
            coordinates to (x, y) coordinates.

            Let M and N, respectively denote the largest number of rows
            and of columns, respectively, in all the level subgrids.

            Consider the rectangle (0, 0, L)-(M, N, L) representing
            the boundary of a largest grid placed at a given aboveground
            level L (e.g. level 1).  Converting coordinates of three of 
            the rectangle's corners gives a basis for the projection
            onto the Cartesian plane:

                (0, 0, L) ↦ (0, L)
                (0, N, L) ↦ (N, L)
                (M, 0, L) ↦ (A, B)

            (The values of A and B can be determined later.)

            The result is an augmented matrix representing the
            coordinate conversion.  We can immediately interchange
            rows to put the augmented matrix in an equivalent
            row-echelon form:

                M 0 L | A B
                0 N L | N L
                0 0 L | 0 L

            Subtract row three from rows one and two to diagonalize
            the augmented matrix:

                M 0 0 | A  B-L
                0 N 0 | N   0
                0 0 L | 0   L

            Now divide each row by the diagonal entry to put the
            augmented matrix in reduced row echelon form.  This yields
            the following basis transformation:

                (1, 0, 0) ↦ (A/M, (B-L)/M)
                (0, 1, 0) ↦ (1, 0)
                (0, 0, 1) ↦ (0, 1)

            Rearranging this yield the following coordinate
            transformation:

                Ai/M + j ↦ x
                (B-L)i/M + L = y

            The only requirement is to find the values of A and B.
            To do this, we consider level 0 and the point (M, 0, 0)
            in (i, j, L) space.  We don't want the projected grids
            to overlap and we want to view grids from above, so
            0 < B-L < M.  We will take B-L = M/2.  We also want
            0 < A < M/2, so we will take A = M/4.
        """
        a = 0.5               # a = A/M = 1/2
        b = 0.25              # b = (B-L)/2 = 1/4
        M, N = 1, 1
        for level in self.layouts:
            layout = self.layouts[level]
            grid = layout.grid
            M = max(M, grid.rows)
            N = max(N, grid.cols)

        for level in self.layouts:
                # draw a schematic representing the level
            layout = self.layouts[level]
            grid = layout.grid
            m, n = grid.rows / M, grid.cols / N
            A, B = a * m, b * m + level
            X = [0, n, A + n, A, 0]
            Y = [level, level, B, B, level]
            self.draw_polyline(X, Y, linecolor)
        grid = self.grid
        for staircell in grid.stairs:
            downcell = staircell["down"]
            i0, j0 = downcell.index
            i0, j0 = i0 / M, j0 / N
            level = grid.stairs[staircell]
            upcell = staircell["up"]
            i1, j1 = upcell.index
            i1, j1 = i1 / M, j1 / N
            i2, j2 = (i0 + i1)/2, (j0 + j1)/2
            
                # stairwell down
            X = [a * i0 + j0, a * i2 + j2]
            Y = [b * i0 + level, b * i2 + level + 0.5]
            if staircell.have_passage(downcell):
                self.draw_polyline(X, Y, linecolor)
            else:
                self.draw_polyline(X, Y, deadcolor)
            
                # stairwell up
            X = [a * i1 + j1, a * i2 + j2]
            Y = [b * i1 + level + 1, b * i2 + level + 0.5]
            if staircell.have_passage(upcell):
                self.draw_polyline(X, Y, linecolor)
            else:
                self.draw_polyline(X, Y, deadcolor)

class Multilevel_Projective_Layout(Multilevel_Layout):
    """layout for multilevel mazes using perspective projection"""

    def draw_schematic(self, linecolor="black", deadcolor="red"):
        """draw a perspective schematic showing levels and stairwells

        This schematic uses a perspective projection which may look
        a bit more natural than the schematic above.

        Coordinate conversion:

            The necessary background may be found in Lay [2], section
            2.8 (Applications to Computer Graphics), pages 160-162
            (Perspective Projections).  The perspective projection is
            uses facts about similar triangle.

            Let the levels run from we imagine standing on the z-axis
            at (0, 0, d).  Using similar triangles, the point (u, v, w)
            in (x, y, z) space projects onto the (x, y) plane at:

                x = u / (1 - w/d)       (depth d)
                y = v / (1 - w/d)

            The issues then become (a) where we want to stand, and (b)
            where should we place our maze.  We want d>0 and w<d.
            If we imagine the back of the maze is on the (x, y) plane,
            and the front is at z=1, then a natural choice for d is 2.
            Placement of the maze insures that 0 <= w <= 1.
            We'd like to have a good view of both top and bottom,
            so we want to center the maze vertically.

            As above, let M be the maximum number of rows, N the maximum
            number of columns, and L the number of levels.  We transform
            (row, column, level) or (i, j, l) coordinates as follows:

                (i, j, l) ↦ (j/M+0.5, 1.2l-0.6L, 1-i/M)

            Individually:

                u=j/M+0.5: places the rows to the right of the viewer
                    and preserves row/column aspect ratio
                v=1.2l-0.6L: centers the maze vertically and avoids
                    overlapping quadrilaterals
                w=1-i/M:  keeps the depth of the maze between 0 and 1
                    in the schematic, with higher rows away from the
                    viewer
        """
        def transform(i, j, l, M, N, L):
            """coordinate transformation"""
            u, v, w = j/M + 0.5, 1.2*l - 0.6*L, 1 - i/M
            denom = 1-w/2
            return u/denom, v/denom

        M, N, L = 1, 1, 0
        for level in self.layouts:
            layout = self.layouts[level]
            grid = layout.grid
            M = max(M, grid.rows)
            N = max(N, grid.cols)
            L += 1

        for level in self.layouts:
                # draw a schematic representing the level
            layout = self.layouts[level]
            grid = layout.grid
            m, n = grid.rows, grid.cols
            rect = [[0, 0], [0, n], [m, n], [m, 0], [0, 0]]
            X, Y = [], []
            for k in range(5):
                i, j = rect[k]
                x, y = transform(i, j, level, M, N, L)
                X.append(x)
                Y.append(y)
            self.draw_polyline(X, Y, linecolor)

        grid = self.grid
        for staircell in grid.stairs:
            downcell = staircell["down"]
            i0, j0 = downcell.index
            level = grid.stairs[staircell]
            upcell = staircell["up"]
            i1, j1 = upcell.index
            i2, j2 = (i0 + i1)/2, (j0 + j1)/2

                # stairwell down
            x1, y1 = transform(i0, j0, level, M, N, L)
            x2, y2 = transform(i2, j2, level+0.5, M, N, L)
            X = [x1, x2]
            Y = [y1, y2]
            if staircell.have_passage(downcell):
                self.draw_polyline(X, Y, linecolor)
            else:
                self.draw_polyline(X, Y, deadcolor)
            
                # stairwell up
            x1, y1 = transform(i1, j1, level+1, M, N, L)
            X = [x1, x2]
            Y = [y1, y2]
            if staircell.have_passage(upcell):
                self.draw_polyline(X, Y, linecolor)
            else:
                self.draw_polyline(X, Y, deadcolor)

# END: layout_plot_multilevel.py
