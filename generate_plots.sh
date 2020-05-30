#!/bin/sh -x

# INSTRUCTIONS:
#####################################################################
# uncomment and edit lines to use make-maze.py to generate examples.
# NOTE:
#     the script will echo commands as they are executed.
#####################################################################

####################################################################
# 1) Query make_maze.py help
#                    (make_maze usage summary)
#    make_maze.py -alg ALGORITHM -dim M N --layout LAYOUTS [--bias BIAS]

./make_maze.py --help

####################################################################
# 2) Create places for examples and test runs

echo "============== 2. Creating Folders..."

      # examples - example plots go into the plot subfolder

mkdir -p examples 
mkdir -p examples/plot
mkdir -p examples/ascii
mkdir -p examples/unicode
mkdir -p examples/graphviz
mkdir -p examples/array

#     test runs - note that test plots go to the demos folder

mkdir -p demos
mkdir -p demos/ascii
mkdir -p demos/unicode
mkdir -p demos/graphviz

####################################################################
# 3) MatPlotLib layout engine
#    these use the 'plot' layout to produce drawings of mazes using
#    matplotlib.
#
#    for more information, see output of make_maze --help
#
#    to repopulate examples, delete examples to be refreshed or use
#    make-maze without the --test option

echo "============== 3(a) Generating Test Plots"

./make_maze.py --alg AB --dim 30 20 --layout plot --test
./make_maze.py --alg ABW --dim 30 20 --layout plot --test
./make_maze.py --alg BT --dim 30 20 --layout plot --test
./make_maze.py --alg BT2 --dim 30 20 --layout plot --test
./make_maze.py --alg DFS --dim 30 20 --layout plot --test
./make_maze.py --alg HK --dim 30 20 --layout plot --test
./make_maze.py --alg NRDFS --dim 30 20 --layout plot --test
./make_maze.py --alg RAB --dim 30 20 --layout plot --test
./make_maze.py --alg SW --dim 30 20 --layout plot --test
./make_maze.py --alg W --dim 30 20 --layout plot --test

#       Here bias is used to create longer horizontal runs.
#       This is akin to using a weighted coin which comes up heads with
#          70% probability.

./make_maze.py --alg BT --dim 30 20 --layout plot --bias 0.7 --test
./make_maze.py --alg SW --dim 30 20 --layout plot --bias 0.7 --test

echo "============== 3(b) Copying Example Plots"

cp -n -v demos/*-plot.png examples/plot

#####################################################################
# 4) Other layouts
#           ASCII, unicode - for small mazes in the terminal
#           graphviz - uses GraphViz/fdp for layout
#    Multiple layout engines are permitted.  All are used.

echo "============== 4(a) Generating Small Test Mazes"

./make_maze.py --alg AB --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg ABW --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg BFS --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg BT --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg BT2 --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg DFS --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg HEAP --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg HK --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg NRDFS --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg RAB --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg SW --dim 5 7 --layout ASCII unicode graphviz --test
./make_maze.py --alg W --dim 5 7 --layout ASCII unicode graphviz --test

./make_maze.py --alg BT --dim 5 7 --layout ASCII unicode graphviz --bias 0.7 --test
./make_maze.py --alg SW --dim 5 7 --layout ASCII unicode graphviz --bias 0.7 --test

echo "============== 4(b) Copying Small Example Mazes"

cp -n -v demos/ascii/*-str.txt examples/ascii
cp -n -v demos/unicode/*-unicode.txt examples/unicode
cp -n -v demos/graphviz/*.gv examples/graphviz
cp -n -v demos/graphviz/*.gv.png examples/graphviz

####################################################################
# 5) MatPlotLib layout engine 2x3 subplot arrays
#   texturizer uses the plot layout

echo "============== 5(a) Generating TexturePlot Arrays"

./texturizer.py --alg AB --dim 20 20
./texturizer.py --alg ABW --dim 20 20
./texturizer.py --alg BFS --dim 20 20
./texturizer.py --alg BT --dim 20 20
./texturizer.py --alg BT2 --dim 20 20
./texturizer.py --alg DFS --dim 20 20
./texturizer.py --alg HEAP --dim 20 20
./texturizer.py --alg HK --dim 20 20
./texturizer.py --alg NRDFS --dim 20 20
./texturizer.py --alg RAB --dim 20 20
./texturizer.py --alg SW --dim 20 20
./texturizer.py --alg W --dim 20 20

./texturizer.py --alg BT --dim 20 20 --bias 0.7
./texturizer.py --alg SW --dim 20 20 --bias 0.7

echo "============== 5(b) Copying TexturePlot Examples"

cp -n -v demos/*-array.png examples/array




