# variables
from os import environ as ENV
TEMP = ENV['HOME'] + '/.cache/'
DATA = '../data/'
FIGS = '../figures/'
DIST = '../data_dist/auditory_cortex_data/'

# our lib
import sys
sys.path.append('../src')
from should_be_stdlib import resample_log

# syslib
import os
from glob import glob

# packages
import numpy as np
import pandas as pd
from scipy.io import loadmat

# convert matlab load to something manageable in python
# things to account for:
#  arrays are 1-indexed
#  arrays gain excess 1-length dimensions (they can be np.squeeze()'d out)
#  cellarrays turn to np.void
#  __variables are metadata (version, platform, ...) and can be excluded
def mat2py(mat):
    if mat.__class__ == dict:
        # remove __ vars
        return {
            k: mat2py(v)
            for (k, v) in mat.items()
            if not k.startswith('__')
        }

    elif mat.__class__ == np.ndarray:
        try:
            # cellarray to dict
            if mat[0].__class__ == np.void:
                return [
                    {
                        name: mm.squeeze()
                        for (name, mm) in zip(
                            m.dtype.names, m
                        )
                    }
                    for m in mat[1:]
                ]

            # drop empty zeroth element
            if mat[0].squeeze().shape == ():
                return mat[1:].squeeze()
        except: pass

        # normal squeeze for 1×N -> N
        return mat2py(mat.squeeze())

    else:
        return mat

# load specific data
def load_set(dataset:str) -> dict:
    return mat2py(loadmat(glob(f'{DIST}/{dataset}/*.mat')[0]))

# load all data in dict
def load_all() -> dict:
    return {
        os.path.basename(os.path.dirname(mat)): mat2py(loadmat(mat))
        for mat in glob(f'{DIST}/*/*.mat')
    }

# put string in appropriate dir (data)
def datapath(dataset:str, name:str) -> str:
    os.makedirs(f'{DATA}/{dataset}/', exist_ok=True)
    return f'{DATA}/{dataset}/{name}'

# put string in appropriate dir (figure)
def figspath(dataset:str, name:str) -> str:
    os.makedirs(f'{FIGS}/{dataset}/', exist_ok=True)
    return f'{FIGS}/{dataset}/{name}'

# make a dataframe
def get_for_planes(datas, indices:range, cols:list[any]|None = None, flat:bool=True) -> pd.DataFrame:
    ans = pd.concat(
        objs = [
            pd.DataFrame(
                data = datas(i),
                columns = cols
            )
            for i in indices
        ],
        keys = [i - min(indices) for i in indices]
    ).rename_axis(['plane', 'idx'])
    if flat:
        ans.reset_index(drop=True, inplace=True)
    return ans

# dataset -> xyz df
def get_xyz(data:dict, flat=True) -> pd.DataFrame:
    return get_for_planes(
        lambda i: np.array([
            data['allxc'][i],
            data['allyc'][i],
            data['allzc'][i],
        ]).squeeze().T,
        range(0, 6),
        ['x', 'y', 'z']
    )
    
# dataset -> tuning curve df
def get_tc(data:dict, flat=True) -> pd.DataFrame:
    return get_for_planes(
        lambda i: data['zStuff'][i]['flatFRA'],
        range(0, 6),
        resample_log([3, 3*2**4], 9).round(1)
    )
    
# dataset -> tuning curve p-value df
def get_tc_p(data:dict, flat=True) -> pd.DataFrame:
    return get_for_planes(
        lambda i: data['zStuff'][i]['pStim'],
        range(0, 6),
        resample_log([3, 3*2**4], 9).round(1)
    )

