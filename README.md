# yaMazeImp
"Yet another maze implementation"
by Eric Conrad.

## Overview

* 1 **Description**
* 2 **Scripts**
* 2.1 **Change log**
* 3 **Algorithms**
* 3.1 **Maze generation**
* 3.2 **Other algorithms**
* 4 **Grids and cells**
* 5 **Layouts**

## 1 Description

This is a collection of maze algorithms and scripts that were implemented primarily in *Python* 3.  Most of these programs are based on suggestions and ideas found in an wonderful little book by Jamis Buck called *Mazes for Programmers*.  See the references at the end for more information.  (My recommendation: buy this book.  In addition to learning about mazes, you will pick up some graph theory and *ruby* language programming.)  I've made some departures from Buck's approaches, so my programs are not simply translations from *ruby* into *python*.

## 2 Scripts

* *make_maze.py* - a script to create rectangular mazes using standard algorithms
* *texturizer.py* - a script to create texture matrices using standard algorithms
* *eval_xxxxx.py* - a collection of scripts to generate a number of mazes using a given algorithm and collect statistics on those mazes
* *xxxxx_demo.py* - a collection of scripts to demonstrate particular objects, including special kinds of mazes ( for example: polar mazes, sigma mazes, delta mazes, upsilon mazes) or to test features (such as layout programs)

The scripts *entab.py* and *detab.py* are respectively a script to replace spaces by tabs and a script to replace tabs by spaces.  They have nothing to do with mazes.  I use them because the text editor that I use (Gnome's TextEditor) cannot be configured to use spaces for Python and tabs for some other language.  The space/tab configuration is all or nothing.  Nor can it be configured correctly to do entabbing or detabbing.

### 2.1 Change log

#### 1 August 2020

**Weave mazes** -- *weave_cell.py* and *weave_grid.py* add classes of cells and grids to support rectangular weave mazes.  Depth-first search, hunt and kill, and the first-entry Aldous/Broder algorithm all work nicely to generate rectangular mazes with weaves.  The layout routines *layout_plot.py* and *layout_plot_color* produce nice plots.  See also *weave_demo.py*.

**Braiding** -- several programs were added to support dead-end removal (aka braiding). Simple braiding by linking is supported in *grid.py*.  Alternative braiding algorithms are implemented in *braiding.py*.  See also *braid_demo.py*, *sparsify_demo.py*, *straightening_demo.py* and *twisting_demo.py*.

**Kruskal's algorithm** -- Kruskal's maze generation algorithm was implemented, closely following the ruby implementation in the Jamis Buck book.  The algorithm does not itself produce weaves, but works well with randomly preconfigured weaves. See *kruskals.py* and *kruskals_demo.py* for more information.

The *demos* folder has several *png* plots produced by the added demonstration programs.  Documentation of these additions still needs to be added below in this README file.

#### 27 July 2020 ####

**Inset Mazes** -- When using *matplotlib* to plot rectangular mazes, the Layout and Color_Layout classes now handle insets.  Method *draw_grid* in *layout_plot.py* directs cells with insets to new method *draw_inset_cell* which has been added to *layout_plot.py* (for walls and passages) and *layout_plot_color.py* (for filling the interior of a cell).  A demonstration program *inset_demo.py* produces a test plot.

#### 26 July 2020

**Braid Mazes** -- Braiding or dead end removal is one way of transforming mazes.  The Grid class handles braiding using two new methods in *grid.py*.  A demonstration script (*braid_demo.py*) shows how with two exxamples.  The result (*demos/braid-arry.png*) is in the *demos* directory.

#### 25 July 2020

**Theta Mazes** -- Minor tweaking of code, some in reponse to pylint3 warnings  Also, descriptive titles were added to the demos.  In addition, I've added a version of the basic E-N binary tree algorithm for theta mazes.  This one proceeds through a theta (polar) grid in a CCW-inward manner.  As in inwinder (the theta version of sidewinder), each latitude requires a hard counterclockwise boundary.  See *binary_tree_polar.py* and *polar_binary_demo.py* for details.  Also, four demos will be updated with titles and two (for the polar binary trees) will be added in short order.

#### 14 July 2020 (Bastille Day)

**Theta Mazes** -- Added the script *polar_demo.py* to create polar mazes (also known as theta mazes).  The associated python programs are *polar_cell.py* (to manage cells), *polar_grid.py* (to manage the associated grids), and *layout_plot_polar.py* (to handle displaying the maze using *matplotlib*).

The layout displays cells as polygons instead of circular bars because the managing circular bars would require using superimposed axes, specifically polar coordinates for flood-filling the circular bars and rectangular coordinates for drawing boundary arcs. Jamis Buck uses essentially the same polygon scheme with his *ruby* *chunky_png* layout of theta mazes.  Two kinds of mazes can be produced -- one kind having a single cell at the pole, and the other with several wedge cells that all circle about the pole.  A cell's neighbors are inward, clockwise, counterclockwise, and outward.  A cell may have more than one outward neighbor.

Two demonstration files were added in the *demos* directory: *demos/polar1.png* and *demos/polar2.png*.  These were produced by running *polar_demo.py*. They are the results of applying the first-entry Aldous-Broder algorithm to both kinds of polar grid.

## 3 Algorithms

### 3.1 Maze Generation

In the descriptions, the terms spanning tree and perfect maze are used interchangeably.  They do really mean exactly the same thing.  They only differ in the underlying context.

* *aldous_broder.py* - implementations of the first-entrance random walk algorithm (Aldous/Broder) and the last-exit random walk algorithm (reverse Aldous/Broder) for generating (theoretically) uniformly random spanning trees on a connected simple graph, or equivalently, uniformly random perfect mazes on a connected grid. (The first-entrance algorithm is described in Buck (2015).)  The algorithm tends to start quickly and end slowly, unlike Wilson's algorithm which tends to start slowly and end quickly.
* *binary_tree.py* - implementation of a simple binary spanning tree algorithm for rectangular mazes.  This is the binary tree algorithm described in Buck (2015).
* *binary_tree2.py* - implementation of a binary tree algorithm that works most of the time for generating perfect mazes on arbitrary grids.  When it fails, the result is a binary spanning forest. When used on rectangular grids, the result is typically a binary spanning tree which cannot be produced by Jamis Buck's binary tree algorithm.
* *binary_tree_polar.py* - and adaptation of the simple binary tree algorithm from Buck (2015) for theta (polar) mazes. 
* *hunt_and_kill.py* - an implementation of the Hunt and Kill algorithm described in Chapter 5 of Buck (2015).
* *inwinder.py* - an adaptation of the sidewinder algorithm for theta (polar) mazes.
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
* *polar_grid.py* - a polar (or theta) grid consisting of concentric circles of cells about the center or pole.  A cell may have an inward neighbor, a clockwise neighbor, a counterclockwise neighbor, and some outward neighbors. The pole may be occupied by a single central cell, or optionally a several pie-shaped wedges forming a circle about the pole.
* *rectangular_grid.py* - the simple N/S/E/W rectangular grid of square cells

The function of the various cell programs should be mostly self-explanatory.  Much of the actual work is done in the grid programs and in the layout programs.  ASCII and unicode layout are handled in *rectangular_grid.py*.

### 5 Layouts

Four types of layouts are supported.  ASCII and unicode layouts are supported on rectangular grids and on grids derived from rectangular grids (for example, cylinder grids).  All grids support GraphViz/dot layout, though the results usually leave a lot to be desired.

Most derived grids support plot layouts using MatPlotLib, though in most cases, support will require some direct use of MatPlotLib methods.  See the scripts for examples.

## References

1. Buck (2015) - Jamis Buck.   *Mazes for Programmers*.  Pragmatic Bookshelf, 2015.  ISBN-13 978-1-68050-055-4.



