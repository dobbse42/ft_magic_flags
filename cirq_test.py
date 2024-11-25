import cirq
from steane_cirq import meas_H_logical_ft_1flag, distill_magic_state, H_logical_nonft

circuit = cirq.Circuit()

data_qubits = cirq.LineQubit.range(7)
ancilla_qubits = [cirq.LineQubit(7), cirq.LineQubit(8)]

H_logical_nonft(circuit, data_qubits)
#meas_H_logical_ft_flag1(circuit, data_qubits, ancilla_qubits)

print(circuit)
