import stim
from magic_stim import magic_state_distillation
from steane_stim import create_steane_0, stab_extract_ft_flag

def pretty_print_detector(sample, n):
  for k in range(0, len(sample), n):
    timeslice = sample[k:k+n]
    print("".join("!" if e else "_" for e in timeslice))
  return

def pretty_print_measure(sample, n):
  for k in range(0, len(sample), n):
    timeslice = sample[k:k+n]
    print("".join("1" if e else "-" for e in timeslice))
  return

print([i for i in range(7)])

circuit = stim.Circuit()
create_steane_0(circuit)
stab_extract_ft_flag(circuit, [i for i in range(7)], [8, 9, 10])
print(circuit)

'''
circuit.append("H", [0])
circuit.append("H", [1])
circuit.append("H", [2])
circuit.append("H", [3])
circuit.append("H", [4])
circuit.append("H", [5])
circuit.append("H", [6])
circuit.append("H", [7])
circuit.append("H", [8])

circuit.append("X_ERROR", [0, 1, 2, 3, 4, 5, 6, 7, 8], 0.2)
circuit.append("TICK")


circuit.append("CNOT", [0, 1])
circuit.append("TICK")

circuit.append("M", [0, 1, 2, 3, 4, 5, 6, 7, 8])
for i in range(1, 10):
  circuit.append("DETECTOR", stim.target_rec(-i))


print(repr(circuit))

sampler = circuit.compile_detector_sampler()
sample = sampler.sample(shots=1)[0]
pretty_print_detector(sample, 9)
'''
