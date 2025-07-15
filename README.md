# Quantum State Fidelity for Functional Neural Network Construction

Team Quadrigems:

* Skylar Chan: [schan12@umd.edu](schan12@umd.edu)
* Wilson Smith: [smith@umd.edu](smith@umd.edu)
* Kyla Gabriel: [kyla_gabriel@hms.harvard.edu](kyla_gabriel@hms.harvard.edu)

Challenge Track: [2025](https://web.archive.org/web/20250622115932/https://www.pqic.org/challenge) [PQIC Global Industry Challenge](https://www.pqic.org/challenge) provided by [NeuroQuantum Nexus](https://web.archive.org/web/20250622115008/https://gcell.umd.edu/)

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

## Run the code

**Expected inputs**: download the [mouse auditory cortex dataset](https://gcell.umd.edu/data/Auditory_cortex_data.zip) and modify the recording path in `neurodata.py`.

Then run the following notebooks in this order:

1. [final_preprocessing](/notebooks/final_preprocessing.ipynb): preprocess the mouse brain neuron data
2. [final_prepare_quantum_circuits](/notebooks/final_prepare_quantum_circuits.ipynb): create the parameterized quantum circuits
3. [final_make_mitiq_circuits](/mitigation/final_make_mitiq_circuits.ipynb): create error-mitigated versions (use separate environment or temporarily downgrade numpy)
4. [final_simulated_circuits](/notebooks/final_simulated_circuits.ipynb): simulate circuits
5. [jobs_ibmq](/notebooks/jobs_ibmq.ipynb): submit everything to run on IBMQ. If you don't have an API key, you can reuse our IBM results inside `data/results_ibm-kingston.xlsx`.
6. [final_correlation_analysis](/notebooks/final_correlation_analysis.ipynb): correlation analysis
7. [final_functional_network_analysis](/notebooks/final_functional_network_analysis.ipynb): functional network analysis

**Expected outputs**: the figures inside the figures directory and in the correlation analysis and functional network analysis show the constructed networks, similarity comparisons, 3-D distance calculations, and measures of neural activity.

## QPU runs

Run the following circuits with and without error mitigation on IBM hardware:

- Angle embedding (no QFT) + swap test
- Amplitude embedding + compute/uncompute
- Amplitude embedding & QFT + compute/uncompute

For error mitigation on IBM, an implementation to use Mitiq for DDD mitigation with XYXY pulse trains is provided.

Note that other quantum platforms (eg IonQ, IQM) may work, but are unimplemented and untested.


## Licensing

All code is 'All Rights Reserved' by the respective authors until further notice.

Exceptions:
- GPL-3.0: `rentian_scaling`, which comes from [`bctpy`](//github.com/aestrivex/bctpy)
- AGPL-3.0: `small_world_propensity`, which comes from [`small_world_propensity`](//github.com/rkdan/small_world_propensity)

## Acknowledgements

We would like to thank Maya Ma and Shiraz Robinson II for their brainstorming in initial phases of this challenge.