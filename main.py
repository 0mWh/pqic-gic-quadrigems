from os import environ as ENV

import numpy as np

import diskcache as dc
cache = dc.Cache(
    ENV['PWD'] + '/.cache/',
    cull_limit = 0,
    size_limit = 2 ** 32, # 4GB
    timeout = 60**2 * 24 * 7, # 1 week
)

from qiskit import (
    QuantumCircuit as QC,
    QuantumRegister as QR,
    ClassicalRegister as CR
)

from qiskit_aer import AerSimulator
SIMULATOR = AerSimulator(method='statevector', device='GPU')

from circuit_components import *
from circuit_pipelines import *


def swap_expectation(counts, n_pairs=9):
    """
    Turn raw measurement `counts` into  ⟨SWAP⟩  and overlap |⟨φ(y)|φ(x)⟩|².
    counts  : dict  bitstring -> frequency   (keys length = 2*n_pairs)
    Returns : (⟨SWAP⟩,  fidelity_estimate)
    """
    total = sum(counts.values())
    exp_swap = 0.0
    for bitstring, freq in counts.items():
        # Qiskit prints qubits little-endian; reverse to pair them as (s_i,t_i)
        bits = bitstring[::-1]
        m = 0                                 # number of |11⟩ pairs
        for i in range(n_pairs):
            if bits[i] == '1' and bits[n_pairs+i] == '1':
                m += 1
        eigenvalue = (-1)**m
        exp_swap  += eigenvalue * freq / total
    fidelity = (1.0 + exp_swap) / 2.0
    return exp_swap, fidelity


# @cache.memoize
def swap_fidelity(recording_path:str, neuron_A:int, neuron_B:int, analytic:bool=True):
    '''
    Given 2 neuron indices, it looks up the recording path and returns the state fidelity between 2 neurons
    '''
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


def queue_job(signal_A, signal_B):
    '''
    TODO
    '''
    return analytic_state_fidelity(signal_A, signal_B)


# ----- run a quick simulation -----
def analytic_state_fidelity(data1, data2):
    '''
    TODO: normalize input data
    '''
    # data1 = np.random.uniform(0, 2*np.pi, 9)
    # data2 = np.random.uniform(0, 2*np.pi, 9)
    
    qc = pipeline_swap_diagonal_test(data1, data2)
    # qc = qc.decompose()              # for Aer 0.12+
    qc.save_statevector()
    
    shots = 2500
    # TODO: how to use analytic simulation, no shots?
    # compiled_circuit = transpile(qc, backend)
    job = SIMULATOR.run(qc).result()
    counts = job.get_counts()
    
    exp_swap, fidelity = swap_expectation(counts)
    # print(f"⟨SWAP⟩  ≈ {exp_swap:.4f}")
    # print(f"|⟨φ(y)|φ(x)⟩|² ≈ {fidelity:.4f}")
    return fidelity

if __name__ == '__main__':
    analytic_state_fidelity()
