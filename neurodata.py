from os import environ as ENV

import scipy
from scipy import stats

import pandas as pd
import numpy as np

# monkeypatch: statsmodels with scipy>=1.16.0
# scipy._lib.{_util._lazywhere -> array_api_extra.apply_where}
#  scipy._lib._util._lazywhere:
#  - https://pydocs.github.io/p/scipy/1.8.0/api/scipy._lib._util._lazywhere.html
#  @ https://github.com/scipy/scipy/commit/0a315773203ce8e20cad3e800f82b2beaef26bdf#diff-d28fbb0be287769c763ce61b0695feb0a6ca0e67b28bafee20526b46be7aaa84L21-L75
#  scipy._lib.array_api_extra.apply_where
#  + https://data-apis.org/array-api-extra/generated/array_api_extra.apply_where.html
#  @ https://github.com/data-apis/array-api-extra/blob/de481f2cac821c2db7ab2a45b83ed29963c2e1eb/src/array_api_extra/_lib/_funcs.py#L62
import scipy._lib._util
scipy._lib._util._lazywhere = \
    lambda cond, arrays, f, fillvalue=None, f2=None: \
    scipy._lib.array_api_extra.apply_where(cond, arrays, f, f2=f2, fill_value=fillvalue)

import statsmodels.api as sm
import statsmodels


DEFAULT_RECORD = ENV['HOME'] + '/work/auditory_cortex_data/081920_355r/allPlanesVariables27-Feb-2021.mat'

def load_record(path):
	record = scipy.io.loadmat(path)
	return record

def get_tuning_curves(record):
	tuning_curves = pd.concat(
		[
			pd.DataFrame(record['zStuff'][0][plane][0])
			for plane in range(1,6)
		]
	).reset_index().drop(columns='index')
	return tuning_curves

def get_sig_neurons(record, p = 0.01):
	pstim = pd.concat(
		[
			pd.DataFrame(record['zStuff']['pStim'][0][plane])  # takes pval of every frequency
			for plane in range(1,6)
		]
	).reset_index().drop(columns='index')

    # neurons are significant if *any* frequency is significant. use p-value in the *paper* not the *data*
	pstim_is_sig = pstim.replace(np.nan, 1).map(lambda x: 1 if x < p else 0)	 

	pstim_total_sig = pstim_is_sig.T.sum().T

	neurons_sig = pstim_total_sig[pstim_total_sig > 0].index
	# neurons_notsig = pstim_total_sig[pstim_total_sig == 0].index
	return neurons_sig # , neurons_notsig

def get_coords(record):
	xs = pd.concat([pd.DataFrame(record['allxc'][plane][0]) for plane in range(1,6)]).rename(columns={0: 'x'}).reset_index().drop(columns='index')
	ys = pd.concat([pd.DataFrame(record['allyc'][plane][0]) for plane in range(1,6)]).rename(columns={0: 'y'}).reset_index().drop(columns='index')
	zs = pd.concat([pd.DataFrame(record['allzc'][plane][0]) for plane in range(1,6)]).rename(columns={0: 'z'}).reset_index().drop(columns='index')
	coords = pd.concat([xs, ys, zs], axis=1)
	return coords

# This function is licensed under GPL-3.0 to respect the original license from bctpy @ https://github.com/aestrivex/bctpy.
def rentian_scaling(A, xyz, n, seed=42):
    """
    An updated Rentian Scaling function from bctpy, which makes random sized cubes at random positions.

    """
    rng = np.random.default_rng(seed)
    m = np.size(xyz, axis=0)  # find number of nodes in system

    # rescale coordinates so they are all greater than unity
    xyzn = xyz - np.tile(np.min(xyz, axis=0) - 1, (m, 1))

    # find the absolute minimum and maximum over all directions
    nmax = np.max(xyzn)
    nmin = np.min(xyzn)

    count = 0
    N = np.zeros((n,))
    E = np.zeros((n,))

    # create partitions and count the number of nodes inside the partition (n)
    # and the number of edges traversing the boundary of the partition (e)
    while count < n:
        # define cube endpoints
        randx = np.sort((nmax - nmin) * rng.random((2,)))
        randy = np.sort((nmax - nmin) * rng.random((2,)))
        randz = np.sort((nmax - nmin) * rng.random((2,)))

        # ensure cube is within network boundaries
        randx[0] = max(randx[0], nmin)
        randx[1] = min(randx[1], nmax)
        randy[0] = max(randy[0], nmin)
        randy[1] = min(randy[1], nmax)
        randz[0] = max(randz[0], nmin)
        randz[1] = min(randz[1], nmax)

        # find nodes in cube
        l1 = xyzn[:, 0] > randx[0]
        l2 = xyzn[:, 0] < randx[1]
        l3 = xyzn[:, 1] > randx[0]
        l4 = xyzn[:, 1] < randx[1]
        l5 = xyzn[:, 2] > randx[0]
        l6 = xyzn[:, 2] < randx[1]

        L, = np.where((l1 & l2 & l3 & l4 & l5 & l6).flatten())
        if np.size(L):
            # count edges crossing at the boundary of the cube
            E[count] = np.sum(A[np.ix_(L, np.setdiff1d(range(m), L))])
            # count nodes inside of the cube
            N[count] = np.size(L)
            count += 1

    return N, E


def rent_exp(A, coords, M=20):
    """
    Compute Rent's exponent with robust fit method
    """
    # M = 1000  # number of partitions, if we have at least M more than neurons, then each partition has about 1 neuron

    N, E = rentian_scaling(A, coords.to_numpy(), M, seed=42)
    # recommended step is to prune partitions with N < M/2
    N_prime = N # [N < M/2]
    E_prime = E # [N < M/2]

    # Log-log transformation
    log_N_prime = np.log10(N_prime)
    log_E_prime = np.log10(E_prime)

    # Add a constant (intercept) to the independent value
    log_N_prime = sm.add_constant(log_N_prime)

    # Fit the robust linear model
    model = sm.RLM(log_E_prime, log_N_prime, M=statsmodels.robust.norms.TukeyBiweight()) # , M=sm.robust.norms.HuberT())
    results = model.fit()

    # The Rent's exponent is the coefficient of the slope
    rent_exponent = results.params[1]
    print("Rent's exponent:", rent_exponent)

    # Standard error of the estimation
    std_error = results.bse[1]
    print("Standard error of the estimation:", std_error)
    return rent_exponent, std_error

from sklearn.metrics import r2_score
import numpy as np
from scipy.optimize import curve_fit

def is_rentian_scaling(A, coords, M = 20):
    
    # Define the power law function
    def power_law(x, a, b):
        return a * x**b
    
    # Define the exponential law function
    def exponential_law(x, a, b):
        return a * np.exp(b * x)
    
    N, E = rentian_scaling(A, coords.to_numpy(), M)
    X, Y = N, E
    
    # Fit the power law
    popt_power, pcov_power = curve_fit(power_law, X, Y)
    y_fit_power = power_law(X, *popt_power)
    
    # Fit the exponential law
    popt_exponential, pcov_exponential = curve_fit(exponential_law, X, Y)
    y_fit_exponential = exponential_law(X, *popt_exponential)

    # Calculate the R^2 values
    r2_power = r2_score(Y, y_fit_power)
    r2_exponential = r2_score(Y, y_fit_exponential)
    
    print("Power law R^2: {:.2f}".format(r2_power))
    print("Exponential law R^2: {:.2f}".format(r2_exponential))
    if r2_power > r2_exponential:
        print('Rentian scaling achieved')
    else:
        print('Rentian scaling not achieved')
    return r2_power, r2_exponential
