from setuptools import setup, find_packages

VERSION = '0.0.2'

DESCRIPTION = 'Using the latent space of a variational autoencoder to perform symbolic regression by sampling equations.'
LONG_DESCRIPTION = """
Variational Autoencoder Embeddings Symbolic Regression (VAEESR)

This Python package performs Symbolic Regression by creating an Embedding where semantically similar equations are close to each other and it uses MCMC sampling to find the equation that is the closest to the observed data. Therefore, it uses three main functions: 

1. `create_dataset` which creates a customizable dataset that can be adjusted for the specific problem at hand. The main parameters are: The x_values for which the functions are evaluated, the range of constants, the maximum tree depth, the possible operators and functions, and the total number of equations in the dataset.

2. `create_autoencoder` which trains an autoencoder with the dataset. Some hyperparameters can be adjusted as well. 

3. `perform_MCMC` which performs the symbolic regression by sampling equations from the autoencoder embedding. 
"""


#with open("README.md", "r") as f:
 #   LONG_DESCRIPTION = f.read()

# Setting up
setup(
        name="vaeesr", 
        version=VERSION,
        author="Lisa Artmann",
        author_email="lisaartmann01@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'equation-tree',
            'numpy',
            'tqdm',
            'torch',
            'pandas',
            'sympy',
            'scipy',
            'scikit-learn',
            'pyro-ppl',
        ],
        
        keywords=['Symbolic Regression', 'Equation Discovery', 'Variational Autoencoder',],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: MIT License",
            "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]
)