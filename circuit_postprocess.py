def swap_expectation(counts:dict[str,int]|list[int], size:int=9) -> tuple[float,float]:
	"""
	Turn raw measurement `counts` into	⟨SWAP⟩	and overlap |⟨φ(y)|φ(x)⟩|².
	counts:
		counts[bitstring] = frequency
		counts = [all frequencies...]
	= ⟨SWAP⟩, overlap
	"""

	if isinstance(counts, dict):
		total = sum(counts.values())
		f = sum(
			(-1) ** sum(
				int(si) * int(ti)
				for ti, si in zip(bitstring[:size], bitstring[size:])
			) * freq / total
			for bitstring, freq in counts.items()
		)
	
	else:
		total = sum(counts)
		f = sum(
			(-1) ** sum(
				((i & 1<<si)>>si) * ((i & 1<<ti)>>ti)
				for si, ti in zip(range(size), range(size+1,size+size))
			) * freq / total
			for i, freq in enumerate(counts)
		)
	
	fidelity = (1+f)/2
	
	return f, fidelity

def swap_expectation_og(counts, n_pairs=9):
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