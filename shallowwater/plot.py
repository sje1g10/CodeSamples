import matplotlib
import numpy as np
import matplotlib.pyplot as plot
from matplotlib import rc
from variables import *

def myplot(filename, ind, data):

    plotfile = filename + "plot/plot%03d.pdf" % ind
    fig = plot.figure(facecolor='white')
    plot.subplots_adjust(hspace=0.001, wspace=0.30, top=0.98, 
                         bottom=0.08,  right=0.97,  left=0.07)
    
# X is in data, so positions are shifted 1 from prim indices
    ax1 = plot.subplot(211)
    ax1.plot(data[0,:],data[H+1,:],'kx',linewidth=2)
    ax1.axis((-1.0, 1.0, -0.5, 10.5))
    plot.setp(ax1.get_xticklabels(), visible=False) # no x ticks for top plot
    ax1.set_ylabel(r'$h$')

    ax2 = plot.subplot(212)
    ax2.plot(data[0,:],data[V_X+1,:],'kx',linewidth=2)
    ax2.axis((-1.0, 1.0, -1.0, 11.5))
    ax2.set_ylabel(r'$v_x$')
    ax2.set_xlabel(r'$x$')
    
    plot.savefig(plotfile, format='pdf')

    ax1.clear()
    ax2.clear()
    fig.clear()
    plot.close("all")

def readfile(filename, ind):

    raw_data = np.loadtxt(filename)

    data = np.zeros((NPRIM+1, NPX))

    # loadtxt imports all times (indices) in the file as one long array
    # We need to find the data that goes with the index we want
    for k in range(NPRIM + 1):
        data[k, :] = raw_data[(NPX + 2*GZ)*ind + GZ : 
                              (NPX + 2*GZ)*(ind + 1) - GZ, k]

    return data

def main():

    outfile = ''

    n = int(TFINAL / TOUT) + 1
    for i in range(n):
        print "Loading index: ", i, "/", n
        data = readfile(FILENAME, i)
        print "Plotting..."
        myplot(outfile, i, data)
        print "Done with index: ", i, "/", n

if __name__ == "__main__":
    main()

