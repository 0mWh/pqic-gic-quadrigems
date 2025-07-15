from qiskit import (
	QuantumCircuit as QC,
	QuantumRegister as QR,
	ClassicalRegister as CR
)


def qc_angle_embed(qc:QC, qubits:QR, thetas:list[float]):
	"""Simple Ry angle encoding."""
	for qubit, theta in zip(qubits, thetas):
		qc.ry(theta, qubit)
	qc.barrier()

from qiskit.circuit.library import QFT
def qc_qft(qc:QC, qubits:QR, inverse=False):
	"""Apply inverse QFT."""
	qft = QFT(len(qubits), do_swaps=False)
	if inverse: qft = qft.inverse()
	qc.append(qft.decompose(), qubits)
	qc.barrier()

def qc_swaptest(qc:QC, left:QR, right:QR, ans:QR):
	"""n-Bit Two-sided Swap-Test"""
	qc.h(ans)
	for l, r in zip(left, right):
		qc.cswap(ans, l, r)
	qc.h(ans)
	qc.barrier()

def qc_swaptest_nonassociative(qc:QC, left:QR, right:QR):
	"""n-Bit One-sided Swap-Test"""
	qc.cx(left, right)
	qc.h(left)
	qc.barrier()

from itertools import combinations
def qc_iqp_embed(qc:QC, qubits:QR, x):
    for qubit, theta in zip(qubits, x):
        qc.rz(theta, qubit)
    for (qa, ta), (qb, tb) in combinations(zip(qubits, x), 2):
        qc.rzz(ta * tb, qa, qb)
    qc.barrier()