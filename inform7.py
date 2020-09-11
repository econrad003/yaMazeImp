# -*- coding: utf-8 -*-
# inform7.py - class for generating Inform 7 code
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
#     4 Sep 2020 - Initial version
"""
grid3d.py - three-dimensional oblong grid and maze implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

The class 'Inform7' generates Inform 7 code from a maze
configuration

Bugs:

    Unknown.
"""

class Inform7(object):
    """Inform7 code generator class"""

    def __init__(self, config, **kwargs):
        """constructor

        Mandatory Named Parameters:
            config - a configparser configuration object

        Optional Named Arguments:
            filename - if present, output will be captured to this file
            console - if present, output will be displayed to stdout
            noExitList - don't generate a list of exits
        """
        self.directions = {"south", "southeast", "east", "northeast", \
            "north", "northwest", "west", "southwest", \
            "up", "down"}
        self.opposites = {"south":"north", "southeast":"northwest", \
            "east":"west", "northeast":"southwest", "north":"south", \
            "northwest":"southeast", "west":"east", \
            "southwest":"northeast", "up":"down", "down":"up"}
        self.config = config
        self.kwargs = kwargs
        self.console = "console" in kwargs
        self.output = open(filename, 'w') if "filename" in kwargs \
            else None
        self.autoname = 1
        self.oneways = 0
        self.cells = {}
        self.topology = {}
        self.arcs = {}
        self.edges = {}
        for section in config.sections():
            self.parse(section)
        for index in self.cells:
            self.identify_edges(index)

        # build references to important information

    def parse(self, section):
        """first pass parsing"""
        if section[:4] == "cell":
            self.parse_cell(section)
            return
        return

    def parse_cell(self, section):
        """get cell information"""

        def new_name():
            """create a cell name"""
            name = "UnnamedCell" + str(self.autoname)
            self.autoname += 1
            return name

        apropos = self.config[section]
        index = section[5:]
        name = new_name()
        if "name" in apropos and apropos["name"] != index:
            name = apropos["name"]
        self.cells[index] = name
        self.topology[index] = {}
        self.arcs[index] = {}

        for direction in self.directions:
            if direction in apropos:
                self.topology[index][direction] = apropos[direction]
                key = "arc_" + direction
                if key in apropos:
                    self.arcs[index][direction] = apropos[key]

    def identify_edges(self, index):
        """identify the two-way connections (edges)"""
        for direction in self.arcs[index]:
            if direction not in self.opposites:
                continue
            opposite = self.opposites[direction]
            key = self.topology[index][direction]
            if key in self.cells:
                if opposite in self.arcs[key]:
                    if self.topology[key][opposite] == index:
                        self.edges[frozenset([index, key])] = 1
                        continue
                self.oneways += 1       # this link is one-way

    def writeln(self, line):
        """write a single line of output"""
        if self.console:
            print(line)
        if self.output:
            self.output.write(line + "\n")

    def generate_prologue(self):
        """prelude - any required definitions should go here"""
        if self.oneways:
            self.writeln("Section - Definitions - Linkage")
            self.writeln("")
            self.writeln("\t[ %d one-way connections were found " + \
                "in preprocessing. The following definitions " + \
                "facilitate creating one-way connections.  They " + \
                "are modelled after the definitions of 'above' " + \
                "and 'below' in the Standard Rules extension. ]")
            self.writeln("")
            for direction in self.directions:
                if direction in {"up", "down"}:
                        # these already have 'above' and 'below'
                    continue
                self.writeln("The verb to be %sward from means " + \
                    "the reversed mapping %s relation." \
                    % (direction, direction))

    @staticmethod
    def preposition(direction):
        """turn a direction into prepositional form"""
        if direction == "up":
            return "above"
        if direction == "down":
            return "below"
        return "%sward from" % direction

    @staticmethod
    def lone_exit(direction):
        """describe a lonely exit"""
        return "The only apparent exit is %s." % direction

    @staticmethod
    def several_exits(directions):
        """describe a number of exits"""
        exitlist = "There are exits leading "
        for i in range(len(directions)):
            if i > 0:
                if i < len(directions)-1:
                    exitlist += ", "
                else:
                    exitlist += " and "
            exitlist += directions[i]
        exitlist += "."
        return exitlist

    def about_cell(self, cell, mentioned):
        """write about a cell"""
        key = "cell:" + cell
        self.writeln("[ cell index: %s ]" % str(cell))
        section = self.config[key]
        roomtype = section["type"] if "type" in section else "room"
            # a simple start: CELL is a ROOM.
        paragraph = "%s is a %s." % (self.cells[cell], roomtype)

            # describe its arcs.  (We can now refer to CELL as IT)
        exits = []
        for direction in self.arcs[cell]:
            nbr = self.topology[cell][direction]
            opposite = self.opposites[direction]
            exits.append(direction)
            if frozenset([cell, nbr]) in self.edges:
                    # two-way connection
                if nbr in mentioned:
                    sentence = "It is %s from %s." \
                         % (opposite, self.cells[nbr])
                    paragraph += "  " + sentence
            else:
                    # one-way connection
                sentence = "It is a room %s %s." \
                    % (self.preposition(opposite), self.cells[nbr])
                paragraph += "  " + sentence

            # build its description 
        description = section["desc"] if "desc" in section else ""
        exitlist = ""
        if "noExitList" not in self.kwargs:
            if len(exits) is 1:
                exitlist += self.lone_exit(exits[0])
            elif len(exits) is 0:
                exitlist = "There are no apparent exits."
            else:
                exitlist = self.several_exits(exits)
        if description and exitlist:
            description += "[paragraph break]" + exitlist
        elif exitlist:
            description = exitlist
        paragraph += "  The description is \"%s\"." % description

                # is there a printed name?
        printed = section["print"] if "print" in section else ""
        if printed:
            paragraph += "  The printed name is \"%s\"." % printed

                # now write!
        self.writeln(paragraph)
        self.writeln("")

    def generate_main_body(self):
        """generate the room definitions"""
        mentioned = {}
        for cell in self.cells:
            mentioned[cell] = 1
            self.about_cell(cell, mentioned)

    def generate_epilogue(self):
        """generate any tail-end code"""
        pass

    def generate(self):
        """code generation"""
        self.writeln("Part - Generated Maze")
        self.writeln("")
        self.writeln("Chapter - Prologue")
        self.writeln("")
        self.generate_prologue()
        self.writeln("")
        self.writeln("Chapter - Main Matter")
        self.writeln("")
        self.generate_main_body()
        self.writeln("")
        self.writeln("Section - Epilogue")
        self.writeln("")
        self.generate_epilogue()
        self.writeln("")
        self.writeln("\t[ end of generated code ]")
        self.writeln("")

# END: inform7.py
