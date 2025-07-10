import pennylane as qml
import numpy as np

def circuit_with_dev(circuit, dev):
    return qml.qjit(seed=0)(qml.qnode(dev)(circuit))

def executor(dev):
    return lambda circuit: qml.qjit(seed = 0)(qml.qnode(dev)(circuit))

# angle / iqp / amplitude
# qft / iqft
# total 6 types of circuits

# Angle Embed -> QFT -> SWAP
def circuit_angle_qft_swap(a, b):
    la, lb = len(a), len(b)
    assert la == lb

    # 1. Data: Angle Embedding
    qml.AngleEmbedding(a, wires=range(la))
    qml.AngleEmbedding(b, wires=range(la, la + lb))
    
    # 2. Nonlinear Transform: QFT
    qml.QFT(wires = range(la))
    qml.QFT(wires = range(la, la + lb))

    # 3. Correlation: SWAP Test
    for i in range(la):
        qml.CNOT(wires = [i, la + i])
    qml.Barrier()
    for i in range(la):
        qml.H(i)
    
    return qml.probs(wires = range(la + lb))

# Angle Embed -> iQFT -> SWAP
def circuit_angle_iqft_swap(a, b):
    la, lb = len(a), len(b)
    assert la == lb

    # 1. Data: Angle Embedding
    qml.AngleEmbedding(a, wires=range(la))
    qml.AngleEmbedding(b, wires=range(la, la + lb))
    
    # 2. Nonlinear Transform: QFT
    qml.adjoint(
    qml.QFT(wires = range(la))
    )
    qml.adjoint(
    qml.QFT(wires = range(la, la + lb))
    )

    # 3. Correlation: SWAP Test
    for i in range(la):
        qml.CNOT(wires = [i, la + i])
    qml.Barrier()
    for i in range(la):
        qml.H(i)
    
    return qml.probs(wires = range(la + lb))

# Polynomial Embed -> iQFT -> SWAP
def circuit_iqp_iqft_swap(a, b):
    la, lb = len(a), len(b)
    assert la == lb

    # 1. Data: Instantaneous Quantum Polynomial (IQP)
    qml.IQPEmbedding(a, wires=range(la), n_repeats=2)
    qml.IQPEmbedding(b, wires=range(la, la + lb), n_repeats=2)

    # 2. Nonlinear Transform: inverse QFT
    qml.adjoint(qml.QFT(wires = range(la)))
    qml.adjoint(qml.QFT(wires = range(la, la + lb)))

    # 3. Correlation: SWAP Test
    for i in range(la):
        qml.CNOT(wires = [i, la + i])
    qml.Barrier()
    for i in range(la):
        qml.H(i)

    return qml.probs(wires = range(la + lb))

# Polynomial Embed -> QFT -> SWAP
def circuit_iqp_qft_swap(a, b):
    la, lb = len(a), len(b)
    assert la == lb

    # 1. Data: Instantaneous Quantum Polynomial (IQP)
    qml.IQPEmbedding(a, wires=range(la), n_repeats=2)
    qml.IQPEmbedding(b, wires=range(la, la + lb), n_repeats=2)

    # 2. Nonlinear Transform: inverse QFT
    qml.QFT(wires = range(la))
    qml.QFT(wires = range(la, la + lb))

    # 3. Correlation: SWAP Test
    for i in range(la):
        qml.CNOT(wires = [i, la + i])
    qml.Barrier()
    for i in range(la):
        qml.H(i)

    return qml.probs(wires = range(la + lb))

# Amplitude Encoding overlap [Figure S.5B]
def circuit_amp_iamp(a, b):
    """
    Drawing
    0: ──H─╭|Ψ⟩──H─╭|Ψ⟩─╭|Ψ⟩†──H─╭|Ψ⟩†──H─┤ ╭Probs
    1: ──H─├|Ψ⟩──H─├|Ψ⟩─├|Ψ⟩†──H─├|Ψ⟩†──H─┤ ├Probs
    2: ──H─├|Ψ⟩──H─├|Ψ⟩─├|Ψ⟩†──H─├|Ψ⟩†──H─┤ ├Probs
    3: ──H─╰|Ψ⟩──H─╰|Ψ⟩─╰|Ψ⟩†──H─╰|Ψ⟩†──H─┤ ╰Probs
    """
    la, lb = len(a), len(b)
    assert la == lb
    # assert power of 2
    n_wires = np.log2(la)
    assert n_wires == int(n_wires)
    n_wires = int(n_wires)
    # print(la, lb)

    # 1. Data: Amplitude Embedding
    for i in range(2):
        for j in range(n_wires):
            qml.H(j)
        qml.AmplitudeEmbedding(a, wires = range(n_wires), normalize = True)
        # qml.Barrier()
        
    # 2. Correlation: Amplitude Un-Embedding
    for i in range(2):
        qml.adjoint(
            qml.AmplitudeEmbedding(b, wires = range(n_wires), normalize = True)
        )
        # qml.Barrier()
        for j in range(n_wires):
            qml.H(j)
    
    return qml.probs(wires = range(n_wires))

# Amplitude Encoding overlap [Figure S.5B]
# the fidelity is the probability of the 0 state
def circuit_amp_iamp_qft_canonical(a, b):
    """
    Drawing
    0: ──H─╭|Ψ⟩─╭QFT──H─╭|Ψ⟩─╭QFT─╭QFT†─╭|Ψ⟩†──H─╭QFT†─╭|Ψ⟩†──H─┤ ╭Probs
    1: ──H─├|Ψ⟩─├QFT──H─├|Ψ⟩─├QFT─├QFT†─├|Ψ⟩†──H─├QFT†─├|Ψ⟩†──H─┤ ├Probs
    2: ──H─├|Ψ⟩─├QFT──H─├|Ψ⟩─├QFT─├QFT†─├|Ψ⟩†──H─├QFT†─├|Ψ⟩†──H─┤ ├Probs
    3: ──H─╰|Ψ⟩─╰QFT──H─╰|Ψ⟩─╰QFT─╰QFT†─╰|Ψ⟩†──H─╰QFT†─╰|Ψ⟩†──H─┤ ╰Probs
    """
    la, lb = len(a), len(b)
    assert la == lb
    # assert power of 2
    n_wires = np.log2(la)
    assert n_wires == int(n_wires)
    n_wires = int(n_wires)
    # print(la, lb)

    def state_prep(data, wires):
        qml.AmplitudeEmbedding(data, wires = wires, normalize = True)
        # qml.Barrier()
        qml.QFT(wires = wires)
        # qml.Barrier()
        
    la, lb = len(a), len(b)
    assert la == lb

    # 1. Data: Amplitude Embedding
    for i in range(2):
        for j in range(n_wires):
            qml.H(j)
        state_prep(a, range(n_wires))

    # 2. Correlation: Amplitude Un-Embedding
    for i in range(2):
        qml.adjoint(state_prep)(b, range(n_wires))
        for i in range(n_wires):
            qml.H(i)
    
    return qml.probs(wires = range(n_wires))

# we can write a more efficient form by eliminate the QFT-iQFT in the middle, these should cancel out
def circuit_amp_iamp_qft(a, b):
    la, lb = len(a), len(b)
    assert la == lb
    # assert power of 2
    n_wires = np.log2(la)
    assert n_wires == int(n_wires)
    n_wires = int(n_wires)
    # print(la, lb)

    # 1. Data: Amplitude Embedding
    for i in range(n_wires): qml.H(i)
    qml.AmplitudeEmbedding(a, wires = range(n_wires), normalize = True)
    qml.QFT(wires = range(n_wires))
    for i in range(n_wires): qml.H(i)
    qml.AmplitudeEmbedding(a, wires = range(n_wires), normalize = True)
    
    # 2. Correlation: Amplitude Un-Embedding
    qml.adjoint(qml.AmplitudeEmbedding(b, wires = range(n_wires), normalize = True))
    for i in range(n_wires): qml.H(i)
    qml.adjoint(qml.QFT(wires = range(n_wires)))
    qml.adjoint(qml.AmplitudeEmbedding(b, wires = range(n_wires), normalize = True))
    for i in range(n_wires): qml.H(i)
    
    return qml.probs(wires = range(n_wires))
    
# Polynomial Embed -> QFT -> SWAP
def circuit_iqpembed_qft_swap(a, b):
    la, lb = len(a), len(b)
    assert la == lb

    # 1. Data: Instantaneous Quantum Polynomial (IQP)
    qml.IQPEmbedding(a, wires=range(la), n_repeats=2)
    qml.IQPEmbedding(b, wires=range(la, la + lb), n_repeats=2)

    # 2. Nonlinear Transform: QFT, DFT
    qml.QFT(wires = range(la))
    qml.QFT(wires = range(la, la + lb))
    # qml.adjoint(qml.QFT(wires = range(la, la + lb))) # iQFT = DFT

    # 3. Correlation: SWAP Test
    for i in range(la):
        qml.CNOT(wires = [i, la + i])
    qml.Barrier()
    for i in range(la + lb):
        qml.H(i)

    return qml.probs(wires = range(la + lb))

# These circuits don't implement SWAP test exactly

# Amplitude Embed -> QFT ->
def circuit_ampembed_something(a, b):
    la, lb = len(a), len(b)
    assert la == lb

    for j in range(la + lb):
        qml.H(j)

    # 1. Data: Amplutide
    qml.AmplitudeEmbedding(a, wires = range(la), normalize = True)

    # 2. Nonlinear Transform: QFT
    qml.QFT(wires = range(la))

    # 3. Correlation: Unembed and uncompute, expecting other data
    qml.adjoint(
        qml.AmplitudeEmbedding(b, wires = range(lb), normalize = True)
    )
    qml.adjoint(
        qml.QFT(wires = range(lb))
    )

    for j in range(la):
        qml.H(j)

    return qml.probs(wires = range(la))

"""
The quantum Fourier transform is the classical discrete Fourier transform applied to the vector of amplitudes of a quantum state
"""