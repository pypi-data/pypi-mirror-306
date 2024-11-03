import numpy as np

import pyro
import pyro.infer
import pyro.optim
import pyro.poutine as poutine
from pyro.infer import MCMC, NUTS
import pyro.distributions as dist

import torch

from .utils import generate_values, decode_latent_classify, mapping_from_spaces
from .preprocessing import generate_dataset, preprocessing
from .training import training_VAE_C, training_AE_C


def create_dataset(
    spaces = (
        ["sin", "exp", "cos", "sqr", "abs", "acos", "asin", "log"],
        ["+", "-", "*", "/", "min", "max", "**"],
        ["x_1", "x_1", "X"],
        ["c_0"]
        ),
    x_values = np.linspace(-1.0, 1.0, 50),
    max_tree_depth=6, 
    num_equation_samples = 10000, 
    batch_size = 50,
    training_set_proportion = 0.8,
    inf_repacement = 1000,
    is_vae=True
):
    """
    Function to create a dataset

    Parameters:
        spaces (tuple): tuple of lists containing the functions, operators, variables and constants to be used in the equations
        x_values (numpy.array): numpy array of values to be used as input to the equations
        latent_dims (int): number of latent dimensions
        tree_depth (int): maximum depth of the equation trees
        num_equation_samples (int): number of equation samples to be generated
        batch_size (int): batch size for training
        training_set_proportion (int): proportion of the dataset to be used for training
        inf_repacement (int): value to replace infinity in the dataset
        is_vae (int): boolean indicating if the model is a VAE

    Returns: autoencoder, dataset, classes, df_results
    """
    is_function = lambda x: x in spaces[0]
    is_operator = lambda x : x in spaces[1]
    is_variable = lambda x : x in spaces[2]
    is_constant = lambda x : x in spaces[3]
    mapping = (is_function, is_operator, is_variable, is_constant)
    print('Generate Dataset:')
    dataset, max_len, classes, unique_symbols = generate_dataset(spaces, num_equation_samples, max_tree_depth, x_values)

    # create data set
    print('preprocessing...')
    train_loader, test_loader, test_size = preprocessing(dataset, batch_size, training_set_proportion)
    # train model
    return train_loader, test_loader, test_size, dataset, classes, unique_symbols, max_len


def create_autoencoder(
    train_loader,
    test_loader,
    unique_symbols,
    test_size,
    max_len,
    classes,
    latent_dims=4, 
    num_epochs = 500,
    batch_size = 50,
    learning_rate = 0.001,
    kl_weight = 0.0001,
    is_vae=True): 
    """
    Function to create an autoencoder for equations

    Parameters:
        spaces (tuple): tuple of lists containing the functions, operators, variables and constants to be used in the equations
        x_values (numpy.array): numpy array of values to be used as input to the equations
        latent_dims (int): number of latent dimensions
        tree_depth (int): maximum depth of the equation trees
        num_equation_samples (int): number of equation samples to be generated
        num_epochs (int): number of epochs for training
        batch_size (int): batch size for training
        learning_rate (int): learning rate for training
        kl_weight (int): weight of the KL divergence loss
        training_set_proportion (int): proportion of the dataset to be used for training
        inf_repacement (int): value to replace infinity in the dataset
        is_vae (int): boolean indicating if the model is a VAE

    Returns: autoencoder, dataset, classes, df_results
    """
    print('Train model')
    if is_vae:
        autoencoder_equations, df_results = training_VAE_C(train_loader, test_loader, latent_dims, unique_symbols, num_epochs, learning_rate, test_size, kl_weight, classes, max_len, 1.0)
    else:
        autoencoder_equations, df_results = training_AE_C(train_loader, test_loader, latent_dims, unique_symbols, num_epochs, learning_rate, test_size, max_len, classes, 1.0)
    return autoencoder_equations, df_results
    
def perform_MCMC(autoencoder_equations, observed_data, latent_dims, dataset, classes, spaces, x_values, num_samples=1000, num_chains=2, warmup_steps=200): 
    """
    Function to perform MCMC sampling

    Parameters:
        autoencoder_equations (torch.nn.Module): autoencoder model
        observed_data (torch.Tensor): observed data
        latent_dims (int): number of latent dimensions
        dataset (list): list of equations
        classes (list): list of classes
        spaces (tuple): tuple of functions to map the equations
        x_values (numpy.array): numpy array of values to be used as input to the equations
        num_samples (int): number of samples to be generated


    Returns: samples, mcmc
    """
    
    pyro.clear_param_store()
    nuts_kernel = NUTS(probabilistic_model)

    mcmc = MCMC(nuts_kernel, num_samples=num_samples, warmup_steps=warmup_steps, num_chains=num_chains)

    mcmc.run(observed_data, latent_dims, autoencoder_equations, dataset, classes, spaces, x_values)

    samples = mcmc.get_samples()
    return samples, mcmc


def probabilistic_model(data, latent_dims, autoencoder, dataset, classes, spaces, x_values):
    mapping = mapping_from_spaces(spaces)

    latent_variables = []
    for i in range(latent_dims):
        latent_variables.append(pyro.sample(f"latent_variable_{i}", dist.Normal(0, 5)))
    variance = torch.tensor(0.01) * 50

    embedding = [latent_variables]

    equations, constants = decode_latent_classify(autoencoder, dataset, embedding, classes)
    

    try:
        values = generate_values(equations[0], constants[0][0][0], mapping[0], mapping[1], mapping[2], mapping[3], x_values)[1]
        values = torch.nan_to_num(torch.tensor(values, dtype=torch.float32))
    except:
        # TODO handle nan values better
        values = torch.tensor([1000.0]*50, dtype=torch.float32)
        print(values)
        print(type(values))
    #print(f"Equation: {prefix_to_infix(equations[0], is_function, is_operator)}; Constant: {constants[0][0][0]} Distance: {torch.norm(values - data, p=1)}")
    # return pyro.sample("observed_data", dist.Normal(values, variance), obs=data)
    
    pyro.sample(f"observed_data", dist.Normal(values, variance).to_event(1), obs=data)