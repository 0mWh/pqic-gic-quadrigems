from qiskit import (
    QuantumCircuit as QC,
    QuantumRegister as QR,
    ClassicalRegister as CR
)


def pipeline_swap_diagonal_test(data1, data2):
    assert len(data1) == len(data2)
    
    qc = QC(
        qA := QR(len(data1), 'A'), # |φ(→y)⟩
        qB := QR(len(data2), 'B'), # |φ(→x)⟩
        cS := CR(len(data1), 's'), # s_i
        cT := CR(len(data2), 't'), # s_t
    )

    # 1. Encode both feature vectors
    qc_angle_embed(qc, qA, data1)
    qc_angle_embed(qc, qB, data2)

    # 2. Nonlinear Transform
    qc_iqft(qc, qA)
    qc_iqft(qc, qB)
    
    # 3. Diagonalise SWAP : CNOT (A→B) + H on A
    qc_swaptest_nonassociative(qc, qA, qB)

    # 4. Measure every qubit
    qc.measure(qA, cbit=cS)
    qc.measure(qB, cbit=cT)
    return qc