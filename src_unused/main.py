from os import environ as ENV

import numpy as np

import diskcache as dc

cache = dc.Cache(
    ENV['PWD'] + '/.cache/',
    cull_limit=0,
    size_limit=2**32,  # 4GB
    timeout=60**2 * 24 * 7,  # 1 week
)

from qiskit import QuantumCircuit as QC, QuantumRegister as QR, ClassicalRegister as CR

from circuit_components import *
from circuit_pipelines import *
from circuit_postprocess import *

from qiskit_aer import AerSimulator

SIMULATOR = AerSimulator(method='statevector', device='GPU')


@cache.memoize()
def swap_fidelity(recording_path: str, neuron_A: int, neuron_B: int, analytic: bool = True):
    """
    Given 2 neuron indices, it looks up the recording path and returns the state fidelity between 2 neurons
    """
    assert type(neuron_A) is int
    assert type(neuron_B) is int
    assert type(analytic) is bool
    signal_A = neurodata.get_tuning_curve(recording_path, A)
    signal_B = neurodata.get_tuning_curve(recording_path, B)
    if signal_A > signal_B:
        return swap_fidelity(neuron_B, neuron_A)
    elif analytic:
        return analytic_swap_fidelity(signal_A, signal_B)
    else:
        return queue_job(signal_A, signal_B)


# ----- run a quick simulation -----
def analytic_state_fidelity(data1, data2):
    """
    TODO: normalize input data
    """
    # data1 = np.random.uniform(0, 2*np.pi, 9)
    # data2 = np.random.uniform(0, 2*np.pi, 9)

    qc = pipeline_swap_diagonal_test(data1, data2)
    print(qc.draw())
    # qc = qc.decompose()			   # for Aer 0.12+
    # qc.save_statevector()

    # shots = 0
    # TODO: how to use analytic simulation, no shots?
    # compiled_circuit = transpile(qc, backend)

    observable = 'Z' * qc.num_qubits
    estimation = SIMULATOR.run(
        circuits=[qc.decompose()],
        observables=[observable],
    )
    print(estimation)

    pub_result = estimation.result()
    print(pub_result)

    print(f'>>> Expectation value: {pub_result.data.evs}')

    exp_swap, fidelity = swap_expectation(counts)
    # print(f"⟨SWAP⟩  ≈ {exp_swap:.4f}")
    # print(f"|⟨φ(y)|φ(x)⟩|² ≈ {fidelity:.4f}")
    return fidelity


if __name__ == '__main__':
    data1 = [2] * 9
    data2 = [3] * 9
    print(analytic_state_fidelity(data1, data2))
