import math
import numpy as np
from qiskit import QuantumCircuit, transpile
from math import gcd
from numpy.random import randint
from fractions import Fraction
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_aer import Aer

class Factorer:
    def __init__(self, N: int, use_real_device: bool = False):
        self.N = N
        self.use_real_device = use_real_device
        self.__a = randint(2, N)
        self.__backend = None

    def shor_factor(self) -> tuple[int, int]:
        while True:
            greatest_common_divisor = gcd(self.__a, self.N)
            if greatest_common_divisor != 1:
                return greatest_common_divisor, self.N // greatest_common_divisor

            # Find the period 'r' of a^x mod N
            phase = self.__qpe_amod15(self.__a) / (2**8)
            frac = Fraction(phase).limit_denominator(self.N)
            r = frac.denominator

            # If 'r' is odd, repeat
            if r % 2 != 0:
                continue

            p = gcd(self.__a**(r//2) + 1, self.N)
            q = gcd(self.__a**(r//2) - 1, self.N)
            
            if p != 1 and p != self.N:
                return p, q


    def classical_factor(self) -> tuple[int, int]:
        if self.N % 2 == 0:
            return 2, self.N // 2
        for i in range(3, int(math.sqrt(self.N)) + 1, 2):
            if self.N % i == 0:
                return i, self.N // i
        return None, None

    def __qpe_amod15(self, a):
        n_count = 8
        qc = QuantumCircuit(4 + n_count, n_count)
        for q in range(n_count):
            qc.h(q)
        qc.x(3+n_count)
        for q in range(n_count):
            qc.append(self.__c_amod15(a, 2**q), 
                     [q] + [i+n_count for i in range(4)])
        qc.append(self.__qft_dagger(n_count), range(n_count))
        qc.measure(range(n_count), range(n_count))

        if self.use_real_device:
            if not self.__backend:
                print("Connecting to IBM Quantum service...")
                service = QiskitRuntimeService()
                self.__backend = service.least_busy(simulator=False, operational=True)
                print(f"Using backend: {self.__backend.name}")
            
            t_qc = transpile(qc, self.__backend)
            sampler = Sampler(self.__backend)
            job = sampler.run([t_qc], shots=1)
            result = job.result()[0]
            # The output is a bitarray, convert it to an integer
            return result.data.c.get_int_counts().popitem()[0]
        else:
            # Use local simulator
            aer_sim = Aer.get_backend('aer_simulator')
            t_qc = transpile(qc, aer_sim)
            counts = aer_sim.run(t_qc, shots=1, memory=True).result().get_memory()
            return int(counts[0], 2)
    def __qft_dagger(self, n):
        qc = QuantumCircuit(n)
        for qubit in range(n//2):
            qc.swap(qubit, n-qubit-1)
        for j in range(n):
            for m in range(j):
                qc.cp(-np.pi/float(2**(j-m)), m, j)
            qc.h(j)
        return qc.to_gate(label="QFT†")

    def __c_amod15(self, a, power):
        U = QuantumCircuit(4)        
        for _ in range(power):
            if a in [2,13]:
                U.swap(0,1)
                U.swap(1,2)
                U.swap(2,3)
            if a in [7,8]:
                U.swap(2,3)
                U.swap(1,2)
                U.swap(0,1)
            if a == 11:
                U.swap(1,3)
                U.swap(0,2)
            if a in [7,11,13]:
                for q in range(4):
                    U.x(q)
        U = U.to_gate()
        U.name = "%i^%i mod 15" % (a, power)
        c_U = U.control()
        return c_U