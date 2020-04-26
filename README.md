# yaMazeImp
Yet another maze implementation
-- Eric Conrad

Python3 implementations of maze algorithms.

* binary_tree.py - a basic binary tree algorithm for 4-neighbor rectangular grids (1)
  * this is an adaptation of the first algorithm in Mazes for Programmers - it always produces long chains of passages along two of the four boundary walls.
* binary_tree_demo.py - a demonstration program for binary_tree.py
* binary_tree2.py - a greedy algorithm which attempts to produce a binary spanning tree (2)
  * the resulting mazes are biased in the early stages towards cells with passage-degree 3 (the greedy condition);
  * long runs along the boundary walls are not common;
  * I believe this should work on rectangular grids and Moebius strip grids, but I haven't worked out a proof in full detail;
  * it may fail on cylindrical grids, but my experiments indicate that failure is rare.
* binary_tree2_demo.py - a demonstration program for binary_tree2.py
* cell.py - a base class for cells in a grid
* cylinder.py - a cylinder maze class based on rectangular_grid.py
  * this includes tweakings of the algorithms in binary_tree.py and sidewinder.py
* cylinder_demo.py - a demonstration program for cylinder.py
* grid.py - a base class for grids and mazes
* helpers.py - some miscellaneous algorithms to help with tweaking, with component detection, and with circuit detection.
* moebius_grid.py - a Moebius strip grid implementation
* moebius_demo.py - a demonstration program for moebius_grid.py (incomplete)
* rectangular_grid.py - a basic rectangular grid implementation
* sidewinder.py - the sidewinder algorithm, a modification of the algorithm in binary_tree.py (1)
  * this algorithm eliminates one of the long passages that are produced in binary_tree.py
* sidewinder_demo.py - a demonstration program for sidewinder.py
* square_cell.py - a asquare cell implementation
* statistics.py - some maze statistics (Euler counting of grid edges, maze walls and maze passages, cell counts, passage degree sequences, etc.)

Notes:

  1. These algorithms are essentially the ones described in *Mazes for Programmers* by Jamis Buck and published in 2015 by the Pragmatic Bookshelf. Please support the author and make yourself by buying your own personal copy of the book.
  
  2. These algorithms are not described in the Jamis Buck book.
