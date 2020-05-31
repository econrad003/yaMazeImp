# yaMazeImp
Yet another maze implementation
Eric Conrad

## 1 Description

This is a collection of maze algorithms and scripts that were implemented primarily in *Python* 3.  Most of these programs are based on suggestions and ideas found in an wonderful little book by Jamis Buck called *Mazes for Programmers*.  See the references at the end for more information.  (My recommendation: buy this book.  In addition to learning about mazes, you will pick up some graph theory and *ruby* language programming.)  I've made some departures from Buck's approaches, so my programs are not simply translations from *ruby* into *python*.

## 2 Scripts

* *make-maze.py* - a script to create rectangular mazes using standard algorithms
* *texturizer.py* - a script to create texture matrices using standard algorithms
* *eval-xxxxx.py* - a collection of scripts to generate a number of mazes using a given algorithm and collect statistics on those mazes
* *xxxxx-demo.py* - a collection of scripts to demonstrate particular objects, including special kinds of mazes ( for example: polar mazes, sigma mazes, delta mazes, upsilon mazes) or to test features (such as layout programs)

The scripts *entab.py* and *detab.py* are respectively a script to replace spaces by tabs and a script to replace tabs by spaces.  They have nothing to do with mazes.  I use them because the text editor that I use (Gnome's TextEditor) cannot be configured to use spaces for Python and tabs for some other language.  The space/tab configuration is all or nothing.  Nor can it be configured correctly to do entabbing or detabbing.

## 3 Algorithms

### 3.1 Maze Generation

In the descriptions, the terms spanning tree and perfect maze are used interchangeably.  They do really mean exactly the same thing.  They only differ in the underlying context.

* *aldous_broder.py* - implementations of the first-entrance random walk algorithm (Aldous/Broder) and the last-exit random walk algorithm (reverse Aldous/Broder) for generating (theoretically) uniformly random spanning trees on a connected simple graph, or equivalently, uniformly random perfect mazes on a connected grid. (The first-entrance algorithm is described in Buck (2015).)  The algorithm tends to start quickly and end slowly, unlike Wilson's algorithm which tends to start slowly and end quickly.
* *binary_tree.py* - implementation of a simple binary spanning tree algorithm for rectangular mazes.  This is the binary tree algorithm described in Buck (2015).
* *binary_tree2.py* - implementation of a binary tree algorithm that works most of the time for generating perfect mazes on arbitrary grids.  When it fails, the result is a binary spanning forest. When used on rectangular grids, the result is typically a binary spanning tree which cannot be produced by Jamis Buck's binary tree algorithm.
* *hunt_and_kill.py* - an implementation of the Hunt and Kill algorithm described in Chapter 5 of Buck (2015).
* *recursive_backtracker.py* - the unfortunately misnamed depth-first search algorithm for producing perfect mazes in a connected grid.  The implementation is stack-based to avoid recursion.  (See also: *tree_search.py*.)
* *sidewinder.py* - a modification of Buck's binary spanning tree algorithm which eliminates one bias in that algorithm.  It only works on rectangular grids or (more generally) on grids which can be traversed in two orthogonal directions.  The resulting spanning trees can be binary, but usually are not.
* *tree_search.py* -  included are alternative spanning tree search algorithms using a queue (breadth-first search) or a priority-queue (best-first search).  These complement the stack-based depth-first search algorithm used in *recursive-backtracker.py*.
* *wilson.py* - Wilson's algorithm, a theoretically unbiased spanning tree algorithm that uses a loop-erased random walk of the grid.  In addition, the program includes a hybrid Aldous/Broder/Wilson algorithm that starts the random walk using the first-entrance algorithm of Aldous and Broder and finishes using the loop-erased random walk due to Wilson.  Wilson's algorithm tends to start slowly and end quickly.  The hybrid algorithm tends to start and end quickly, slowing down as it approaches the middle using Aldous/Broder, then speeding up after Wilson's algorithm takes control.  I don't know whether the hybrid algorithm is biased.

### 3.2 Other Algorithms

* *norms.py* - Dijkstra's algorithm for finding distances, shortest path, longest path, *etc.*

## 4 Grids and cells

The programs *grid.py* and *cell.py* describe the basic grid and cell classes that underly all mazes and the grids that they span.

* *cylinder_grid* - a modified rectangular grid of square cells in which the east and west edges are identified.
* *masked_grid.py* - a grid which mirrors part another grid, essentially producing a subgrid.  Actions in the subgrid are mirrored in the parent.
* *moebius_grid* - a modified rectangular grid of square cells in which the east and west edges are identified with a twist, resulting in a Moebius strip 
* *ortho_delta_grid.py* - a grid of right triangular cells arranged in a rectangle
* *ortho_sigma_grid.py* - a grid of regular hexagonal cells arranged in an approximate rectangle, much like a beekeeper's honeycomb
* *ortho_upsilon_grid.py* - a grid consisting of alternating regular octagonal cells and square cells, arranged in an approximate rectangle
* *rectangular_grid.py* - the simple N/S/E/W rectangular grid of square cells

The function of the various cell programs should be mostly self-explanatory.  Much of the actual work is done in the grid programs and in the layout programs.  ASCII and unicode layout are handled in *rectangular_grid.py*.

### 5 Layouts

Four types of layouts are supported.  ASCII and unicode layouts are supported on rectangular grids and on grids derived from rectangular grids (for example, cylinder grids).  All grids support GraphViz/dot layout, though the results usually leave a lot to be desired.

Most derived grids support plot layouts using MatPlotLib, though in most cases, support will require some direct use of MatPlotLib methods.  See the scripts for examples.

## References

1. Buck (2015) - Jamis Buck.   *Mazes for Programmers*.  Pragmatic Bookshelf, 2015.  ISBN-13 978-1-68050-055-4.


