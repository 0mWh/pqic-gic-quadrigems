from os import environ as ENV

import numpy as np
import numpy.typing as npt
Float = np.float64

import diskcache as dc
cache = dc.Cache(
    ENV['HOME'] + '/.cache/postprocess/', # this longevity does not matter
    size_limit = 2 ** 32, # 4GB
)

@cache.memoize()
def swap_expectation_table(size:int=9) -> npt.NDArray[Float]:
	# (-1) ** sum(s_i * t_i)
	return (-1) ** sum(
		((np.indices((2**(size+size),)) & (1<<si)) >> si)
		*
		((np.indices((2**(size+size),)) & (1<<ti)) >> ti)
		for si, ti in zip(range(size), range(size+1,size+size))
	)

def swap_expectation(ans, size:int=9) -> tuple[Float,Float]:
	''' Convert measurement into ⟨SWAP⟩ and overlap |⟨φ(y)|φ(x)⟩|². '''

	def swap_expectation_list(probs:npt.NDArray[Float]) -> tuple[Float,Float]:
		''' counts = [probabilities...] '''
		t = swap_expectation_table(size)
		f = np.sum(t * probs)
		return f, (1+f)/2
	
	def swap_expectation_dict(counts:dict[str,Float]) -> tuple[Float,Float]:
		''' counts[bitstring] = frequency '''
		probs = np.zeros((2**(size+size),))
		probs[[tuple(counts.keys())]] = list(counts.values())
		return swap_expectation_list(probs, size)

	if isinstance(ans, dict):
		return swap_expectation_dict(ans)
	else:
		return swap_expectation_list(ans)

def swap_expectation_og(counts:dict[str,int], n_pairs:int=9) -> tuple[float,float]:
    """
    Turn raw measurement `counts` into  ⟨SWAP⟩  and overlap |⟨φ(y)|φ(x)⟩|².
    counts  : dict  bitstring -> frequency   (keys length = 2*n_pairs)
    Returns : (⟨SWAP⟩,  fidelity_estimate)
    """
    total = sum(counts.values())
    exp_swap = 0.0
    for bitstring, freq in counts.items():
        # Qiskit prints qubits little-endian; reverse to pair them as (s_i,t_i)
        # bits = bitstring[::-1]
        m = 0                                 # number of |11⟩ pairs
        for i in range(n_pairs):
            if bits[i] == '1' and bits[n_pairs+i] == '1':
                m += 1
        eigenvalue = (-1)**m
        exp_swap  += eigenvalue * freq / total
    fidelity = (1.0 + exp_swap) / 2.0
    return exp_swap, fidelity