# Quantum State Fidelity for Functional Neural Network Construction

Team Quadrigems:

* Skylar Chan: [schan12@umd.edu](schan12@umd.edu)
* Wilson Smith: [smith@umd.edu](smith@umd.edu)
* Kyla Gabriel: [kyla_gabriel@hms.harvard.edu](kyla_gabriel@hms.harvard.edu)

Challenge Track: [2025](https://web.archive.org/web/20250622115932/https://www.pqic.org/challenge) [PQIC Global Industry Challenge](https://www.pqic.org/challenge) provided by [NeuroQuantum Nexus](https://web.archive.org/web/20250622115008/https://gcell.umd.edu/)

This project recieved [2nd place (Runner-up)](//www.quantumworldcongress.com/news-and-updates/quantum-world-congress-2025-celebrates-global-industry-challenge-winners#:~:text=Quadrigems) in the PQIC GIC!

- **Challenge**: Analyze high-dimensional neural data with quantum computers 🧠💻⚛️
- **Solution**: Quantum hybrid algorithms for neuron clustering 💡⚛️⚙️
- **Key Finding**: Quantum state fidelity complements classical fidelity 🤝📊🎖️
- **Impact**: Accelerates discovery and innovation in: ↗️🚀️📈
  - Neuroscience research 🧪
  - Healthcare 🩺️
  - Brain-Computer Interfaces (BCIs) 🤖️
  - Neuro-prosthetics 🦾️
  - Wetware 🧮️
  - ~~Neuro-gaming 🧠🎮️~~

## Abstract

Neuroscientists face challenges analyzing high-dimensional neural recording data of dense functional networks. To manage computational complexity, researchers use neuron clustering to identify important subnetworks. Without ground-truth reference data, finding the best algorithm for recovering neurologically relevant networks remains an open question. In this paper, we implement and survey quantum hybrid algorithms to construct functional networks, and benchmark them against documented classical techniques. We demonstrate that quantum state fidelity can provide a competitive alternative to classical metrics, revealing distinct functional networks while maintaining neurological relevance. Our findings highlight quantum computing's potential to advance neuroscientific analysis and transform methodological approaches in neurological research and healthcare, including brain-computer interfaces and neuro-prosthetics.

## Set-up Instructions

Please click on the "Launch on qBraid" button to get started. This will clone the repository to qBraid:
[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/0mWh/pqic-gic-quadrigems.git)

Alternatively, clone this repository locally and install dependencies listed in [the project config](/pyproject.toml).

### Project Structure

- `api-keys/`
  - `IBM_API_KEY` your API key for IBMQ, plain text, first line.
  - `IBM_CRN` IBM CRN, plain text, first line
- `pqic-gic-quadrigems/`
  - `data_dist/` where data should be downloaded and extracted. see `url.txt`
  - `notebooks/` main notebook files. see below for instructions.
  - `mitigation/` mitiq project environment directory. (numpy version conflict)
  - `src/` plain python scripts, included by the notebooks.
  - `data/` generated data output.
  - `figures/` generated figures.
  - `*_unused/` anything not used in the main workflow.
  - `pyproject.toml` the dependencies. can be used with [uv](//docs.astral.sh/uv/).
  - `README.md` this file 😁️

## Run the code

**Expected inputs**:
- Download the [mouse auditory cortex dataset](https://gcell.umd.edu/data/Auditory_cortex_data.zip) and extract it as [`data_dist/auditory_cortex_data`](/data_dist/), or modify the recording path in [`neurodata.py`](/src/neurodata.py). The preprocessed data is also available as [tuning-curves_resampled](/data/081920_355r_p0.01/data_tuning-curves_resampled.csv) and [tuning-curves_rescaled](/data/081920_355r_p0.01/data_tuning-curves_rescaled.csv).
- An IBM API key is needed to reproduce the QPU results. Put the API key into a file at `../api-keys/IBM_API_KEY` and the CRN into `../api-keys/IBM_CRN`, or modify the path to the file in [jobs_ibmq](/notebooks/5_circuit_ibmq.ipynb). If you don't have an API key, you can reuse our results from [IBM Kingston](/data/081920_355r_p0.01/results_ibm-kingston.xlsx).

**Run the following notebooks in this order:**

1. [preprocessing](/notebooks/1_preprocessing.ipynb): preprocess the mouse brain neuron data
2. [classical](/notebooks/2_classical.ipynb): classical neural distance metrics
3. [circuit_prepare](/notebooks/3_circuit_prepare.ipynb): create the parameterized quantum circuits for each algorithm  
   - optional: [make_mitiq_circuits](/mitigation/3b_make_mitiq_circuits.ipynb): create error-mitigated versions for running on a QPU. Use a separate environment or temporarily downgrade numpy to v1 to use mitiq. Otherwise the mitigated circuits in Qasm2 format are available in `data/circuits_*.xlsx`.
4. [circuit_simulate](/notebooks/4_circuit_simulate.ipynb): simulate circuits with [Pennylane Lightning Catalyst](//github.com/PennyLaneAI/catalyst). If the Catalyst JIT compiler does not work due to dependency, environment PATH, or unsupported compiler operations, the `qjit` wrapper function can be omitted to use software devices without JIT.
5. [circuit_ibmq](/notebooks/5_circuit_ibmq.ipynb): submit everything to run on IBMQ
6. [circuit_stats](/notebooks/6_circuit_stats.ipynb): calculate statistics about the circuits that were executed.
7. [analysis](/notebooks/7_analysis.ipynb): analysis of the metrics and their correlations
8. [fnn](/notebooks/8_fnn.ipynb): analysis of the constructed functional neural network

**Expected outputs**:   
- figures inside the `figures/` subdirectory:
  - general analysis
    - similarity tests between metrics
  - functional neural networks
    - constructed networks by metric
    - 3-D distance calculations
    - measures of neural structure and organization
- data inside the `data/` subdirectory:
  - reprocessed tuning curve data
  - neuron correlation score matrices (upper triangular)
  - quantum circuits

## QPU runs

Run the following circuits with and without error mitigation on IBM hardware:

- Angle embedding + swap test
- Amplitude embedding + compute/uncompute
- Amplitude embedding & QFT + compute/uncompute

For error mitigation on IBM, an implementation to use [Mitiq for DDD mitigation](//mitiq.readthedocs.io/en/stable/guide/ddd.html) with XYXY pulse trains is provided.

Note that other quantum platforms (eg IonQ, IQM) may work, but are unimplemented and untested.

## Licensing

All code is 'All Rights Reserved' by the respective authors until further notice.

Exceptions:
- GPL-3.0: `rentian_scaling`, which comes from [`bctpy`](//github.com/aestrivex/bctpy)
- AGPL-3.0: `small_world_propensity`, which comes from [`small_world_propensity`](//github.com/rkdan/small_world_propensity)

## Acknowledgements

We would like to thank Maya Ma and Shiraz Robinson II for their brainstorming in initial phases of this challenge.