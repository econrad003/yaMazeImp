# yaMazeImp
"Yet another maze implementation"
by Eric Conrad.

## Overview

* 1 **Description**
* 2 **Scripts**
* 2.1 **Recent changes**
* 3 **Algorithms**
* 3.1 **Maze generation**
* 3.2 **Other algorithms**
* 4 **Grids and cells**
* 5 **Layouts**
* **References**

## 1 Description

This is a collection of maze algorithms and scripts that were implemented primarily in *Python* 3.  Most of these programs are based on suggestions and ideas found in an wonderful little book by Jamis Buck called *Mazes for Programmers*.  See the references at the end for more information.  (My recommendation: buy this book.  In addition to learning about mazes, you will pick up some graph theory and *ruby* language programming.)  I've made some departures from Buck's approaches, so my programs are not simply translations from *ruby* into *python*.

## 2 Scripts

* *make\_maze.py* - a script to create rectangular mazes using standard algorithms
* *texturizer.py* - a script to create texture matrices using standard algorithms
* *eval\_xxxxx.py* - a collection of scripts to generate a number of mazes using a given algorithm and collect statistics on those mazes
* *xxxxx\_demo.py* - a collection of scripts to demonstrate particular objects, including special kinds of mazes ( for example: polar mazes, sigma mazes, delta mazes, upsilon mazes) or to test features (such as layout programs)

The scripts *entab.py* and *detab.py* are respectively a script to replace spaces by tabs and a script to replace tabs by spaces.  They have nothing to do with mazes.  I use them because the text editor that I use (Gnome's TextEditor) cannot be configured to use spaces for Python and tabs for some other language.  The space/tab configuration is all or nothing.  Nor can it be configured correctly to do entabbing or detabbing.

### 2.1 Recent changes

The list of older changes, going back to 14 July 2020, has been moved to file *CHANGELOG.md*.  A short list of recent changes will continue to appear here before being archived in *CHANGELOG.md*.

#### 4 September 2020

**Complete maze** -- mainly for testing purposes -- this carves a complete maze on a grid, that is a maze with an arc for every grid connection.

**High card wins algorithm** -- A generalization of the Binary Tree algorithm (Buck [1], Chapter 1) and the Ternary (aka Trinary) Tree algorithm (Buck [1], Chapter 12).  This is
implemented in *high\_card\_wins.py*.  The implementation is similar in flavour to the Kruskal's algorithm implementation in *kruskals.py* in that it uses a state matrix (closing issue #9).  The demonstration script *high\_card\_demo.py* contains two demonstrations of the algorithm, the first essentially random, and the other a binary tree instantiation.

**3-dimensional oblong grid** -- A simple rectangular 3-D grid or, more precisely, rectangular parallelopiped lattice.  Cell: *cell3d.py*; grid: *grid3d.py*, simple matplotlib layout: *layout\_plot3d.py*, demo using ternary tree algorithm: *grid3d\_demo.py*.

#### 29 August 2020

**Prim's algorithm and multilevel mazes** -- This change turned out to be easy.  Since Prim's  algorithm already works naturally with weave mazes, no teaking was needed for the Prims.State class. The only thing that was needed was to incorporate the algorithm into a demonstration script.  My choice here was *prims_demo.py*.  I incorporated *argparse* into the script to support command line arguments and added machinery to support multilevel weave mazes.  (I also cleaned up some of the documentation in the script.)

Note: This is stage two of the enhancement issue #5. Still needed: growing tree algorithms applied to multilevel mazes. 

## 3 Algorithms

### 3.1 Maze Generation

In the descriptions, the terms spanning tree and perfect maze are used interchangeably.  They do really mean exactly the same thing.  They only differ in the underlying context.

* *aldous\_broder.py* - implementations of the first-entrance random walk algorithm (Aldous/Broder) and the last-exit random walk algorithm (reverse Aldous/Broder, see [6]) for generating (theoretically) uniformly random spanning trees on a connected simple graph, or equivalently, uniformly random perfect mazes on a connected grid. (The first-entrance algorithm is described in Buck (2015).)  The algorithm tends to start quickly and end slowly, unlike Wilson's algorithm which tends to start slowly and end quickly.
* *binary\_tree.py* - implementation of a simple binary spanning tree algorithm for rectangular mazes.  This is the binary tree algorithm described in Buck (2015).
* *binary\_tree2.py* - implementation of a binary tree algorithm that works most of the time for generating perfect mazes on arbitrary grids.  When it fails, the result is a binary spanning forest. When used on rectangular grids, the result is typically a binary spanning tree which cannot be produced by Jamis Buck's binary tree algorithm.
* *boruvkas.py* - Borůvka's algorithm [8] (and see also [7]) is an algorithm to create minimum-weight spanning trees from connected edge-weighted graphs, provided the weight function is injective.  (If the weight function is not one-to-one, the result is a connected spanning subgraph which could contain circuits. \[*N.B.*: This is either a bug or a feature of the algorithm, depending on one's point of view.\])  Python program *boruvkas.py* is an implementation of Borůvka's algorithm for creating mazes. To insure that weights are unique, the default weight function is a random one-to-one map from the grid edges into range \[1,*e*\], where *e* is the number of grid edges.  As with Kruskal's algorithm, edge costs need to be known a priori, so the algorithm does not create weave mazes in a natural way, but like Kruskal's algorithm, the algorithm can be used to extend forests to spanning trees, and thus it is well-suited to mazes with prewoven crossings.
* *binary\_tree\_polar.py* - an adaptation of the simple binary tree algorithm from Buck (2015) for theta (polar) mazes.
* *edgewise\_growing_tree.py* - a family of algorithms for creating spanning trees (perfect mazes) on edge-weighted connected graphs (grids) that are similar in form to Prim's algorithm.
* *hunt\_and\_kill.py* - an implementation of the Hunt and Kill algorithm described in Chapter 5 of Buck (2015).
* *ellers.py* - an implementation of Eller's algorithm as described in Chapter 12 of the Jamis Buck book [1].  The algorithm is suitable as implemented for rectangular grids using "north" and "east" row and column grid connections.  In *polar_ellers.py*, there is an adaptation of the state matrix that uses the "inward" and "ccw" grid connections -- this variant make the Eller's algorithm implementation work with polar maze.
* *high\_card\_wins.py* - a generalization of the binary tree algorithm described in Chapter 1 of Buck [1].  This also includes the ternary tree algorithm described in Chapter 12 as another special case. (Note: It is called the 'Trinary Tree' algorithm on page 219.)  The basic idea of the algorithm is that players, representing grid directions, go from cell to cell.  At each cell any players who won't create a circuit are dealt a card. The player who has the high card makes the maze connection.  The game continues until the maze is connected.
* *inwinder.py* - an adaptation of the sidewinder algorithm for theta (polar) mazes.
* *kruskals.py* - an implementation of Kruskal's minimum weight spanning tree algorithm tocreate perfect mazes.  The implementation includes some special handling for Preweave mazes to allow for random tunneling and for the creation of long tunnels.  (This implementation closely follows the approaches used in the Jamis Buck book.  See chapters 9 and 10 in [1].)
* *multilevel\_mst.py* - state classes for prewoven multilevel mazes, to be used with Kruskal's algorithm and with Borůvka's algorithm.  (A state class for use with Prim's algorithm should be available in the near future.)
* *prims.py* - an implementation of Prim's minimum weight spanning tree algorithm to create perfect mazes.  This is the algorithm described in the beginning of Chapter 11 of [1], with implementation left as an exercise ("Truest Prim").
* *recursive\_backtracker.py* - the unfortunately misnamed depth-first search algorithm for producing perfect mazes in a connected grid.  The implementation is stack-based to avoid explicit recursion.  (See also: *tree\_search.py*.)
* *recursive\_division.py* - a maze generation algorithm (recursive division) which recursively partitions a grid (in the manner of quicksort) until minimal partitions are obtained. In [1], the algorithm is implemented as a wall adder.  Here it is implemented as a *passage carver* using a State object as in the implementations of Kruskal's algorithm, Prim's algorithm, vertex-Prim's, and Borůvka's algorithm.  The partitions are created in pairs, with a door to connect paired partitions.  Minimal partitions are carved using some other maze algorithm.  The default settings are to create rectangular partitions on a rectangular grid, with minimal partitions being those which are either one cell in width or one cell in height, and to use Sidewinder to carve mazes in the minimal partitions.  The defaults can be reconfigured by creating subclasses of the State object and supplying any necessary methods.  The supplied State classes allow some simple reconfiguration.
* *sidewinder.py* - a modification of Buck's binary spanning tree algorithm which eliminates one bias in that algorithm.  It only works on rectangular grids or (more generally) on grids which can be traversed in two orthogonal directions.  The resulting spanning trees can be binary, but usually are not.
* *vertexwise\_growing\_tree.py* - a family of algorithms for creating spanning trees (perfect mazes) on vertex-weighted connected graphs (grids) that are superficially similar to Prim's algorithm.  These are all built on an algorithm that, for lack of a better name, I call vertex Prim.  These algorithms are similar to the algorithms "Simple Prim" and "True Prim", and two of the growing tree algorithms that were implemented in Chapter 11 of [1].
* *tree\_search.py* -  included are alternative spanning tree search algorithms using a queue (breadth-first search) or a priority-queue (best-first search).  These complement the stack-based depth-first search algorithm used in *recursive\_backtracker.py*.
* *wilson.py* - Wilson's algorithm, a theoretically unbiased spanning tree algorithm that uses a loop-erased random walk of the grid.  In addition, the program includes a hybrid Aldous/Broder/Wilson algorithm that starts the random walk using the first-entrance algorithm of Aldous and Broder and finishes using the loop-erased random walk due to Wilson.  Wilson's algorithm tends to start slowly and end quickly.  The hybrid algorithm tends to start and end quickly, slowing down as it approaches the middle using Aldous/Broder, then speeding up after Wilson's algorithm takes control.  I don't know whether the hybrid algorithm is biased.

### 3.2 Other Algorithms

* *norms.py* - Dijkstra's algorithm for finding distances, shortest path, longest path, *etc.*
* *braiding.py* - simple dead-removal (or braiding) by joining dead ends with random neighbors is supported in the Grid base class (see *grid.py*).  Other braiding algorithms, generally based on exercises in Buck [1] are implemented in *braiding.py*.  Currently implemented are:
  * sparsify - removal by clipping.
  * straightener - removal by carving a passage straight thru the dead end.
  * twister - removal by carving a passage which turns randomly (right or left) at the dead end. Twister can be configured to be restrict turns in a single direction. It can also be specially configured to arrange turnings in grids which don't support normal south/east/north/west directions.

The demonstration script *konigsberg_demo.py* produces a maze based on the Königsberg bridges problem (Leonhard Euler, 1736).  It uses the recursive backtracker algorithm followed by one pass of simple braiding to insure that bridges are passable. Cell removal and cell coloring are governed by a template file *input/königsberg.txt* and sample output is in *demos/königsberg.png*.  For background, see references [2] through [5].

## 4 Grids and cells

The programs *grid.py* and *cell.py* describe the basic grid and cell classes that underly all mazes and the grids that they span.

* *cylinder\_grid* - a modified rectangular grid of square cells in which the east and west edges are identified.
* *masked\_grid.py* - a grid which mirrors part another grid, essentially producing a subgrid.  Actions in the subgrid are mirrored in the parent.
* *moebius\_grid* - a modified rectangular grid of square cells in which the east and west edges are identified with a twist, resulting in a Moebius strip
* *multilevel\_grid.py* - a simple multilevel rectangular grid, with optional weaving.  Levels are connected by stairwells.
* *ortho\_delta\_grid.py* - a grid of right triangular cells arranged in a rectangle
* *ortho\_sigma\_grid.py* - a grid of regular hexagonal cells arranged in an approximate rectangle, much like a beekeeper's honeycomb
* *ortho\_upsilon\_grid.py* - a grid consisting of alternating regular octagonal cells and square cells, arranged in an approximate rectangle
* *polar\_grid.py* - a polar (or theta) grid consisting of concentric circles of cells about the center or pole.  A cell may have an inward neighbor, a clockwise neighbor, a counterclockwise neighbor, and some outward neighbors. The pole may be occupied by a single central cell, or optionally a several pie-shaped wedges forming a circle about the pole.
* *rectangular\_grid.py* - the simple N/S/E/W rectangular grid of square cells
* *weave\_grid.py* - implements two classes:
  + a Weave subclass of Rectangular_Grid which allows for the creation of short tunnels
  + a Preweave subclass of Weave, allowing for preconfigured tunnels and long tunnels. Preconfiguration in the Preweave class is probably not compatible with most of the implemented algorithms.  An exception is Kruskal's algorithm, which has been tailored to work well with the Preweave class.

The function of the various cell programs should be mostly self-explanatory.  Much of the actual work is done in the grid programs and in the layout programs.  ASCII and unicode layout are handled in *rectangular\_grid.py*.

### 5 Layouts

Several types of layouts are supported.  ASCII and unicode layouts are supported on rectangular grids and on some grids derived from rectangular grids (for example, cylinder grids).  All grids support GraphViz/dot layout, though the results usually leave a lot to be desired.

Most derived grids support plot layouts using MatPlotLib, though in most cases, support will require some direct use of MatPlotLib methods.  See the scripts for examples.

## References

1. Buck (2015) - Jamis Buck.   *Mazes for Programmers*.  Pragmatic Bookshelf, 2015.  ISBN-13 978-1-68050-055-4.

2. Leonhard Euler (1736). "Solutio problematis ad geometriam situs pertinentis". *Comment Acad Sci U Petrop* **8**, 128–40.

3. Carl Hierholzer (1873), "Ueber die Möglichkeit, einen Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren", *Mathematische Annalen*, **6** (1): 30–32, doi:10.1007/BF01442866.

4. "Eulerian path". *Wikipedia*, 5 Aug. 2020. Web, accessed 8 Aug. 2020.
[Wikipedia: https://en.wikipedia.org/wiki/Eulerian_path](https://en.wikipedia.org/wiki/Eulerian_path)

5. "Seven bridges of Königsberg". *Wikipedia*, 6 Jun. 2020. Web, accessed 8 Aug. 2020.
[Wikipedia: https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg](https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg)

6. Yiping Hu, Russell Lyons and Pengfei Tang.  "A reverse Aldous/Broder algorithm".  Preprint.  Web: arXiv.org.  24 Jul 2019.
[Arxiv.org: http://arxiv.org/abs/1907.10196v1](http://arxiv.org/abs/1907.10196v1)

7. Bernard Chazelle. "A minimum spanning tree algorithm with inverse-Ackermann type complexity". *J ACM* **47** (2000), 1028-1047.
[Preprint: https://www.cs.princeton.edu/~chazelle/pubs/mst.pdf](https://www.cs.princeton.edu/~chazelle/pubs/mst.pdf)

8. "Borůvka's algorithm". *Wikipedia*. 10 Jun. 2020. Web, accessed 12 Aug. 2020.
[Wikipedia: https://en.wikipedia.org/wiki/Bor%C5%AFvka%27s_algorithm](https://en.wikipedia.org/wiki/Bor%C5%AFvka%27s_algorithm)

 
