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

def resample(data:npt.NDArray[any], n_out:int) -> npt.NDArray[any]:
	scale = lambda l,r,i: l*(1-i) + r*i
	t = np.linspace(0, len(data)-1, num=n_out)
	data = np.array(data)
	return scale(
		data[np.floor(t).astype(np.int_)],
		data[np.ceil(t).astype(np.int_)],
		t % 1
	)

def resample_log(data:npt.NDArray[any], n_out:int) -> npt.NDArray[any]:
	return 2 ** resample(np.log2(data), n_out)