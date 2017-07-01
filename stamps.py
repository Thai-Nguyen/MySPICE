'''

'''

import numpy as np
import scipy as sp
from scipy import sparse
import CircuitStructure as cs


def add_resistor(R, i, j, circuit_struct):
    # Convert to zero-based array indexing
    i -= 1
    j -= 1

    if i == -1:  # if node i is ground
        circuit_struct.Gmat[(j, j)] = 1 / R
    elif j == -1:  # if node j is ground
        circuit_struct.Gmat[(i, i)] = 1 / R
    else:
        circuit_struct.Gmat[(i, i)] = 1 / R
        circuit_struct.Gmat[(j, j)] = 1 / R
        circuit_struct.Gmat[(i, j)] = -1 / R
        circuit_struct.Gmat[(j, i)] = -1 / R


def add_capacitor(C, i, j, circuit_struct):
    # Convert to zero-based array indexing
    i -= 1
    j -= 1

    if i == -1:  # if node i is ground
        circuit_struct.Cmat[(j, j)] = C
    elif j == -1:  # if node j is ground
        circuit_struct.Cmat[(i, i)] = C
    else:
        circuit_struct.Cmat[(i, i)] = C
        circuit_struct.Cmat[(j, j)] = C
        circuit_struct.Cmat[(i, j)] = -C
        circuit_struct.Cmat[(j, i)] = -C


def add_inductor(L, i, j, circuit_struct):
    # Add another row and column to G,C. Add another row for F and B.
    nrows, ncols = circuit_struct.Cmat.shape
    empty_row = np.zeros((1, ncols), dtype='complex128')
    empty_col = np.zeros((nrows + 1, 1), dtype='complex128')

    circuit_struct.Gmat = sp.sparse.vstack([circuit_struct.Gmat, empty_row])
    circuit_struct.Gmat = sp.sparse.hstack([circuit_struct.Gmat, empty_col])
    circuit_struct.Cmat = sp.sparse.vstack([circuit_struct.Cmat, empty_row])
    circuit_struct.Cmat = sp.sparse.hstack([circuit_struct.Cmat, empty_col])
    circuit_struct.Fvec = np.vstack((circuit_struct.Fvec, 0))
    circuit_struct.Bvec = np.vstack((circuit_struct.Bvec, 0))

    # Gmat and Cmat became COO sparse matrices. Convert back to LIL format for ease in data entry
    circuit_struct.Gmat = circuit_struct.Gmat.tolil()
    circuit_struct.Cmat = circuit_struct.Cmat.tolil()

    # Convert to zero-based array indexing
    i -= 1
    j -= 1
    n = circuit_struct.Gmat.shape[0] - 1  # index of last row/col of Gmat and Cmat
    if i == -1:  # if node i is ground
        circuit_struct.Gmat[(n, j)] = -1
        circuit_struct.Gmat[(j, n)] = -1
    elif j == -1:  # if node j is ground
        circuit_struct.Gmat[(n, i)] = 1
        circuit_struct.Gmat[(i, n)] = 1
    else:
        circuit_struct.Gmat[(n, j)] = -1
        circuit_struct.Gmat[(j, n)] = -1
        circuit_struct.Gmat[(n, i)] = 1
        circuit_struct.Gmat[(i, n)] = 1
    circuit_struct.Cmat[(n, n)] = -L


# TODO: Add independent voltage source

def add_current_source(type, I, i, j, circuit_struct):
    if type == 'dc':
        if i != 0:
            circuit_struct.Bvec[i] = -I
        elif j != 0:
            circuit_struct.Bvec[j] = I
    elif type == 'ac':
        print('Source type not yet implemented.')
    else:  # TODO: Throw an exception instead
        print('Source type invalid.')


def test_circuit(circuit_struct):
    add_resistor(1, 1, 2, circuit_struct)
    add_resistor(1, 2, 0, circuit_struct)
    add_capacitor(1, 2, 0, circuit_struct)
    add_inductor(1, 2, 0, circuit_struct)
    add_current_source('dc', 1, 0, 1, circuit_struct)


if __name__ == '__main__':
    num_elements = 5
    num_inductors = 0
    num_voltage_sources = 0

    # Create matrices and vectors
    Gmat = sp.sparse.lil_matrix((num_elements, num_elements), dtype='complex128')
    Cmat = sp.sparse.lil_matrix((num_elements, num_elements), dtype='complex128')
    Fvec = np.zeros((num_elements, 1), dtype='complex128')
    Bvec = np.zeros((num_elements, 1), dtype='complex128')

    # Organize into a data structure
    circuit_struct = cs.CircuitStructure(Gmat, Cmat, Fvec, Bvec)

    # Add components 
    test_circuit(circuit_struct)

    # TODO: Convert circuit information to CSR for fast sparse matrix arithmetic
