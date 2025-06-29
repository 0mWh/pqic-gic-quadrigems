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
