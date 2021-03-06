
# Primitive Variables
NPRIM = 3
H   = 0
V_X = 1
V_Y = 2

# Conserved Variables
HV_X = 1
HV_Y = 2

# Auxiliary Variables
NAUXL = 1
HH   = 0

# Other Parameters
GRAVITY = 9.8

FILENAME = 'results.dat'
BOUNDARY_TYPE = 'freeze'

XMIN = -1.0
XMAX = 1.0
#LAM = 100.0          # Just guess the maximum characteristic speed
RC = 0.5             # Relative courant should be less than one for stability
#COURANT = RC / LAM   # Set the ratio between dx and dt

GZ = 2
NPX = 1000

# Edges of grid including ghost zones
GS = 0
GE = NPX + 2*GZ
# Edges of real grid (exluding ghost zones)
RS = GZ
RE = NPX + GZ

DX = (XMAX - XMIN) / NPX

TFINAL = 0.16
TOUT = 0.005 
