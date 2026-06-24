# SpecificityStudio

<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/d4003c0b-5668-479b-8adc-627b9fd857f8" />

Code for the benchmark dataset for understanding how different protein fitness models score and design variants of altered specificity and to reproduce all analyses in the paper "Differences between protein fitness models can be used to design variants of altered specificity" by Samuel P Berry, Rachelle Gaudet and Debora S Marks.

All main text figures and analyses can be found under Notebooks/, as can individual .ipynb notebooks for processing assay data.

Scripts for scoring models can be found in scripts/ and within the cloned ProteinGym repository (the identities of the .py scripts from ProteinGym are called from within the .sh wrappers in scripts/)

## Required packages
The analysis of the data requires only standard scientific python packages: numpy, pandas, sklearn, matplotlib, and seaborn.
For running the individual models, see the ProteinGym repo: https://github.com/OATML-Markslab/ProteinGym.

## Questions
This benchmark is still in development. If you have questions or feedback, please reach out to me (Sam) at my current email address, sb84@sanger.ac.uk.
