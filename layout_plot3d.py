# -*- coding: utf-8 -*-
# layout_plot3d.py - a layout class for 3d mazes
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
#     3 Sep 2020 - Initial version
"""
layout_plot_color.py - basic plotting with color for rectangular mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

import matplotlib.patches as patches

class Plot3D_Layout(object):
    """implementation of 3-D maze with colored cells"""
    
    def __init__(self, grid, plt, dim, **kwargs):
        """constructor"""
        self.color = {}               # default - no colors
        self.palette ={}              # palette
        m, n = self.dim = dim
        assert m*n >= len(grid.levels)
        self.fig, self.axs = plt.subplots(m, n)
        if "title" in kwargs:
            self.fig.suptitle(kwargs["title"])
        self.kwargs = kwargs
        self.grid = grid
        self.layouts = {}
        j = 0
        k = 0
        i = 0
        for j in range(m):
            for k in range(n):
                    # assign a layout to a set of axes
                if m > 1:
                    if n > 1:
                        ax = self.axs[j, k]
                    else:
                        ax = self.axs[j]
                else:
                    if n > 1:
                        ax = self.axs[k]
                    else:
                        ax = self.axs
                ax.set(aspect=1)
                ax.axis('off')

                if i in range(len(grid.levels)):
                    level = grid.levels[i]
                    layout = [self.fig, ax]
                    ax.set_title(str(level))
                    self.layouts[tuple(level)] = layout
                i += 1

    def draw_grid(self, linecolor="black"):
        """plot the grid"""
        for cell in self.grid.each():
            self.draw_cell(cell, linecolor)

    def draw_cell(self, cell, color):
        """draw a square cell with no inset"""
        i, j, k, rest = self.grid.from_cell(cell)
        level = tuple([k] + rest)
        fig, ax = self.layouts[level]

            # draw the cell
        x, y = 2*j, 2*i           # lower left corner
        if "underCell" not in cell.kwargs:
            facecolor = self.palette[self.color[cell]] \
                if cell in self.color else 'white'
            rect = patches.Rectangle((x, y), 1.5, 1.5, \
                edgecolor=color, facecolor=facecolor)
            ax.add_patch(rect)

            # draw the planar connections
        if cell.status("south"):
            X = [x+0.75, x+0.75]
            Y = [y, y-0.25]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("southeast"):
            X = [x+1.5, x+1.75]
            Y = [y, y-0.25]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("east"):
            X = [x+1.5, x+1.75]
            Y = [y+0.75, y+0.75]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("northeast"):
            X = [x+1.5, x+1.75]
            Y = [y+1.5, y+1.75]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("north"):
            X = [x+0.75, x+0.75]
            Y = [y+1.5, y+1.75]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("northwest"):
            X = [x, x-0.25]
            Y = [y+1.5, y+1.75]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("west"):
            X = [x, x-0.25]
            Y = [y+0.75, y+0.75]
            self.draw_polyline(ax, X, Y, color)
        if cell.status("southwest"):
            X = [x, x-0.25]
            Y = [y, y-0.25]
            self.draw_polyline(ax, X, Y, color)

            # draw the up-down connections
        if cell.status("up"):
            X = [x+1, x+1.2, x+1.4]
            Y = [y+1, y+1.3, y+1]
            self.draw_polyline(ax, X, Y, color)     # ^ in upper right
        if cell.status("down"):
            X = [x+1, x+1.2, x+1.4]
            Y = [y+0.5, y+0.2, y+0.5]
            self.draw_polyline(ax, X, Y, color)     # v in lower right

    def draw_polyline(self, ax, X, Y, linecolor):
        """draw a wall"""
        ax.plot(X, Y, color=linecolor)

    def set_palette_color(self, ID, color):
        """load the color into the palette"""
        self.palette[ID] = color

    def set_color(self, cell, ID):
        """set the color of a cell"""
        self.color[cell] = ID

    def render(self, filename, tight=True):
        """render the output"""
        if tight:
            self.fig.savefig(filename, bbox_inches='tight', pad_inches=0.0)
        else:
            self.fig.savefig(filename)
        print('rendered figure to %s' % filename)

# END: layout_plot3d.py
