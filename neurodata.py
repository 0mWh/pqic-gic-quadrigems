from os import environ as ENV

import scipy
import pandas as pd
import statsmodels
import numpy as np

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
			pd.DataFrame(record['zStuff']['pStim'][0][plane])
			for plane in range(1,6)
		]
	).reset_index().drop(columns='index')

	pstim_is_sig = pstim.replace(np.nan, 1).map(lambda x: 1 if x < p else 0)	 # what p-value threshold should we use?

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

# tuning_curves = pd.concat(
# 	[
# 		pd.DataFrame(record['zStuff'][0][plane][0])
# 		for plane in range(1,6)
# 	]
# ).reset_index().drop(columns='index')

# ## SIGNIFICANT NEURONS
# pstim = pd.concat(
# 	[
# 		pd.DataFrame(record['zStuff']['pStim'][0][plane])
# 		for plane in range(1,6)
# 	]
# ).reset_index().drop(columns='index')

# pstim_is_sig = pstim.replace(np.nan, 1).map(lambda x: 1 if x < 0.01 else 0)	 # what p-value threshold should we use?

# pstim_total_sig = pstim_is_sig.T.sum().T

# neurons_sig = pstim_total_sig[pstim_total_sig > 0].index
# neurons_notsig = pstim_total_sig[pstim_total_sig == 0].index

# # only focus on significant neurons

# ## COORDINATES
# xs = pd.concat([pd.DataFrame(record['allxc'][plane][0]) for plane in range(1,6)]).rename(columns={0: 'x'}).reset_index().drop(columns='index')
# ys = pd.concat([pd.DataFrame(record['allyc'][plane][0]) for plane in range(1,6)]).rename(columns={0: 'y'}).reset_index().drop(columns='index')
# zs = pd.concat([pd.DataFrame(record['allzc'][plane][0]) for plane in range(1,6)]).rename(columns={0: 'z'}).reset_index().drop(columns='index')
# coords = pd.concat([xs, ys, zs], axis=1)

# # neurons_sig, neurons_notsig
# # SAVE THESE VALUES

# # use a single recording
# def get_tuning_curve(i):
# 	return tuning_curves.loc[i]

# def get_coords(i):
# 	return coords.loc[i]