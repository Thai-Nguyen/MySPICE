import scipy as sp

def solver(circuit_struct):
    soln = inv(circuit_struct.Gmat) * circuit_struct.Bvec