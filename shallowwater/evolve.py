import numpy as np
from variables import *
from output import *
from boundaries import *

def evolve(prim, dx, dt):

    rhs, info = calcRHS(prim, dx)

    cons = prim2cons(prim)
    cons = update(cons, rhs, dt)

    prim = cons2prim(cons)
    prim = boundaries(prim)

# For analysis only
    auxl = prim2auxl(prim)

# For info/debug purposes
    rhs, info = calcRHS(prim, dx)
    return prim, cons, auxl, info

def calcRHS(prim, dx):
    rhs = np.zeros((NPRIM, NPX+2*GZ))
    
    prim_l, prim_r = reconstruct(prim)
    
    # Get conserved variables and fluxes from reconstructed primitive variables
    cons_l = prim2cons(prim_l)
    cons_r = prim2cons(prim_r)

    flux_l = calcFlux(prim_l)
    flux_r = calcFlux(prim_r)

    lam = calcMaxLam(prim)

    # Estimate flux at cell boundary using HLL approximate Riemann solver
    flux = HLL(cons_l, cons_r, flux_l, flux_r, lam)

    # In flux, index > i-1/2
    #  RHS = -0.5/dx * (flux_{i+1/2} - flux_{i-1/2})
    rhs[:, RS:RE] = -1/(2.0*dx) * (flux[:, RS+1:RE+1] - flux[:, RS:RE])

    return rhs, (prim_l, prim_r, cons_l, cons_r, flux_l, flux_r, flux)

def reconstruct(prim):
    prim_l = np.zeros((NPRIM, NPX+2*GZ))
    prim_r = np.zeros((NPRIM, NPX+2*GZ))
    
    slope = np.zeros((NPRIM, NPX+2*GZ))
    
    # Apply slope-limiter
    for i in range(GS+1, GE-1):
        for k in range(NPRIM):
            # new index > slope for cell i (comparing i-1/2 and i+1/2 using a
            #  a slope limiter)
            slope[k, i] = minmod(prim[k, i] - prim[k, i-1],
                                 prim[k, i+1] - prim[k, i])
            # prim_l is to the left edge of cell i (at i-1/2)
            prim_l[k, i] = prim[k, i] - 0.5*slope[k, i]
            # prim_r is to the right edge of cell i (at i+1/2)
            prim_r[k, i+1] = prim[k, i] + 0.5*slope[k, i]
            # In prim_l and prim_r, the index > i-1/2: we assign as above
            #  so that prim_l[:, i] and prim_r[:, i] refer to the same cell edge

    return prim_l, prim_r

def minmod(a, b):
    if (a * b <= 0.0):
        return 0.0
    elif (abs(a) < abs(b)):
        return a
    else:
        return b

def HLL(cons_l, cons_r, flux_l, flux_r, lam):
    return (flux_r + flux_l + lam * (cons_r - cons_l)) / 2.0

# Simple forward-in-time differencing seems to produce relatively sharp results
def update(cons, rhs, dt):
    
    # Only update real cells
    cons[:, RS:RE] = cons[:, RS:RE] + rhs[:, RS:RE] * dt

    return cons

def calcFlux(prim):
    flux = np.zeros((NPRIM, NPX+2*GZ))

# In 1D, we only look at the flux in the x-direction
    flux[H, :] = prim[H, :] * prim[V_X, :]
    flux[HV_X, :] = (prim[H, :] * prim[V_X, :]**2 + 
                     0.5 * GRAVITY * prim[H, :]**2)
    flux[HV_Y, :] = prim[H, :] * prim[V_X, :] * prim[V_Y, :]

    return flux

def prim2cons(prim):
    cons = np.zeros((NPRIM, NPX+2*GZ))
    
    cons[H, :] = prim[H, :]
    cons[HV_X, :] = prim[H, :] * prim[V_X, :]
    cons[HV_Y, :] = prim[H, :] * prim[V_Y, :]

    return cons

def cons2prim(cons):
    prim = np.zeros((NPRIM, NPX+2*GZ))

    prim[H, :] = cons[H, :]
    prim[V_X, :] = cons[HV_X, :] / prim[H, :]
    prim[V_Y, :] = cons[HV_Y, :] / prim[H, :]
    
    return prim

def prim2auxl(prim):
    auxl = np.zeros((NAUXL, NPX+2*GZ))
    
    auxl[HH,   :] = prim[H, :]

    return auxl

def calcMaxLam(prim):

    cs = np.sqrt(GRAVITY * prim[H, :])
    lam1 = np.amax(abs(prim[V_X, :] + cs))    
    lam2 = np.amax(abs(prim[V_X, :] - cs))
    return max(lam1, lam2)
