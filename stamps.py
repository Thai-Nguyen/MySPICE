'''

'''

import numpy as np
import CircuitStructure as cs

def add_resistor(R, i, j, circuit_struct):
    # Convert to zero-based array indexing
    i -= 1
    j -= 1
    
    if i == -1: # if node i is ground
        circuit_struct.Gmat[(j, j)] = 1/R
    elif j == -1: # if node j is ground
        circuit_struct.Gmat[(i, i)] = 1/R
    else:
        circuit_struct.Gmat[(i, i)] = 1/R
        circuit_struct.Gmat[(j, j)] = 1/R
        circuit_struct.Gmat[(i, j)] = -1/R
        circuit_struct.Gmat[(j, i)] = -1/R
    
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
    
# def stamp_inductor(L, i, j, circuit_struct):

# def stamp_voltage_source(type, val, i, j, Gmat, Cmat, Bvec):
#     if type == 'dc':
#         B

def add_current_source(type, I, i, j, circuit_struct):
    if type  == 'dc':
        if i != 0:
            circuit_struct.Bvec[(i)] = -I
        elif j!= 0:
            circuit_struct.Bvec[(j)] = I
    elif type == 'ac':
        return None
    else:
        print('Source type invalid.')


def test_circuit(circuit_struct):
    add_resistor(1, 1, 2, circuit_struct)
    add_resistor(1, 2, 0, circuit_struct)
    add_capacitor(1, 2, 0, circuit_struct)
    add_current_source('dc', 1, 0, 1, circuit_struct)


if __name__ == '__main__':
    num_elements = 5
    num_inductors = 0
    num_voltage_sources = 0
    
    # Create matrices and vectors
    Gmat = np.zeros((num_elements, num_elements))
    Cmat = np.zeros((num_elements, num_elements))
    Fvec = np.zeros((num_elements, 1))
    Bvec = np.zeros((num_elements, 1))

    # Organize into a data strucute TODO: Maybe use a dictionary?
    circuit_struct = cs.CircuitStructure(Gmat, Cmat, Fvec, Bvec)
    
    # Add components 
    test_circuit(circuit_struct)
    