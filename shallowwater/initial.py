import numpy as np
import scipy as sc
from variables import *
from evolve import *

def setInitialValues(initial_data, xmin, xmax, dx):

    initial_type = select_input(initial_data)

    inds = np.arange(-GZ, NPX+GZ, 1)
    x = xmin + dx * (inds + 0.5)
    prim  = np.zeros((NPRIM, len(x)))

    for i in range(len(x)):
        
        prim[:, i] = initial_type(prim[:, i], x[i])

    cons = prim2cons(prim)
    auxl = prim2auxl(prim)

    return x, prim, cons, auxl

def dam_break(prim, x):

    if (x < 0.0):
        prim[H] = 10.0
    else:
        prim[H] = 0.2
        
    prim[V_X] = 0.0        
    prim[V_Y] = 0.0        

    return prim

def wave(prim, x):
    
    xcenter = 0.0
    width   = 0.1

    prim[H]   = 0.1 * np.exp(-(x-xcenter)**2 / (2.0 * width**2)) + 10.0
    prim[V_X] = 0.0
    prim[V_Y] = 0.0

    return prim

def select_input(initial_data):

    # map strings to functions that give initial data
    input_mapping = {
        'dam_break' : dam_break,
        'wave'      : wave,
    }

    try:
        return input_mapping[initial_data]
    except KeyError:
        print 'Unrecognized initial data type:', initial_data
