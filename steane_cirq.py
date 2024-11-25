import cirq

''' ancilla is assumed to start in the $\ket{H}$ state
'''
def distill_magic_state(circuit, ancilla, data):
  circuit.append(cirq.CY(ancilla, data))
  
  #measure in the Y-basis
  circuit.append(cirq.S(ancilla) ** -1) # changing basis
  circuit.append(cirq.measure(ancilla, key="m")) # measurement with key m

  #apply correction
  circuit.append(cirq.S(data).controlled_by(cirq.KeyCondition("m", 1)))


def controlled_h(circuit, control, target):
  circuit.append(cirq.T(target) ** -1)
  circuit.append(cirq.CZ(control, target))
  circuit.append(cirq.T(target))


def meas_H_logical_ft_flag(circuit, data_qubits, ancilla_qubits):
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

