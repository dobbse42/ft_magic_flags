import cirq
import numpy as np
import sympy

class my_T(cirq.Gate):
  def __init__(self):
    super(my_T, self)

  def _num_qubits_(self):
    return 1

  def _unitary_(self):
    return np.array([
      [np.cos(np.pi/8), -1*np.sin(np.pi/8)],
      [np.sin(np.pi/8), np.cos(np.pi/8)]
    ])

  def _circuit_diagram_info(self, args):
    return "my_T"


''' ancilla is assumed to start in the $\ket{0}$ state
'''
def distill_magic_state(circuit, ancilla, data, adj=False):
  circuit.append(my_T().on(ancilla))
  circuit.append(cirq.Y(data).controlled_by(ancilla))
  #measure in the Y-basis
  circuit.append(cirq.measure_single_paulistring(cirq.Y(ancilla), key='anc_'+str(ancilla)))

  #apply correction
  if adj:
    symbol = sympy.Symbol('anc_'+str(ancilla))
    expr = sympy.Eq(symbol, 0)
    circuit.append((cirq.S(data)**-1).with_classical_controls(cirq.SympyCondition(expr))) #probably not 1, but actually 0
  else:
    circuit.append(cirq.S(data).with_classical_controls('anc_'+str(ancilla)))



def controlled_h(circuit, control, target, qubitmanager):
  #circuit.append(cirq.T(target) ** -1)
  magic = qubitmanager.qalloc(1)[0]
  # apply a T gate with some probability of error to create the magic state
  circuit.append(cirq.T(magic))
  distill_magic_state(circuit, magic, target, adj=True)

  circuit.append(cirq.CZ(control, target))
  
  #circuit.append(cirq.T(target))
  magic_2 = qubitmanager.qalloc(1)[0]
  distill_magic_state(circuit, magic_2, target)

def meas_H_logical_ft_1flag(circuit, data_qubits, ancilla_qubits, qubitmanager):
  # Use if you want the cirq implemention of CH rather than custom decomp
  # controlled_h = cirq.ControlledGate(sub_gate=cirq.H, num_controls=1)

  # send ancilla[0] to $\ket{+}$
  circuit.append(cirq.H(ancilla_qubits[0]))

  controlled_h(circuit, ancilla_qubits[0], data_qubits[6], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  
  controlled_h(circuit, ancilla_qubits[0], data_qubits[5], qubitmanager)
  controlled_h(circuit, ancilla_qubits[0], data_qubits[4], qubitmanager)
  controlled_h(circuit, ancilla_qubits[0], data_qubits[3], qubitmanager)
  controlled_h(circuit, ancilla_qubits[0], data_qubits[2], qubitmanager)
  controlled_h(circuit, ancilla_qubits[0], data_qubits[1], qubitmanager)

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  circuit.append(cirq.measure(ancilla_qubits[1])) # measure Z ancilla[1]
  
  controlled_h(circuit, ancilla_qubits[0], data_qubits[0], qubitmanager)

  # measure ancilla[0] in the X-basis
  circuit.append(cirq.H(ancilla_qubits[0]))
  circuit.append(cirq.measure(ancilla_qubits[0], key='ans_meas_'+str(ancilla_qubits[0])))

  return

''' Assumes data_qubits is a list of 7 qubits initialized to $\ket{0}$ which will be sent into the encoded state.
'''
def H_logical_nonft(circuit, data_qubits):
  # initializing some qubits to $\ket{+}$
  circuit.append(cirq.H(data_qubits[0]))
  circuit.append(cirq.H(data_qubits[1]))
  circuit.append(cirq.H(data_qubits[3]))
  # initializing the h_index'th qubit to $\ket{H}$
  circuit.append(my_T().on(data_qubits[3]))

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

''' Assumes ancilla_qubits is a list of 5 qubits initialized to $\ket{0}$
'''
def H_logical_ft_flag1(circuit, data_qubits, ancilla_qubits, qubitmanager):
  H_logical_nonft(circuit, data_qubits)
  meas_H_logical_ft_1flag(circuit, data_qubits, ancilla_qubits[:2], qubitmanager)
  stab_extract_ft_flag(circuit, data_qubits, qubitmanager)
  return

def stab_extract_ft_flag(circuit, data_qubits, qubitmanager):
  ancilla_qubits = qubitmanager.qalloc(3)
  circuit.append(cirq.H(ancilla_qubits[0]))
  
  circuit.append(cirq.CNOT(ancilla_qubits[0], data_qubits[4]))
  circuit.append(cirq.CNOT(data_qubits[6], ancilla_qubits[1]))
  circuit.append(cirq.CNOT(data_qubits[5], ancilla_qubits[2]))

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))

  circuit.append(cirq.CNOT(ancilla_qubits[0], data_qubits[0]))
  circuit.append(cirq.CNOT(data_qubits[4], ancilla_qubits[1]))
  circuit.append(cirq.CNOT(data_qubits[1], ancilla_qubits[2]))

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))

  circuit.append(cirq.CNOT(ancilla_qubits[0], data_qubits[6]))
  circuit.append(cirq.CNOT(data_qubits[5], ancilla_qubits[1]))
  circuit.append(cirq.CNOT(data_qubits[2], ancilla_qubits[2]))

  circuit.append(cirq.H(ancilla_qubits[0]))
  circuit.append(cirq.measure(ancilla_qubits[0], key='syn_'+str(ancilla_qubits[0])))
  circuit.append(cirq.measure(ancilla_qubits[1], key='flag_'+str(ancilla_qubits[1])))
  circuit.append(cirq.measure(ancilla_qubits[2], key='flag_'+str(ancilla_qubits[2])))
  #circuit.append(cirq.ResetChannel().on_each(ancilla_qubits[0:3]))
  ancilla_qubits = qubitmanager.qalloc(3)
  circuit.append(cirq.H(ancilla_qubits[1]))
  circuit.append(cirq.H(ancilla_qubits[2]))

  circuit.append(cirq.CNOT(data_qubits[4], ancilla_qubits[0]))
  circuit.append(cirq.CNOT(ancilla_qubits[1], data_qubits[6]))
  circuit.append(cirq.CNOT(ancilla_qubits[2], data_qubits[5]))

  circuit.append(cirq.CNOT(ancilla_qubits[2], ancilla_qubits[0]))

  circuit.append(cirq.CNOT(data_qubits[0], ancilla_qubits[0]))
  circuit.append(cirq.CNOT(ancilla_qubits[1], data_qubits[4]))
  circuit.append(cirq.CNOT(ancilla_qubits[2], data_qubits[1]))

  circuit.append(cirq.CNOT(data_qubits[2], ancilla_qubits[0]))
  circuit.append(cirq.CNOT(ancilla_qubits[1], data_qubits[3]))
  circuit.append(cirq.CNOT(ancilla_qubits[2], data_qubits[6]))

  circuit.append(cirq.CNOT(ancilla_qubits[1], ancilla_qubits[0]))

  circuit.append(cirq.CNOT(data_qubits[6], ancilla_qubits[0]))
  circuit.append(cirq.CNOT(ancilla_qubits[1], data_qubits[5]))
  circuit.append(cirq.CNOT(ancilla_qubits[2], data_qubits[2]))

  circuit.append(cirq.H(ancilla_qubits[1]))
  circuit.append(cirq.H(ancilla_qubits[2]))
  circuit.append(cirq.measure(ancilla_qubits[0], key='syn_'+str(ancilla_qubits[0])))
  circuit.append(cirq.measure(ancilla_qubits[1], key='flag_'+str(ancilla_qubits[1])))
  circuit.append(cirq.measure(ancilla_qubits[2], key='flag_'+str(ancilla_qubits[2])))
  return


def meas_H_logical_ft_2flag(circuit, data_qubits, qubitmanager):
  ancilla_qubits = qubitmanager.qalloc(4)
  circuit.append(cirq.H(ancilla_qubits[0]))

  controlled_h(circuit, ancilla_qubits[0], data_qubits[6], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[5], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[4], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))
  circuit.append(cirq.measure(ancilla_qubits[2]))
  ancilla_qubits[2] = qubitmanager.qalloc(1)[0]
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[1], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[3], qubitmanager)
  circuit.append(cirq.measure(ancilla_qubits[2]))
  circuit.append(cirq.measure(ancilla_qubits[3]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[0], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[2], qubitmanager)
  circuit.append(cirq.measure(ancilla_qubits[1]))
  circuit.append(cirq.measure_single_paulistring(cirq.X(ancilla_qubits[0])*cirq.I(data_qubits[0])))

  return


def H_logical_ft_flag2(circuit, data_qubits, qubitmanager):
  H_logical_nonft(circuit, data_qubits)
  meas_H_logical_ft_2flag(circuit, data_qubits, qubitmanager)
  stab_extract_ft_flag(circuit, data_qubits, qubitmanager)
  meas_H_logical_ft_2flag(circuit, data_qubits, qubitmanager)
  stab_extract_ft_flag(circuit, data_qubits, qubitmanager)
  meas_H_logical_ft_2flag(circuit, data_qubits, qubitmanager)

  return


def meas_H_logical_ft_17(circuit, data_qubits, qubitmanager):
  ancilla_qubits = qubitmanager.qalloc(5)
  circuit.append(cirq.H(ancilla_qubits[0]))

  controlled_h(circuit, ancilla_qubits[0], data_qubits[0], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[1], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[2], qubitmanager)
  controlled_h(circuit, ancilla_qubits[0], data_qubits[3], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[4], qubitmanager)
  controlled_h(circuit, ancilla_qubits[0], data_qubits[5], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[4]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[6], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  circuit.append(cirq.measure(ancilla_qubits[3]))
  ancilla_qubits[3] = qubitmanager.qalloc(1)[0]
  controlled_h(circuit, ancilla_qubits[0], data_qubits[7], qubitmanager)

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[8], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[4]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[9], qubitmanager)
  circuit.append(cirq.measure(ancilla_qubits[4]))
  ancilla_qubits[4] = qubitmanager.qalloc(1)[0]

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[4]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[10], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  circuit.append(cirq.measure(ancilla_qubits[3]))
  ancilla_qubits[3] = qubitmanager.qalloc(1)[0]
  controlled_h(circuit, ancilla_qubits[0], data_qubits[11], qubitmanager)


  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[12], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[4]))
  circuit.append(cirq.measure(ancilla_qubits[4]))
  ancilla_qubits[4] = qubitmanager.qalloc(1)[0]
  controlled_h(circuit, ancilla_qubits[0], data_qubits[13], qubitmanager)

  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[4]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[14], qubitmanager)
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[3]))
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[1]))
  circuit.append(cirq.measure(ancilla_qubits[3]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[15], qubitmanager)
  circuit.append(cirq.measure(ancilla_qubits[1]))
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[2]))
  controlled_h(circuit, ancilla_qubits[0], data_qubits[16], qubitmanager)
  circuit.append(cirq.measure(ancilla_qubits[2]))
  circuit.append(cirq.CNOT(ancilla_qubits[0], ancilla_qubits[4]))
  circuit.append(cirq.measure(ancilla_qubits[4]))
  circuit.append(cirq.measure_single_paulistring(cirq.X(ancilla_qubits[0] * cirq.I(data_qubits[0]))))

  return










