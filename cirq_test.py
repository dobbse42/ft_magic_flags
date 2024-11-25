import cirq
from steane_cirq import meas_H_logical_ft_flag

circuit = cirq.Circuit()

data_qubits = cirq.LineQubit.range(7)
ancilla_qubits = [cirq.LineQubit(7), cirq.LineQubit(8)]

meas_H_logical_ft_flag(circuit, data_qubits, ancilla_qubits)

print(circuit)
