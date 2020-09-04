# -*- coding: utf-8 -*-
# high_card_wins.py - spanning tree(?) algorithm
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
#     30 Aug 2020 - Initial version
"""
high_card_wins.py - spanning forest algorithm implementation
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

Algorithm:

    Initialization:

        Color each component with a unique color.  (If any cells are
        linked at start, they will have the same color.)

    Play: (for each cell)

        From the given cell's neighbors, select only those neighbors which
        are in different components.  If there are none, continue with the
        next cell.

        With this selection of neighbors, play a round of high card wins to
        select a winner.

        Carve a passage between the cell and the winner and adjust the
        coloring accordingly.

    Outcome:

        The game is won if the maze is connected.

Remarks:

    This is an algorithm based on the binary tree algorithm given in
    [1], but, unlike that algorithm, it is not guaranteed to produce a
    spanning tree.  Moreover, the resulting spanning subgraph will not 
    in general be binary.  It will however produce a spanning forest,
    i.e. the resulting forest need not be connected.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

Bugs and Features:

    See discussion above.
"""

from random import random, choice, shuffle

class High_Card_Wins:
    """implementation of the high-card-wins spanning forest algorithm"""

    class State(object):
        """state matrix for the high-card-wins algorithm"""

        def __init__(self, grid, mustShuffle=True):
            """constructor

            Parameters:
                grid - the grid to be carved
                choose - a function which takes a cell and either returns a 
                    winning neighbor or None
            """
            self.grid = grid

                # component management
            self.next_component = 0     # the components initial color
            self.components = {}        # componentOf[cell] = color
            self.cells = {}             # cells[color] = [cell1, cell2, ...]

                # initialization of component structures
            self.initialize()
            self.configure()

                # get a list of cells to process
            self.queue = list(self.components.keys())
            if mustShuffle:
                shuffle(self.queue)
            self.requeue = self.queue[:]

        def initialize(self):
            """assign a unique color to each cell"""
            for cell in self.grid.each():
                self.components[cell] = self.next_component
                self.cells[self.next_component] = [cell]
                self.next_component += 1

        def configure(self):
            """collect components"""
            for cell in self.grid.each():
                for nbr in cell.passages():
                    self.recolor(cell, nbr)

        def recolor(self, cell, nbr):
            """recolor adjacent components"""
            color1 = self.components[cell]
            color2 = self.components[nbr]
            if color1 > color2:
                self.recolor(nbr, cell)
                return
            assert color1 != color2, "recoloring error"

            for u in self.cells[color2]:
                self.cells[color1].append(u)
                self.components[u] = color1
            del self.cells[color2]

        def merge(self, cell, nbr):
            """link a cell with a differently-colored neighbor"""
            color1 = self.components[cell]
            color2 = self.components[nbr]
            if color1 == color2:
                return False          # failure
            self.recolor(cell, nbr)
            cell.makePassage(nbr)
            return True               # success

                # the next two routines can be overridden to enable
                # 'cheating'.  For example see Binary_Tree_State
                # below...

        def neighbors(self, cell):
            """a list of admissible neighbors"""
            players = []
            for nbr in cell.neighbors():
                color1 = self.components[cell]
                color2 = self.components[nbr]
                if color1 != color2:
                    players.append(nbr)
            return players

        def play_one_round(self, cell):
            """one round of high card wins"""
            players = self.neighbors(cell)      # admissible neighbors
            if players:
                winner = choice(players)
                if winner:
                    self.merge(cell, winner)

        def replenish_if(self, prevcomponents):
            """restock the queue for another pass"""
            curr = len(self.cells)

                # we don't replenish if either:
                #     (1) we have fewer than two components
                #     (2) the last pass failed to reduce the components
            if curr > 1 and curr != prevcomponents:
                    # replenish
                self.queue = self.requeue[:]
            return curr

    @classmethod
    def on(cls, grid, state=None):
        """carve a spanning forest maze by playing high card wins

        Mandatory arguments:
            grid - a grid

        Optional named arguments:
            state - a state matrix
        """
        if not state:
            state = cls.State(grid)

        print("High Card Wins: start with %d cells in %d components" \
            % (len(state.grid), len(state.cells)))

        prev = len(state.cells)
        while state.queue:
            cell = state.queue.pop()
            state.play_one_round(cell)
            if not state.queue:
                prev = state.replenish_if(prev)
                if state.queue:
                    print("  -- next pass: %d components" % prev)

        print("High Card Wins: end with %d cells in %d components" \
            % (len(state.grid), len(state.cells)))
        if len(state.cells) is 1:
            return True           # win (spanning tree)
        return False              # lose (disconnected)

class NAry_Tree_State(High_Card_Wins.State):
    """a n-ary tree algorithm based on high card wins

    This is the same as the binary tree algorithm from the Jamis Buck
    book [1].
    """

    def __init__(self, grid, directions=["east", "north"], biases=None):
        """constructor

        Optional arguments:
            directions - a list of admissible directions
            biases - a list of weights (for cheating) or None

        The directions should normally be orthogonal, e.g.:
            ["east", "north"]
            ["east", "south"]
            ["northeast", "southeast"]
            ["east", "north", "up"]
            ["east", "north", "up", "widdershins"]
            ["inward", "ccw"]

        Each player has his own deck of cards.  Cards are drawn once
        per round, with (for all practical purposes) replacement.

        For an east-north weighted game favoring east 70% of the time
        the weights should be [1, 0.7].  For three-party (or more) game,
        choosing weights will be more complicated.
        """
        super().__init__(grid, mustShuffle=False)
        self.directions = directions
        self.biases = biases

    def neighbors(self, cell):
        """get the admissible neighbors"""
        players = []
        for i in range(len(self.directions)):
                # add a neighbor if it is admissible
            direction = self.directions[i]
            nbr = cell[direction]
            if nbr and self.components[cell] != self.components[nbr]:
                if self.biases:             # cheating
                    players.append([nbr, self.biases[i]])
                else:                       # fair game
                    players.append(nbr)

        return players

    def cheat(self, players):
        """one round with cheaters"""
            # player 1 is the default winner
        winner, bias = players[0]
        high_card = -1

        for x in players:
            player, bias = x
            show_card = bias * random()       # show a card
            if show_card > high_card:         # new winner!
                winner, high_card = player, show_card

        return winner

    def play_one_round(self, cell):
        """one round of high card wins"""
        players = self.neighbors(cell)      # admissible neighbors
        if players:
            winner = self.cheat(players) if self.biases \
                else choice(players)
            self.merge(cell, winner)

# END: high_card_wins.py
