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
def wire_trim(qc_in:QC, split_cbits:bool=False, sort_qbits:bool=True) -> QC:
    if sort_qbits:
        qrmap_all = list(set(sum({ci.qubits for ci in qc_in}, ())))
        qrmap_measured = [
            gate.qubits[0]
            for gate in sorted(
                (gate for gate in qc_in[:] if gate.name == 'measure'),
                key = lambda g: g.clbits[0]._index
            )
        ]
        qrmap = {i: QR(1, name=f"q{i._index}") for i in qrmap_measured + qrmap_all}
    else:
        qrmap = {i: QR(1, name=f"q{i._index}") for i in set(sum({ci.qubits for ci in qc_in}, ()))}
    if split_cbits:
        crmap = {i: CR(1, name=f"c{i._index}") for i in list(sum({ci.clbits for ci in qc_in}, ()))}
        qc_out = QC(*qrmap.values(), *crmap.values())
    else:
        crmap = dict(zip(sum(map(list, qc_in.cregs), []), cr_out:=CR(sum(cr.size for cr in qc_in.cregs))))
        qc_out = QC(*qrmap.values(), cr_out)
    for gate in qc_in:
        qc_out.append(gate.replace(
            qubits = [qrmap[q] for q in gate.qubits],
            clbits = [crmap[q] for q in gate.clbits],
        ))
    return qc_out
QC.trim = lambda self, **kwargs: wire_trim(self, **kwargs)