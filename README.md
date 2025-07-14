# Quantum State Fidelity for Functional Neural Network Construction

###### QSM for FNNC
Team Quadrigems:
* Skylar Chan: [schan12@umd.edu](schan12@umd.edu),
* Wilson Smith: [smith@umd.edu](smith@umd.edu),
* Kyla Gabriel: [kyla_gabriel@hms.harvard.edu](kyla_gabriel@hms.harvard.edu)

Challenge Track: [2025](https://web.archive.org/web/20250622115932/https://www.pqic.org/challenge) [PQIC Global Industry Challenge](https://www.pqic.org/challenge) provided by [NeuroQuantum Nexus](https://web.archive.org/web/20250622115008/https://gcell.umd.edu/)


## Set-up Instructions
Please click on the "Launch on qBraid" button to get started.   
[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/0mWh/pqic-gic-quadrigems.git)

Run the following notebooks in order:
1. [final_preprocessing](/notebooks/final_preprocessing.ipynb)
2. [final_simulated_circuits](/notebooks/final_simulated_circuits.ipynb)
3. [final_analysis](/notebooks/final_analysis.ipynb)
4. [final_graph_contruction](/notebooks/final_graph_contruction.ipynb)


## QPU runs
Run the following circuits with and without error mitigation: (IonQ + IBM + IQM).

- Angle embedding (no QFT) + swap test
- Amplitude embedding + compute/uncompute
- Amplitude embedding & QFT + compute/uncompute

For error mitigation on IBM/IQM, use Mitiq with XYXY canceling sequence.


## Descriptions
- [notebooks/final_prepare_quantum_circuits](/notebooks/final_prepare_quantum_circuits.ipynb): generate the QASM2 string for our circuits
- [mitigation/final_make_mitiq_circuits](/mitigation/final_make_mitiq_circuits.ipynb): read in QASM2 strings and apply mitigation with [Mitiq](https://github.com/unitaryfoundation/mitiq)
- [notebooks/jobs_ibmq](/notebooks/jobs_ibmq.ipynb): submit jobs on [IBMQ](https://quantum.ibm.com/). save results

## Acknowledgements

We would like to thank Maya Ma and Shiraz Robinson II for their brainstorming in initial phases of this challenge.