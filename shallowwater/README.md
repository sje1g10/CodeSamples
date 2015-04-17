shallowwater
============

For my thesis, I worked on a collaborative code that is not publicly
available. The code was also quite large; I didn't think it would make
a very good code sample. However, I wanted to make available a simple
code showing the types of methods I used in my thesis code.

The project presented here evolves the shallow water equations for an
initial, dam-break problem. The methods used here are not very
advanced, but it gives a simple overview of how one might go about
evolving a conservation-law system of partial differential equations.


# Instructions

It is possible to run the evolution code and the code to process the
results all in one go using a shell script:

```sh
./run_and_process.sh
```

It may be necessary to first make the shell script executable:

```sh
chmod 755 run_and_process.sh
```

You can also just run the evolution code:

```sh
python run.py
```

Then you can do all of the processing in one go using the following
shell script:

```sh
./process_results.sh
```

Alternatively, you can run the plotting script independently. This
just generates the individual frames of an animation of the results:

```sh
python plot.py
```

Then you'll need to compile the animation LaTeX file, which is best
done using the following commands:

```sh
cd results/
pdflatex results.tex
mv results.pdf ../
cd ../
```

Regardless of method used, you'll need to view the results file using
Adobe Reader in order to see the animation. Alternatively, the output
(.dat) files containing the results of the simulation can be plotted
directly in Gnuplot.

To open Gnuplot:

```sh
gnuplot
```

Then, for example, to plot the height as a function of x for the first
output time step:

```sh
plot 'prim.dat' u 1:2 i 1 w lp
```

More Gnuplot guidance is [here](http://people.duke.edu/~hpgavin/gnuplot.html).

# Modules Used

The code in this project uses the following special Python modules:

```sh
numpy, scipy, matplotlib
```

The code was written and tested using Python 2.7.6.

In order to produce the results.pdf file, you'll need pdflatex installed.