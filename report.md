
### Problem Statement
We will be implementing the technique presented in [1] for fault-tolerant magic state preparation in software. Specifically, we will verify the circuits in figures 1-7 and the results in figures 9, 10.

This amounts to verifying 1) that magic state distillation works, 2) that the distilled states can be used in other computations, such as measuring the Hadamard operator, 3) that logical $\ket{H}$ states can be produced with only stabilizer operations, and 4) that the original flag-qubit scheme works for various fault-tolerant operations in the Steane code and the $[[17, 1, 5]]$ color code, as well as simulating the scheme for many qubits.

### Methods
As convenient as it would be to use stim for our simulations, this would not be possible without a great deal of effort. Amusingly, ChatGPT incorrectly believes stim to be possible of directly simulating T gates. Unfortunately (or perhaps fortunately for the careers of those in the field), stim is not capable of this, so we would need to resort to using techniques from one of [2], [3], or [4] (as suggested by Craig Gidney in [6]). However, only figures 1, 2, and 4 require non-stabilizer operations, so we will use stim for the other circuits. For figures 1, 2, and 4 we will use cirq, as they are relatively small in size and so should be easy enough to simulate. For any supplementary simulations necessary to generate plots we will make use of either stim or cirq as deemed necessary on a case-by-case basis. Our analysis of gate and qubit counts for given physical and logical error rates will be done in a manner mirroring that in [1] (appendix C). In [1] this analysis is based on simulations giving the expected number of repetitions of the flag ft syndrome extraction circuits. These circuits are stabilizer circuits, and the authors do not specify how these simulations were performed (they state that these number were obtained with "Monte Carlo simulation with $10^6$ trials"), though considering the authors' use of qiskit for other portions of the paper (appendix E) and their position at IBM it is possible they used qiskit for this (though stim should work just as well and be far faster). Regardless, we will use stim to obtain analogous numbers. 

While there is not necessarily a place for it in this report, we point out the following works which build upon or provide alternatives to Chamberland and Cross' original 2019 scheme: 
[7]. 2020 Cross (AWS)  
[8]. 2023 (IBM)
[9]. 2024 Magic State Cultivation (Google)

### Expected Results
We expect that our simulations of figures 1-7 will verify the authors' results, as many of these circuits are very small and have been used as the foundation for many more complex circuits and techniques. The more interesting result to predict is the failure rate at higher levels of code concatenation (part D). Notably figures 9 and 10 of [1] do not give this value, but instead simply report the gate and qubit counts required to stay *below* a certain failure rate, given different physical error rates (hence the stepwise nature of the plots, as each 'step' represents an increase in concatenation level). We would expect that as the concatenation level increases, the failure rate of the scheme will decrease in the same manner as the distance of the code. Since codes perform differently depending on how far below their threshold the physical error rate is (i.e. since threshold graphs are not linear), we would not expect the difference in failure rates between code concatenation levels to remain constant as the physical error rate changes. With that said, Figure 7 from [5] implies that we might expect near constant differences in failure rates simply because we are using a concatenated Steane code. However, if we were to repeat this process for a flag scheme on some other easily concatenated code we would not expect to see similarly stable results. In figure 9 of [1], at a fixed physical error rate of $p=3*10^{-5}$, the failure rate of the scheme can be inferred to decrease by approximately an order of magnitude per level of concatenation, so we should expect similar results at most physical error rates (though it is worth noting that [5] only considers physical error rates of $10^{-4}$ and higher).

### References
[1](https://quantum-journal.org/papers/q-2019-05-20-143/pdf/)
[2](https://quantum-journal.org/papers/q-2019-09-02-181/)
[3](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.123.170502)
[4](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.99.052307)
[5](https://arxiv.org/pdf/2403.09978)
[6](https://arxiv.org/abs/2103.02202)
[7](https://www.nature.com/articles/s41534-020-00319-5)
[8](https://www.nature.com/articles/s41586-023-06846-3)
[9](https://arxiv.org/pdf/2409.17595)
