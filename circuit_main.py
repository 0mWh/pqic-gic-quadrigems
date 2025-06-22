import numpy as np
import scipy as sp

import qiskit

from qiskit import QuantumCircuit as QC
from qiskit import QuantumRegister as QR
from qiskit.circuit.library import *

# unused. probably never will be
from qiskit_aer import AerSimulator as Aer
def sim_pure(qc):
	Aer().run(qc).result().get_statevector()

# angle embedding
def qc_angleembed(qc:QC, qs:list[int], data):
	# TODO: process/normalize data?
	qc.ry(data, qubits)
	None

# amplitude encoding
def qc_amplitudeencode(qc:QC, qs:list[int], data):
	# TODO
	None

# inverse quantum forier
def qc_qft(qc:QC, qs:list[int]):
	qc.append(QFT(len(qs)).inverse(), qs)

# n-bit swap test
def qc_swap(qc:QC, left:list[int], right:list[int], ans:int):
	qc.h(ans)
	for l, r in zip(left, right):
		qc.cswap(ans, l, r)
	qc.h(ans)

# nearest-neighbor entanglement
# just cnot gates between each adj. qbit
def qc_nn(qc:QC, qs:list[int]):
	qc.cx(qs[:-1], qs[1:])


# example
qc = QC(9, 1)

# load data
# TODO: 
#  get data
#  decide angle/amplitude

qc.barrier()

# transform
qc_qft(qc, [1,2,3,4])
qc_qft(qc, [5,6,7,8])

qc.barrier()

# analysis
qc_swap(qc, [1,2,3,4], [5,6,7,8], 0)

qc.barrier()

# measure
# TODO
qc.measure(0, cbit=0)


print(qc.draw())