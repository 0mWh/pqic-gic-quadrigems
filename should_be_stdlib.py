import numpy as np, numpy.typing as npt

def is_array_lesser_list(a:list, b:list) -> bool:
	for i, (ai, bi) in enumerate(zip(a,b)):
		if ai < bi:
			return True
		if ai > bi:
			return False
	return False

def is_array_lesser(a:npt.NDArray[any], b:npt.NDArray[any]) -> np.bool:
	return (
		np.all(a < b) or
		( np.any(a < b) and np.all(a == b) )
	)