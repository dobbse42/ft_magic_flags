import cirq
import matplotlib.pyplot as plt
from steane_cirq import meas_H_logical_ft_1flag, distill_magic_state, H_logical_nonft, H_logical_ft_flag1, controlled_h

circuit = cirq.Circuit()
qubitmanager = cirq.SimpleQubitManager()

data_qubits = cirq.LineQubit.range(7)
ancilla_qubits = [cirq.LineQubit(7), cirq.LineQubit(8), cirq.LineQubit(9), cirq.LineQubit(10), cirq.LineQubit(11)]

H_logical_ft_flag1(circuit, data_qubits, ancilla_qubits, qubitmanager)

#H_logical_nonft(circuit, data_qubits)
#meas_H_logical_ft_1flag(circuit, data_qubits, ancilla_qubits, qubitmanager)
#distill_magic_state(circuit, ancilla_qubits[0], data_qubits[0])
#circuit.append(cirq.measure(data_qubits[0]))

s = cirq.Simulator()
result = s.run(circuit, repetitions=1)
print(result)
#_ = cirq.plot_state_histogram(result, plt.subplot())
#plt.show()
#plt.savefig("test.svg")
#print(circuit)
