#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# recursive_division_demo5.py - demonstrate recursive division with multiple
#     texturing algorithms
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
#     13 Aug 2020 - Initial version
##############################################################################
"""
recursive_division_demo5.py - demonstrate recursive division with
    varied texturing
Copyright ©2020 by Eric Conrad
License: GNU General Public License version 3 (GNU GPLv3)

For more information, see documentation in 'recursive_division_demo.py'.

References:

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).
"""
import recursive_division as rd
import recursive_division_demo as demo

if __name__ == "__main__":
    print("Recursive Division Test Script (continued)...")
    print("Test 5:")
        # test 5
    maze = demo.make_grid(30, 40)
    state = rd.Random_Texture_State(maze, golden=True)
    demo.generate_maze(maze)
    filename = "demos/recursive_division_demo5.png"
    demo.render(maze, filename, \
        "Recursive Division\n(various textures, Fibonacci)")

# END: recursive_division_demo5.py
