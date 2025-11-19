
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import grover_operator, MCMTGate, ZGate
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_aer import Aer
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

class Searcher:
    def __init__(self, list_to_search, use_real_device: bool = False):
        self.list_to_search = list_to_search
        self.use_real_device = use_real_device
        self.__backend = None

    def classical_search(self, element_to_find):
        for i, element in enumerate(self.list_to_search):
            if element == element_to_find:
                return i
        return -1

    def grover_search(self, marked_states):
        oracle = self.__grover_oracle(marked_states)
        grover_op = grover_operator(oracle)
        optimal_num_iterations = math.floor(
            math.pi
            / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))
        )
        qc = QuantumCircuit(grover_op.num_qubits)
        qc.h(range(grover_op.num_qubits))
        qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
        qc.measure_all()
        qc = qc.decompose()

        if self.use_real_device:
            if not self.__backend:
                print("Connecting to IBM Quantum service...")
                service = QiskitRuntimeService()
                self.__backend = service.least_busy(simulator=False, operational=True)
                print(f"Using backend: {self.__backend.name}")
            
            pm = generate_preset_pass_manager(target=self.__backend.target, optimization_level=3)
            circuit_isa = pm.run(qc)
            sampler = Sampler(self.__backend)
            result = sampler.run([circuit_isa]).result()
            dist = result[0].data.meas.get_counts()
            return dist
        else:
            aer_sim = Aer.get_backend('aer_simulator')
            sampler = Sampler(aer_sim)
            result = sampler.run([qc]).result()
            dist = result[0].data.meas.get_counts()
            return dist


    def __grover_oracle(self, marked_states):
        if not isinstance(marked_states, list):
            marked_states = [marked_states]
        num_qubits = len(marked_states[0])
        qc = QuantumCircuit(num_qubits)
        for target in marked_states:
            rev_target = target[::-1]
            zero_inds = [
                ind
                for ind in range(num_qubits)
                if rev_target.startswith("0", ind)
            ]
            if zero_inds:
                qc.x(zero_inds)
            qc.compose(MCMTGate(ZGate(), num_qubits - 1, 1), inplace=True)
            if zero_inds:
                qc.x(zero_inds)
    def __grover_oracle(self, marked_states):
        if not isinstance(marked_states, list):
            marked_states = [marked_states]
        num_qubits = len(marked_states[0])
        qc = QuantumCircuit(num_qubits)
        for target in marked_states:
            rev_target = target[::-1]
            zero_inds = [
                ind
                for ind in range(num_qubits)
                if rev_target.startswith("0", ind)
            ]
            if zero_inds:
                qc.x(zero_inds)
            qc.compose(MCMTGate(ZGate(), num_qubits - 1, 1), inplace=True)
            if zero_inds:
                qc.x(zero_inds)
        return qc.decompose()

    def plot_distribution(self, dist):
        from qiskit.visualization import plot_distribution
        import matplotlib.pyplot as plt
        plot_distribution(dist)
        plt.savefig('search/distribution.png')
