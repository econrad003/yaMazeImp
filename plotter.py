# -*- coding: utf-8 -*-
# plotter.py - a plotter class for mazes
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
#     27 Apr 2020 - Initial version
#     30 Apr 2020 - Initialize self.settings[cell]
"""
plotter.py - basic plotter implementation for mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

class Plotter(object):
    """base class for maze plotting"""

    ID = -1                 # source for a unique identifier for the plotter

    def __init__(self, grid, **kwargs):
        """constructor

        Mandatory arguments:
            grid - the associated grid object

        Optional named arguments:
            name - a name for the plotter
            title - a title for the plot
        """
            # unique identifier
        Plotter.ID += 1
        self.id = Plotter.ID

            # plotter management
        self.name = kwargs["name"] if "name" in kwargs \
            else "Plotter{x}".format(x=self.id)
        self.title = kwargs["title"] if "title" in kwargs \
            else "Untitled{x}".format(x=self.id)
        self.kwargs = kwargs

            # maze management
        self.grid = grid              # the passages in the neighborhood
        self.settings = {}            # plotter settings
        for cell in grid.each():      # plotter cell settings - 30 Apr 2020
            self.settings[cell] = {}

        self.configure()              # configure the settings
        self.open()                   # create the plotter object

            # basic plotter management

    def configure(self):
        """configure the plotter object settings"""
        pass

    def open(self):
        """open a plotter"""
        self.plotter = None           # customize this

    def close(self):
        """close the plotter"""
        pass                          # customize this

    def show(self):
        """display the plot"""
        pass                          # customize this

    def save(self, filename=None):
        """save the plot to a file"""
        pass

            # drawing

    def draw_cell(self, cell):
        """draw an individual cell"""
        pass                          # customize this

    def draw_passage(self, cell, nbr):
        """draw the maze"""
        pass                          # customize this

    def draw(self):
        """draw the maze"""
        pass                          # customize this

# END: plotter.py
