import numpy as np
import scipy as sc
from initial import *
from variables import *
from evolve import *
from output import *

def main():

    n = 0
    t = 0.0
    t_last_out = 0.0

    x, prim, cons, auxl, bed, d_bed = setInitialValues('shore', XMIN, XMAX, DX)
    output_files(t, x, prim, cons, auxl, adding=False)
    rhs, info = calcRHS(prim, DX)
    output_info(t, x, info, adding=False)

    while t < TFINAL:
        # Assign dt from maximum characteristic speed
        lam = calcMaxLam(prim, bed)
        dt = RC * DX / lam

        # Make sure output timesteps are as specified
        if (t + dt > t_last_out + TOUT):
            dt = t_last_out + TOUT - t

        prim, cons, auxl, info = evolve(prim, DX, dt, bed, d_bed)

        n = n + 1
        t = t + dt

        if t >= t_last_out + TOUT:
            t_last_out = t
            output_files(t, x, prim, cons, auxl)
            output_info(t, x, info)
            print "Step: %05i, Time: %.10f" %(n, t)

if __name__ == "__main__":
    main()
