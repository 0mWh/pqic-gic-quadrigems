# Quadrigems
## Quantum Similarity Metrics for Functional Neural Network Construction

###### QSM for FNNC

[Skylar Chan](schan12@umd.edu),
[Wilson Smith](smith@umd.edu),
[Kyla Gabriel](kyla_gabriel@hms.harvard.edu),

Contestant research in the [2025](https://web.archive.org/web/20250622115932/https://www.pqic.org/challenge) [PQIC Global Industry Challenge](https://www.pqic.org/challenge) provided by [NeuroQuantum Nexus](https://web.archive.org/web/20250622115008/https://gcell.umd.edu/)



## Instructions

First run final_preprocessing.ipynb

Then run final_simulated_circuits.ipynb

Then run final_analysis.ipynb

Then run final_graph_contruction.ipynb

## QPU runs

Run the following circuits with and without error mitigation: (IonQ + IBM + IQM).

- Angle embedding (no QFT) + swap test
- Amplitude embedding + compute/uncompute
- Amplitude embedding & QFT + compute/uncompute

For error mitigation on IBM/IQM, use Mitiq with XYXY canceling sequence.