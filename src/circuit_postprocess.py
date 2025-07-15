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
		for si, ti in zip(range(0,size), range(size,size+size))
	)

def swap_expectation(ans, size:int=9) -> tuple[Float,Float]:
	''' Convert measurement into ⟨SWAP⟩ and overlap |⟨φ(y)|φ(x)⟩|². '''

	def swap_expectation_list(arr:npt.NDArray[Float]) -> tuple[Float,Float]:
		''' ans = [probabilities...] '''
		t = swap_expectation_table(size)
		exp = np.sum(t * arr)
		return exp, (1+exp)/2
	
	def swap_expectation_dict(arr:dict[str,Float]) -> tuple[Float,Float]:
		''' ans[bitstring] = probability '''
		probs = np.zeros((2**(size+size),))
		probs[[tuple(arr.keys())]] = list(arr.values())
		# if any(v>1 for v in probs):
		if any(probs > 1):  # np array, rescale if needed
			probs /= (2**(size+size))
		return swap_expectation_list(probs)

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
	counts = np.array(counts)
	total = np.sum(counts)
	exp_swap = 0.0
	e_values = []
	for bitstring, freq in zip(bitGen(n_pairs*2), counts):
		m = 0								 # number of |11⟩ pairs
		for i in range(n_pairs):
			if bitstring[i] == '1' and bitstring[n_pairs+i] == '1':
				m += 1
		eigenvalue = (-1)**m
		exp_swap  += eigenvalue * freq / total
		e_values.append(eigenvalue)
	fidelity = (1.0 + exp_swap) / 2.0
	return np.array(e_values), exp_swap, fidelity