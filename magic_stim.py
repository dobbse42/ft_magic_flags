import stim


''' Assumes that q_magic begins in the $\bra{H}$ state.
'''
def magic_state_distillation(circuit, q_magic, q_ancilla):
  circuit.append("CY", [q_magic, q_ancilla])
  circuit.append("MY", q_magic)
  circuit.append("CY", [stim.target_rec(-1), q_ancilla])
  return

