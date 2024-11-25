import cirq

''' ancilla is assumed to start in the $\ket{H}$ state
'''
def distill_magic_state(circuit, ancilla, data, adj=False):
  circuit.append(cirq.Y(data).controlled_by(ancilla))
  
  #measure in the Y-basis
  circuit.append(cirq.S(ancilla) ** -1) # changing basis
  circuit.append(cirq.measure(ancilla, key="m")) # measurement with key m

  #apply correction
  #circuit.append(cirq.S(data).controlled_by(cirq.KeyCondition("m", 1)))
  if adj:
    circuit.append((cirq.S(data)**-1).with_classical_controls(cirq.KeyCondition("m", 1))) #probably not 1, but actually 0
  else:
    circuit.append(cirq.S(data).with_classical_controls(cirq.KeyCondition("m", 1)))



def controlled_h(circuit, control, target):
  #circuit.append(cirq.T(target) ** -1)
  magic = cirq.LineQubit(99) # This is terrible practice. I do this as a stopgap solution, but this should be replaced with proper use of QubitManager.qalloc() ASAP (though I believe this requires properly implementing circuit decompositions, etc.)
  # apply a T gate with some probability of error to create the magic state
  circuit.append(cirq.T(magic))
  distill_magic_state(circuit, magic, target, adj=True)

  circuit.append(cirq.CZ(control, target))
  
  #circuit.append(cirq.T(target))
  distill_magic_state(circuit, magic, target)

def meas_H_logical_ft_1flag(circuit, data_qubits, ancilla_qubits):
  # Use if you want the cirq implemention of CH rather than custom decomp
  # controlled_h = cirq.ControlledGate(sub_gate=cirq.H, num_controls=1)

  # send ancilla[0] to $\ket{+}$
  circuit.append(cirq.H(ancilla_qubits[0]))

  controlled_h(circuit, ancilla_qubits[0], data_qubits[6])
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  
  controlled_h(circuit, ancilla_qubits[0], data_qubits[5])
  controlled_h(circuit, ancilla_qubits[0], data_qubits[4])
  controlled_h(circuit, ancilla_qubits[0], data_qubits[3])
  controlled_h(circuit, ancilla_qubits[0], data_qubits[2])
  controlled_h(circuit, ancilla_qubits[0], data_qubits[1])

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  circuit.append(cirq.measure(ancilla_qubits[1])) # measure Z ancilla[1]
  
  controlled_h(circuit, ancilla_qubits[0], data_qubits[0])

  # measure ancilla[0] in the X-basis
  circuit.append(cirq.H(ancilla_qubits[0]))
  circuit.append(cirq.measure(ancilla_qubits[0]))

  return

''' Assumes data_qubits is a list of 7 qubits initialized to $\ket{0}$ which will be sent into the encoded state.
'''
def H_logical_nonft(circuit, data_qubits):
  # initializing some qubits to $\ket{+}$
  circuit.append(cirq.H(data_qubits[0]))
  circuit.append(cirq.H(data_qubits[1]))
  circuit.append(cirq.H(data_qubits[3]))
  # initializing the h_index'th qubit to $\ket{H}$
  circuit.append(cirq.T(data_qubits[3]))

  circuit.append(cirq.CNOT(data_qubits[3], data_qubits[4]))
  circuit.append(cirq.CNOT(data_qubits[0], data_qubits[6]))
  circuit.append(cirq.CNOT(data_qubits[3], data_qubits[5]))
  circuit.append(cirq.CNOT(data_qubits[2], data_qubits[5]))
  circuit.append(cirq.CNOT(data_qubits[0], data_qubits[4]))
  circuit.append(cirq.CNOT(data_qubits[1], data_qubits[6]))
  circuit.append(cirq.CNOT(data_qubits[0], data_qubits[2]))
  circuit.append(cirq.CNOT(data_qubits[1], data_qubits[5]))
  circuit.append(cirq.CNOT(data_qubits[3], data_qubits[4]))
  circuit.append(cirq.CNOT(data_qubits[1], data_qubits[2]))
  circuit.append(cirq.CNOT(data_qubits[3], data_qubits[6]))

  return

def H_logical_ft_flag1(circuit, data_qubits, ancilla_qubits):
  H_logical_nonft(circuit, data_qubits)
  meas_H_logical_ft_1flag(circuit, data_qubits, ancilla_qubits[:2])
  stab_extract_ft_flag(circuit, data_qubits, ancilla_qubits[2:])
