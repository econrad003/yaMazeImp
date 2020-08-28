# Change Log

Recent changes are found in file *README.md*.  This file contains a list of older changes going back to 14 July 2020.  This list is in reverse chronological order.

#### 14 August 2020

**Prim's algorithm** -- Python modules *prims.py* contains an implementation of Prim's algorithm for generating a minimum weight spanning tree from an edge-weighted graph.  (This is the "Truest Prim" algorithm described in the beginning of Chapter 11 of [1], not the similar maze-generation algorithm misleadingly named "True Prim" which uses vertex weights instead of edge weights.) The script *prims\_demo.py* provides a demonstration.

**growing tree algorithms** -- Several algorithms related to Prim's algorithm are collected in the Python modules *edgewise\_growing\_tree.py* and *vertexwise\_growing\_tree.py*.

The edgewise growing tree modules build on the Prims.State class in *prims.py* in order to produce different kinds of spanning trees (i.e. perfect mazes) on connected grids (i.e. connected graphs).  The implemented examples (suggested by exercises in Chapter 11 of [1]) are illustrated in the demonstration script *edge\_growing\_demo.py*.  For comparison purposes, the maze array also includes mazes produced using Prim's algorithm and Kruskal's algorithm.

Module *vertexwise\_growing\_tree.py* contains vertexwise growing tree classes starting with class Vertex\_Prims, my version of algorithm "True Prim" as described and implemented in Chapter 11 of[1].  Nested class Vertex\_Prims.State maintains the algorithms state using a priority queue.  Several subclasses of Vertex\_Prims.State are included as examples of variants.  (The included variations either change the cost function or change the queue discipline.)  Script *vertex\_growing\_demo.py* demonstrates the implemented vertexwise growing tree algorithms.  Prim's algorithm ("Truest Prim" in [1]) is included in the maze output array for purposes of comparison.

**Borůvka's algorithm** -- *boruvkas.py* is an implementation of Borůvka's algorithm to create minimum spanning tree mazes. A demonstration script *boruvkas\_demo.py* outputs a maze.

**recursive division** -- implemented in the Jamis Buck book [1] as a wall adder, it is implemented here (in *recursive\_division.py*) as a passage carver, using a State object in the manner of the implementation of Kruskal's algorithm.  Some subclasses of the recursive division State object are included to illustrate some variations of the algorithm.  The primary demonstration script (*recursive\_division\_demo.py*) gives four examples.  A secondary script (*recursive\_division\_demo5.py*) gives a fifth example and also illustrates calling of the primary script from another script.

**minor bug fixes** including typographical errors, documentation oversights, and markdown issues.

**change log** -- A list of older changes, previously included at the end of *README.md*, has been moved to *CHANGELOG.md*.  A short list of recent changes will continue to remain in *README.md*.

#### 8 August 2020

**Königsberg maze** -- a maze based on Leonhard Euler's Königsberg bridges problem.  The maze uses a template, *input/königsberg.txt* and classes in *weave\_grid.py* and *template\_grid.py*.  The maze is produced using depth-first search on a subgrid of a large rectangular grid.  One pass of simple braiding is done to insure that the bridges are passable.  Coloring and cell-removal is based on the template file.  See *konigsberg\_demo.py* (with no umlaut to insure that the source file name is easily typed) for details.  References [2], [3], [4] and [5] (see README.md) contain details about Euler's problem and its principal generalization.

**long tunnels** -- The Preweave class in *weave.py* can create long tunnels, completing an exercise in Chapter 10 of Buck [1].  These can be preconfigured in a Kruskals.State object (see *kruskals.py*).

**templates for rectangular grids** -- templating to bias maze texture by grid surgery is supported in *grid\_template.py*.  In addition to local surgery (removing specific cells or grid edges), some global surgery can be performed.  Global surgery (for the Rectangular Grid class) includes erecting hard walls (with or without doors), creating hard spirals, or, using recursive division with some restrictions, by partitioning the grid into hard rooms.  See the script *template\_demo.py* for examples.

**minor bug fixes** -- *layout\_plot.py*, *weave\_grid.py*

## 1 August 2020

* **Weave mazes** -- *weave\_cell.py* and *weave\_grid.py* add classes of cells and grids to support rectangular weave mazes.  Depth-first search, hunt and kill, and the first-entry Aldous/Broder algorithm all work nicely to generate rectangular mazes with weaves.  The layout routines *layout\_plot.py* and *layout\_plot_color* produce nice plots.  See also *weave\_demo.py*.

* **Braiding** -- several programs were added to support dead-end removal (aka braiding). Simple braiding by linking is supported in *grid.py*.  Alternative braiding algorithms are implemented in *braiding.py*.  See also *braid\_demo.py*, *sparsify\_demo.py*, *straightening\_demo.py* and *twisting\_demo.py*.

* **Kruskal's algorithm** -- Kruskal's maze generation algorithm was implemented, closely following the ruby implementation in the Jamis Buck book.  The algorithm does not itself produce weaves, but works well with randomly preconfigured weaves. See *kruskals.py* and *kruskals\_demo.py* for more information.

The *demos* folder has several *png* plots produced by the added demonstration programs.  Documentation of these additions still needs to be added to this README file.

## 27 July 2020

* **Inset Mazes** -- When using *matplotlib* to plot rectangular mazes, the Layout and Color\_Layout classes now handle insets.  Method *draw\_grid* in *layout\_plot.py* directs cells with insets to new method *draw\_inset\_cell* which has been added to *layout\_plot.py* (for walls and passages) and *layout\_plot_color.py* (for filling the interior of a cell).  A demonstration program *inset\_demo.py* produces a test plot.

## 26 July 2020

* **Braid Mazes** -- Braiding or dead end removal is one way of transforming mazes.  The Grid class handles braiding using two new methods in *grid.py*.  A demonstration script (*braid\_demo.py*) shows how with two exxamples.  The result (*demos/braid-array.png*) is in the *demos* directory.

## 25 July 2020

* **Theta Mazes** -- Minor tweaking of code, some in reponse to pylint3 warnings  Also, descriptive titles were added to the demos.  In addition, I've added a version of the basic E-N binary tree algorithm for theta mazes.  This one proceeds through a theta (polar) grid in a CCW-inward manner.  As in inwinder (the theta version of sidewinder), each latitude requires a hard counterclockwise boundary.  See *binary\_tree\_polar.py* and *polar\_binary\_demo.py* for details.  Also, four demos will be updated with titles and two (for the polar binary trees) will be added in short order.

## 14 July 2020 (Bastille Day)

* **Theta Mazes** -- Added the script *polar\_demo.py* to create polar mazes (also known as theta mazes).  The associated python programs are *polar\_cell.py* (to manage cells), *polar\_grid.py* (to manage the associated grids), and *layout\_plot\_polar.py* (to handle displaying the maze using *matplotlib*).

> The layout displays cells as polygons instead of circular bars because the managing circular bars would require using superimposed axes, specifically polar coordinates for flood-filling the circular bars and rectangular coordinates for drawing boundary arcs. Jamis Buck uses essentially the same polygon scheme with his *ruby* *chunky\_png* layout of theta mazes.  Two kinds of mazes can be produced -- one kind having a single cell at the pole, and the other with several wedge cells that all circle about the pole.  A cell's neighbors are inward, clockwise, counterclockwise, and outward.  A cell may have more than one outward neighbor.

> Two demonstration files were added in the *demos* directory: *demos/polar1.png* and *demos/polar2.png*.  These were produced by running *polar\_demo.py*. They are the results of applying the first-entry Aldous-Broder algorithm to both kinds of polar grid.


