# Change Log

Recent changes are found in file *README.md*.  This file contains a list of older changes going back to 14 July 2020.  This list is in reverse chronological order.

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


