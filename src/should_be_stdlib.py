import numpy as np
from numpy import typing as npt

# a < b?
def is_array_lesser_list(a: list, b: list) -> bool:
    for i, (ai, bi) in enumerate(zip(a, b)):
        if ai < bi:
            return True
        if ai > bi:
            return False
    return False

# a < b?
def is_array_lesser(a: npt.NDArray[any], b: npt.NDArray[any]) -> np.bool:
    return np.all(a < b) or (np.any(a < b) and np.all(a == b))

# sort (a, b)
def small_then_big_array(a: list, b: list) -> tuple[list, list]:
    if is_array_lesser(b, a):
        return b, a
    else:
        return a, b

# turn triangular matrix into square
def mirror_matrix(mat: npt.NDArray[any]) -> npt.NDArray[any]:
    mirror = mat.copy()
    mirror[np.isnan(mirror)] = mirror.T[np.isnan(mirror)]
    return mirror

# make hollow matrix (zero diagonal) - useful for mantel test
def hollow_matrix(mat: npt.NDArray[any]) -> npt.NDArray[any]:
    hollow = mat.copy()
    np.fill_diagonal(hollow, 0)
    return hollow

# linear space resampling
def resample(data: npt.NDArray[any], n_out: int) -> npt.NDArray[any]:
    def scale(left, right, i):
        return left * (1 - i) + right * i

    t = np.linspace(0, len(data) - 1, num=n_out)
    data = np.array(data)
    return scale(data[np.floor(t).astype(np.int_)], data[np.ceil(t).astype(np.int_)], t % 1)

# logarithmic space resampling
def resample_log(data: npt.NDArray[any], n_out: int) -> npt.NDArray[any]:
    return 2 ** resample(np.log2(data), n_out)

# divy list into blocks of size
def chunk(arr: list[any], chunk_size: int) -> dict[int, list[any]]:
    try:  # py > 3.11
        from itertools import batched

        generator = batched(arr, chunk_size)
    except ImportError:
        generator = (arr[i : min(len(arr), i + chunk_size)] for i in range(0, len(arr), chunk_size))
    return dict(enumerate(generator))

# really user-friendly double-confirmation
def verify_run(string: str = 'REALLY', throw: bool = False):
    ans = input(f'You must type "{string}" to run this because it may cost a lot of money!!! >>> ')
    bad = f'By not typing "{string}", you did not run this code'
    if ans != string:
        if throw:
            raise ValueError(bad)
        else:
            print(bad)
        return False
    ans = input(f'If you are really sure you want to run this code, type "{string}" to proceed >>> ')
    if ans != string:
        if throw:
            raise ValueError(bad)
        else:
            print(bad)
        return False
    return True

# get a list of keys from a dict
def dict_get(d: dict[any, any], keys: list[any], default: any = None) -> list[any]:
    return [d.get(k, default) for k in keys]
