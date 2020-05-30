# -*- coding: utf-8 -*-
# plotter_graphviz.py - a plotter class for mazes using GraphViz
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
plotter_graphviz.py - basic plotter implementation for mazes
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs:

    Unknown.
"""

from plotter import Plotter

class GraphViz_Plotter(Plotter):
    """implementation of rudimentary maze plotting using GraphViz"""

    # Already set up in the base class:
    #   self.id - a unique identifier for the instance
    #   self.name - a name for the plot (default: "Plotter{id}")
    #   self.title - a title for the plot (default: "Untitled{id}")
    #   self.kwargs - keyword arguments
    #   self.grid - the grid object
    # At the end of base class setup, self.open() is called
    # Usage guidelines:
    #   (1) initialize (attaching the plotter object to a grid)
    #   (2) construct the maze
    #   (3) call the draw method (to create the graphViz/dot file)
    #   (4) call the close method to finalize the plot
    #   (4) call the show method to create a PNG image
    # The save method is not implemented.

            # basic plotter management

    def open(self):
        """open a plotter - called by __init__"""
            # self.plotter is set to the file descriptor of the
            #   graphViz/dot file
        filename = self.kwargs["filename"] if "filename" in self.kwargs \
            else "demos/" + self.name          # does not include extension
        self.filename = filename                  # the name of the file

            # create and open the dot file fo writing
        fp = open(filename + ".dot", "w")         # file descriptor
        self.plotter = fp                         # file descriptor

            # generator comments
        fp.write("/*" + ("*" * 70) + "\n")        # open comment
        fp.write(" * " + filename + ".dot - " + self.title + "\n")
        fp.write(" * " + "generator information:" + "\n")
        fp.write(" * " + "    (generator) plotter_graphviz.py" + "\n")
        fp.write(" * " + "       (author) Eric Conrad, 2020" + "\n")
        fp.write(" * " + self.shell_command() + "\n")
        fp.write(" *" + ("*" * 70) + "\n")        # stars for visual close
        fp.write(" */\n")                         # close comment
        fp.write("\n")                            # blank line


    def close(self):
        """close the plotter"""
        fp = self.plotter

        fp.write("\n")                            # blank line
        fp.write(" /* END of " + self.filename + ".dot */\n")
        fp.close()

    def shell_command(self):
        """create shell command (used by show() and open())"""
        command = self.kwargs["command"] if "command" in self.kwargs \
            else "dot"
        command += " "
        command += self.kwargs["args"] if "args" in self.kwargs \
            else "-Tpng -O"
        command += " "
        command += self.filename + ".dot"
        return command

    def show(self):
        """display the plot"""
        from os import system                     # command interpreter shell
        command = self.shell_command()

            # execute command
        print("shell: %s" % command)
        system(command)
        print("(done)")

            # drawing

    def parameters_to_string(self, x, label=False):
        """format a parameter as a string

        Parameters:
            x - a key into the self.settings dictionary object;
                self.settings[x] is itself a directory which represents a
                list of parameters
        
        Keys to the self.settings dictionary: (four kinds of keys)
                "node" - general node attributes
                "edge" - general edge or arc attributes
                cell - node attributes for the given cell
                (cell,nbr) - node attributes for the given arc or edge

        Example:
            self.settings["node"] = {}
            self.settings["node"]["shape"] = '"circle"'
            
            These generate the following graphViz/dot code:
                node [shape="circle"]
        """
        if x not in self.settings:
            return None

        s = " [" if label else "  " + x + "["
        m = 0
        n = len(self.settings[x])
        for parameter in self.settings[x]:         # directory
            s += ' %s=%s' % (parameter, self.settings[x][parameter])
            m += 1
            if m < n:
                s += ","

        s += " ]"
        return s

    def draw_cell(self, cell):
        """draw an individual cell"""
        fp = self.plotter
        s = '  "%s"' % cell.name
        if cell in self.settings:
            s += self.parameters_to_string(cell, label=True)
        else:
            s += " [ ]"
        s += ";\n"
        fp.write(s)

    def draw_passage(self, cell, nbr, twoway=True):
        """draw an individual passage"""
        fp = self.plotter
        s = '  "%s"' % cell.name
        s += " -> "
        s += '"%s"' % nbr.name
        index = (cell, nbr)
        if twoway:
            if index not in self.settings:
                self.settings[index] = {}
            self.settings[index]["arrowhead"] = "none"
        if index in self.settings:
            s += self.parameters_to_string(index, label=True)
        s += ";\n"
        fp.write(s)

    def draw(self):
        """draw the maze"""
        fp = self.plotter                         # file descriptor
        visited = {}                              # cells already drawn

        fp.write("digraph " + ('"%s"' % self.name) + " {\n")

            # generic node and edge setup
        s = self.parameters_to_string("node")
        if s:
            fp.write(s)
        s = self.parameters_to_string("edge")
        if s:
            fp.write(s)

            # nodes
        fp.write("    /* cells */\n")
        for cell in self.grid.each():
            self.draw_cell(cell)

            # arcs and edges
        fp.write("    /* passages */\n")
        for cell in self.grid.each():
            for nbr in cell.arcs:
                if cell in nbr.arcs:
                    if nbr not in visited:
                        self.draw_passage(cell, nbr)
                else:
                    self.draw_passage(cell, nbr, twoway=False)
            visited[cell] = 1

            # finish the graph
        if "title" in self.kwargs:                # untitled otherwise
            fp.write('  label="%s";\n' % self.kwargs["title"])
        fp.write("}\n")

class GraphViz_Plotter_Rectangular(GraphViz_Plotter):
    """configure a plot for rectangular mazes using GraphViz"""

    def configure(self):
        """configure the parameters"""
        self.kwargs["command"] = "neato"
        for cell in self.grid.each():
            if cell not in self.settings:
                self.settings[cell] = {}
            self.settings[cell]["pos"] = '"%f,%f!"' % cell.kwargs["position"]
            self.settings[cell]["label"] = '""'

# END: plotter.py
