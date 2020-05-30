# -*- coding: utf-8 -*-
# layout_graphviz.py - a layout class for mazes using GraphViz/dot
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
#     28 Apr 2020 - Initial version
"""
layout_graphviz.py - basic plotter implementation for mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from graphviz import Digraph

class Layout(object):
    """implementation of rudimentary maze layout using GraphViz"""
    
    def __init__(self, grid, **kwargs):
        """constructor

        The layout uses a digraph object as arcs are directed.  An arrowless
        arc is used to represent two-way passages.

        The rendering engine should be set here, for example:
            foo = Layout(grid, engine='fdp')

        The default layout engine is 'dot'.

        The rendering engine can be changed, for example:
            foo = Layout(grid)
            foo.dot.engine('fdp')
        """
        self.grid = grid

        if 'comment' not in kwargs:
            kwargs['comment'] = 'GraphViz Layout'

        if 'filename' not in kwargs:
            kwargs['filename'] = 'demos/maze.gv'
        self.filename = kwargs['filename']

        if 'format' not in kwargs:
            kwargs['format'] = 'png'
        self.rendername = self.filename + '.' + kwargs['format']

        if 'name' not in kwargs:
            kwargs['name'] = grid.name

        self.dot = Digraph(**kwargs)

    def draw_cell(self, cell):
        """draw a cell"""
        kwargs = cell.kwargs['graphviz'] if 'graphviz' in cell.kwargs \
            else {}
        self.dot.node(cell.name, **kwargs)

    def draw_passage(self, cell, nbr, **kwargs):
        """draw a passage"""
        self.dot.edge(cell.name, nbr.name, **kwargs)

    def set_attribute(self, name, **kwargs):
        """set attributes"""
        if kwargs:
            self.dot.attr(name, **kwargs)

    def draw(self, cellargs={}, passageargs={}):
        """draw the maze"""
        visited = {}
        self.set_attribute('node', **cellargs)
        self.set_attribute('edge', **passageargs)
                # define the cells
        for cell in self.grid.each():
            self.draw_cell(cell)
                # define the arcs and edges
        for cell in self.grid.each():
            for nbr in cell.arcs:
                if cell in nbr.arcs:        # two-way passage
                    if nbr not in visited:
                        self.draw_passage(cell, nbr, arrowhead='none')
                else:
                    self.draw_passage(cell, nbr)
            visited[cell] = 1

    def set_square_cells(self):
        """configuration for a rectangular maze

        The preferred rending engines for 'pos' are 'fdp' and 'neato'.
        """
        for cell in self.grid.each():
            if 'graphviz' not in cell.kwargs:
                cell.kwargs['graphviz'] = {}
            cell.kwargs['graphviz']['pos'] = '%f,%f!' % cell.position
            cell.kwargs['graphviz']['label'] = ''
            cell.kwargs['graphviz']['shape'] = 'box'

    def set_cell(self, cell, **kwargs):
        """configuration for a particular cell"""
        if 'graphviz' not in cell.kwargs:
            cell.kwargs['graphviz'] = {}
        for name in kwargs:
            if kwargs[name] is None:
                del cell.kwargs['graphviz'][name]
            else:
                cell.kwargs['graphviz'][name] = kwargs[name]

    def render(self):
        """render the output"""
        self.dot.render()
        print('saved to %s' % self.filename)
        print('rendered to %s' % self.rendername)

# END: layout_graphviz.py
