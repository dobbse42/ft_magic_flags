import cirq
import matplotlib.pyplot as plt
from steane_cirq import meas_H_logical_ft_1flag, distill_magic_state, H_logical_nonft, H_logical_ft_flag1, controlled_h, meas_H_logical_ft_2flag, H_logical_ft_flag2, my_T

circuit = cirq.Circuit()
qubitmanager = cirq.SimpleQubitManager()

data_qubits = cirq.LineQubit.range(7)
ancilla_qubits = [cirq.LineQubit(7), cirq.LineQubit(8), cirq.LineQubit(9), cirq.LineQubit(10), cirq.LineQubit(11)]

#H_logical_ft_flag1(circuit, data_qubits, ancilla_qubits, qubitmanager)
#meas_H_logical_ft_2flag(circuit, data_qubits, qubitmanager)
#H_logical_nonft(circuit, data_qubits)
#H_logical_ft_flag2(circuit, data_qubits, qubitmanager)


# Testing magic state distillation

distill_magic_state(circuit, ancilla_qubits[0], data_qubits[0])
circuit.append(cirq.measure_single_paulistring(cirq.Z(data_qubits[0])))
#circuit.append(my_T().on(data_qubits[1]))
#circuit.append(cirq.measure_single_paulistring(cirq.Z(data_qubits[1])))


circuit = circuit.with_noise(cirq.depolarize(p=0.2))

s = cirq.Simulator()
result = s.run(circuit, repetitions=1000)
#print(result)
_ = cirq.plot_state_histogram(result.histogram(key=str(data_qubits[0])), plt.subplot())
#plt.show()
plt.savefig("test.svg")
#print(circuit)


