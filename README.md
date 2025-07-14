# Quantum Similarity Metrics for Functional Neural Network Construction

###### QSM for FNNC
Team Quadrigems:
* Skylar Chan: [schan12@umd.edu](schan12@umd.edu),
* Wilson Smith: [smith@umd.edu](smith@umd.edu),
* Kyla Gabriel: [kyla_gabriel@hms.harvard.edu](kyla_gabriel@hms.harvard.edu)

Challenge Track: [2025](https://web.archive.org/web/20250622115932/https://www.pqic.org/challenge) [PQIC Global Industry Challenge](https://www.pqic.org/challenge) provided by [NeuroQuantum Nexus](https://web.archive.org/web/20250622115008/https://gcell.umd.edu/)


## Set-up Instructions
Please click on the "Launch on qBraid" button to get started, then run the following notebooks in the order that it is presented:
<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">

1. final_preprocessing.ipynb
2. final_simulated_circuits.ipynb
3. final_analysis.ipynb
4. final_graph_contruction.ipynb


## QPU runs
Run the following circuits with and without error mitigation: (IonQ + IBM + IQM).

- Angle embedding (no QFT) + swap test
- Amplitude embedding + compute/uncompute
- Amplitude embedding & QFT + compute/uncompute

For error mitigation on IBM/IQM, use Mitiq with XYXY canceling sequence.
