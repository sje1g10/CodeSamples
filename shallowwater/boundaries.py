from variables import *

def boundaries(prim):
    boundary_function = select_boundaries(BOUNDARY_TYPE)
    return boundary_function(prim)

def copy(prim):
    for i in range(GZ):
        prim[:, RS-1-i] = prim[:, RS+i]
        prim[:, RE+i]   = prim[:, RE-1-i]
    return prim

def freeze(prim):
    return prim

def select_boundaries(boundary_type):

    # map strings to functions that give initial data
    boundary_mapping = {
        'copy'   : copy,
        'freeze' : freeze,
    }

    try:
        return boundary_mapping[boundary_type]
    except KeyError:
        print 'Unrecognized boundary type:', boundary_type
