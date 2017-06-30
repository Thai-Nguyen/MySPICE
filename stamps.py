'''

'''

import numpy as np
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
    # Create pointers for ease in reading
    Cmat = circuit_struct.Cmat
    Gmat = circuit_struct.Gmat
    Fvec = circuit_struct.Fvec
    Bvec = circuit_struct.Bvec

    # Add another row and column to G,C. Add another row for F and B.
    nrows, ncols = Cmat.shape
    empty_row = np.zeros((1, ncols), dtype='complex128')
    empty_col = np.zeros((nrows + 1, 1), dtype='complex128')

    Cmat = np.vstack((Cmat, empty_row))
    Cmat = np.hstack((Cmat, empty_col))
    Gmat = np.vstack((Gmat, empty_row))
    Gmat = np.hstack((Gmat, empty_col))
    Fvec = np.vstack((Fvec, 0))
    Bvec = np.vstack((Bvec, 0))

    # Convert to zero-based array indexing
    i -= 1
    j -= 1
    n = Gmat.shape[0] - 1
    if i == -1:  # if node i is ground
        Gmat[(n, j)] = -1
        Gmat[((j, n))] = -1
    elif j == -1:  # if node j is ground
        Gmat[(n, i)] = 1
        Gmat[(i, n)] = 1
    else:
        Gmat[(n, j)] = -1
        Gmat[(j, n)] = -1
        Gmat[(n, i)] = 1
        Gmat[(i, n)] = 1
    Cmat[(n, n)] = -L

    circuit_struct.Cmat = Cmat
    circuit_struct.Gmat = Gmat
    circuit_struct.Fvec = Fvec
    circuit_struct.Bvec = Bvec


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
    total_num_elements = num_elements + num_inductors + num_voltage_sources

    # Create matrices and vectors
    Gmat = np.zeros((num_elements, num_elements), dtype='complex128')
    Cmat = np.zeros((num_elements, num_elements), dtype='complex128')
    Fvec = np.zeros((num_elements, 1), dtype='complex128')
    Bvec = np.zeros((num_elements, 1), dtype='complex128')

    # Organize into a data structure
    circuit_struct = cs.CircuitStructure(Gmat, Cmat, Fvec, Bvec)

    # Add components 
    test_circuit(circuit_struct)

    # TODO: Convert circuit information to CSR for fast sparse matrix arithmetic
