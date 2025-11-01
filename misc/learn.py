from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# quantum circuit with 2 qubits. both in default 0 state
qc = QuantumCircuit(2) 

# hadamard gate - puts index0 qubit in superposition so could be 0 or 1
qc.h(0) 

# control not gate - puts i0 qubit as control, and i1 qubit as target
# if control is 0, then nothing
# if control is 1, then NOT/invert the target qubit
qc.cx(0,1) 

# NOT gate applied to i1 qubit
qc.x(1)
qc.measure_all() 

# sample the quantum circuit 1024 times and plot histogram of results
sampler = StatevectorSampler() 
result = sampler.run([qc], shots=1024).result() 
counts = result[0].data.meas.get_counts() 
plot_histogram(counts)
plt.show()