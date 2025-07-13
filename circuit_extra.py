import qiskit
import qiskit.qasm3
import pennylane as qml

from qiskit import (
    QuantumCircuit as QC,
    QuantumRegister as QR,
    ClassicalRegister as CR,
)


def test_pennylane_circuit(x):
    qml.RZ(x, wires=0)
    qml.CNOT(wires=[0,1])
    qml.RY(x, wires=1)
    return qml.expval(qml.Z(wires=1))

def test_qiskit_circuit() -> tuple[QC,str]:
    qc = QC(qr:=QR(3), cr1:=CR(3))
    qc.h(qr[0])
    qc.cx(qr[0], qr[1:])
    qc.measure(qr,cr1)
    return qc, qiskit.qasm3.dumps(qc)

# remove unused qubits from a circuit. useful when pulling circuits back from execution
def wire_trim(qc_in:QC) -> QC:
    qrmap = {i: QR(1, name=f"q{i._index}") for i in list(sum({ci.qubits for ci in qc_in}, ()))}
    crmap = {i: CR(1, name=f"c{i._index}") for i in list(sum({ci.clbits for ci in qc_in}, ()))}
    qc_out = QC(*qrmap.values(), *crmap.values())
    for gate in qc_in:
        qc_out.append(gate.replace(qubits=[qrmap[q] for q in gate.qubits], clbits=[crmap[q] for q in gate.clbits]))
    return qc_out
QC.trim = lambda self: wire_trim(self)