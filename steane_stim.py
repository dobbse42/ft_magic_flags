import stim


''' Instantiate a $\bra{0_L}$ state in Steane's code:
IIIXXXX
IXXIIXX
XIXIXIX
IIIZZZZ
IZZIIZZ
ZIZIZIZ
'''
def create_steane_0(circuit):
  circuit.append("MPP", [stim.target_x(3), stim.target_combiner(), stim.target_x(4), stim.target_combiner(), stim.target_x(5), stim.target_combiner(), stim.target_x(6)])
  circuit.append("MPP", [stim.target_x(1), stim.target_combiner(), stim.target_x(2), stim.target_combiner(), stim.target_x(5), stim.target_combiner(), stim.target_x(6)])
  circuit.append("MPP", [stim.target_x(0), stim.target_combiner(), stim.target_x(2), stim.target_combiner(), stim.target_x(4), stim.target_combiner(), stim.target_x(6)])
  circuit.append("MPP", [stim.target_z(3), stim.target_combiner(), stim.target_z(4), stim.target_combiner(), stim.target_z(5), stim.target_combiner(), stim.target_z(6)])
  circuit.append("MPP", [stim.target_z(1), stim.target_combiner(), stim.target_z(2), stim.target_combiner(), stim.target_z(5), stim.target_combiner(), stim.target_z(6)])
  circuit.append("MPP", [stim.target_z(0), stim.target_combiner(), stim.target_z(2), stim.target_combiner(), stim.target_z(4), stim.target_combiner(), stim.target_z(6)])

  return

''' Assumes qubits is a list of 7 qubit indices which, when taken in order, represent the 7 physical qubits for a logical qubit encoded with the Stean code. Ancilla qubits should be a list of 3 qubits initialized to the $\bra{0}$ state.
Note: may require that we can initialize to $\bra{+}$ without noise?
'''
def stab_extract_ft_flag(circuit, data_qubits, ancilla_qubits):
  # Initialize the first data qubit to $\bra{+}$.
  circuit.append("H", ancilla_qubits[0])

  # First half
  circuit.append("CNOT", [ancilla_qubits[0], data_qubits[4]])
  circuit.append("CNOT", [data_qubits[6], ancilla_qubits[1]])
  circuit.append("CNOT", [data_qubits[5], ancilla_qubits[2]])
  circuit.append("TICK")
  
  circuit.append("CNOT", [ancilla_qubits[0], ancilla_qubits[2]])
  circuit.append("TICK")
  
  circuit.append("CNOT", [ancilla_qubits[0], data_qubits[0]])
  circuit.append("CNOT", [data_qubits[4], ancilla_qubits[1]])
  circuit.append("CNOT", [data_qubits[1], ancilla_qubits[2]])
  circuit.append("TICK")

  circuit.append("CNOT", [ancilla_qubits[0], data_qubits[2]])
  circuit.append("CNOT", [data_qubits[3], ancilla_qubits[1]])
  circuit.append("CNOT", [data_qubits[6], ancilla_qubits[2]])
  circuit.append("TICK")

  circuit.append("CNOT", [ancilla_qubits[0], ancilla_qubits[1]])
  circuit.append("TICK")

  circuit.append("CNOT", [ancilla_qubits[0], data_qubits[6]])
  circuit.append("CNOT", [data_qubits[5], ancilla_qubits[1]])
  circuit.append("CNOT", [data_qubits[2], ancilla_qubits[2]])
  circuit.append("TICK") # Maybe extraneous TICK?

  # Measure and reset ancilla (do I actually need to reset?)
  circuit.append("MX", ancilla_qubits[0])
  circuit.append("MZ", ancilla_qubits[1])
  circuit.append("MZ", ancilla_qubits[2])
  circuit.append("R", ancilla_qubits[0])
  circuit.append("RX", ancilla_qubits[1])
  circuit.append("RX", ancilla_qubits[2])
  
  # Second half
  circuit.append("CNOT", [data_qubits[4], ancilla_qubits[0]])
  circuit.append("CNOT", [ancilla_qubits[1], data_qubits[6]])
  circuit.append("CNOT", [ancilla_qubits[2], data_qubits[5]])
  circuit.append("TICK")
  
  circuit.append("CNOT", [ancilla_qubits[2], ancilla_qubits[0]])
  circuit.append("TICK")
  
  circuit.append("CNOT", [data_qubits[0], ancilla_qubits[0]])
  circuit.append("CNOT", [ancilla_qubits[1], data_qubits[4]])
  circuit.append("CNOT", [ancilla_qubits[2], data_qubits[1]])
  circuit.append("TICK")

  circuit.append("CNOT", [data_qubits[2], ancilla_qubits[0]])
  circuit.append("CNOT", [ancilla_qubits[1], data_qubits[3]])
  circuit.append("CNOT", [ancilla_qubits[2], data_qubits[6]])
  circuit.append("TICK")

  circuit.append("CNOT", [ancilla_qubits[1], ancilla_qubits[0]])
  circuit.append("TICK")

  circuit.append("CNOT", [data_qubits[6], ancilla_qubits[0]])
  circuit.append("CNOT", [ancilla_qubits[1], data_qubits[5]])
  circuit.append("CNOT", [ancilla_qubits[2], data_qubits[2]])
  circuit.append("TICK") # Maybe extraneous TICK?

  # Measure the last stabilizers
  circuit.append("MZ", ancilla_qubits[0])
  circuit.append("MX", ancilla_qubits[1])
  circuit.append("MX", ancilla_qubits[2])
  
  return

