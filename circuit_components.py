from qiskit import (
    QuantumCircuit as QC,
    QuantumRegister as QR,
    ClassicalRegister as CR
)


def qc_angle_embed(qc:QC, qubits:QR, thetas:list[float]):
    """Simple Ry angle encoding."""
    for qubit, theta in zip(qubits, thetas):
        qc.ry(theta, q)
    qc.barrier()

from qiskit.circuit.library import QFT
def qc_iqft(qc:QC, qubits:QR, inverse=False):
    """Apply inverse QFT."""
    qft = QFT(len(qubits), do_swaps=False)
    if inverse: qft = qft.inverse()
    qc.append(qft, qubits)
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

