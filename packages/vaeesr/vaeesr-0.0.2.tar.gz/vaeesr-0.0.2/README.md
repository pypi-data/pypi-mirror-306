# Variational Autoencoder Embeddings Symbolic Regression (VAEESR)

This Python package performs Symbolic Regression by creating an Embedding where semantically similar equations are close to each other and it uses MCMC sampling to find the equation that is the closest to the observed data. Therefore, it uses three main functions: 

1. `create_dataset` which creates a customizable dataset that can be adjusted for the specific problem at hand. The main parameters are: The x_values for which the functions are evaluated, the range of constants, the maximum tree depth, the possible operators and functions, and the total number of equations in the dataset.

2. `create_autoencoder` which trains an autoencoder with the dataset. Some hyperparameters can be adjusted as well. 

3. `perform_MCMC` which performs the symbolic regression by sampling equations from the autoencoder embedding. 

## Install 
`pip install vaeesr`

## Tutorial
The `demo.ipynb` contains a detailed tutorial for using the package. It also includes some helper functions for the visualization and evaluation of the results.
