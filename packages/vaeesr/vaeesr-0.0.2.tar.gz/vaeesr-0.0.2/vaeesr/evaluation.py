import numpy as np
import pandas as pd

from scipy.spatial import distance_matrix
from scipy.spatial.distance import squareform
from scipy.stats import pearsonr

import pyro.distributions as dist

import torch

from equation_tree import instantiate_constants
from equation_tree.util.conversions import infix_to_prefix, prefix_to_infix
from equation_tree.tree import EquationTree, node_from_prefix

from IPython.utils import io

from sympy import *

from .loss import correlation_coeff
from .utils import try_infix, decode_latent_classify, generate_values, mapping_from_spaces
from .training import  training_AE_C, training_VAE_C

def evaluation(df_results, equation_tree_dataset, max_len, classes):
    x_hat_batches_n = [torch.argmax(batch[0], dim=1).tolist() for batch in df_results["x_hat_batches"]]
    # constants

    for i, batch in enumerate(x_hat_batches_n):
        for j, eq in enumerate(batch):
            x_hat_batches_n[i][j] = classes[eq]

    # concatenate all batches
    x_hat_batches_n = [item for sublist in x_hat_batches_n for item in sublist]
    x_batches_n = [item for sublist in df_results['x_batches'] for item in sublist[0]]
    x_constants = [item for sublist in df_results['x_batches'] for item in sublist[1]]
    # caclulate accuracy
    count = 0
    for rec, real in zip(x_hat_batches_n, x_batches_n):
        if rec == real.tolist():
            count += 1
        else: 
            print(f"rec: {equation_tree_dataset.decode_equation(rec)}, real: {equation_tree_dataset.decode_equation(real)}")

    accuracy = count / (len(x_hat_batches_n))
    #mse_constants = np.mean([np.square(c - c_hat) for c, c_hat in zip(x_constants, x_hat_constants_p)])

    return {
        "Equation reconstruction accuracy": accuracy,
        "Number of equations": len(x_batches_n),
    }

def evaluate_sampling(samples, autoencoder, dataset, classes, latent_dims, spaces, x_values):
    is_function, is_operator, is_variable, is_constant = mapping_from_spaces(spaces)
    results_mcmc = []
    # take just the mean of the samples
    for i in range(latent_dims):
        results_mcmc.append(samples[f'latent_variable_{i}'].mean())

    # sample from the distribution
    results_sampled = []
    for i in range(latent_dims):
        results_sampled.append(dist.Normal(samples[f'latent_variable_{i}'].mean(), samples[f'latent_variable_{i}'].std()).sample())

    # random embedding
    random_samples = []
    for i in range(latent_dims):
        random_samples.append(dist.Normal(0, 5).sample())

    # decode results (take the mean)
    results_dec = decode_latent_classify(autoencoder, dataset, [results_mcmc], classes)
    result_equation = results_dec[0][0]
    result_constant = results_dec[1][0][0][0]

    # decode sampled results
    sampled_dec = decode_latent_classify(autoencoder, dataset, [results_sampled], classes)
    sampled_equation = sampled_dec[0][0]
    sampled_constant = sampled_dec[1][0][0][0]

    # decode random samples
    random_dec = decode_latent_classify(autoencoder, dataset, [random_samples], classes)
    random_equation = random_dec[0][0]
    random_constant = random_dec[1][0][0][0]

    #print(observed_data)
    v_mean = generate_values(result_equation, result_constant, is_function, is_operator, is_variable, is_constant, x_values)
    v_sample = generate_values(sampled_equation, sampled_constant, is_function, is_operator, is_variable, is_constant, x_values)
    v_random = generate_values(random_equation, random_constant, is_function, is_operator, is_variable, is_constant, x_values)
    return (result_equation, result_constant,v_mean), (sampled_equation, sampled_constant, v_sample), (random_equation, random_constant, v_random)





def get_latent_representation(
    model,
    device,
    test_dataloader,
    
    x_batches_p,
    x_hat_batches_p,
    equation_tree_dataset,
    num_interpolations=3,
    results = None,
):
    latent_space_representation = []
    # get random number between 0 and test_size
    test_values = []

    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        for (
            test_equations_batch,
            test_constant_batch,
            test_values_batch,
        ) in test_dataloader:
            test_equations_batch = test_equations_batch.to(device)  #
        
            out = model.encode(test_equations_batch, test_constant_batch)
            if len(out) == 2:
                mean, logvar = out
                z_syntax = model.reparameterize(mean, logvar)
            else:
                z_syntax = out
            # print(z_syntax)
            latent_space_representation.append(z_syntax.cpu().numpy())
            test_values += test_values_batch

    latent_space_representation = np.concatenate(latent_space_representation, axis=0)
    # take only the first two dimensions of the latent space
    lat = latent_space_representation  # [:, :2]

    return latent_space_representation, test_values,

def get_interpolated_df(
    kind,
    model,
    equation_tree_dataset,
    latent_space_representation,
    equation_1,
    equation_2,
    c_1,
    c_2,
    num_interpolations,
    assignment,
    classes = None,):
    is_function, is_operator, is_variable, is_constant = assignment
    # get 2 random vectors from the latent space
    if type(equation_1) == int:
        z1 = np.array(latent_space_representation[equation_1])
        z2 = np.array(latent_space_representation[equation_2])
    else: 
        equation_1 = infix_to_prefix(equation_1, is_function, is_operator)
        equation_2 = infix_to_prefix(equation_2, is_function, is_operator)
        
        if len(equation_1) < 6:
            equation_1 = equation_1 + ["<PAD>"] * (6 - len(equation_1))
        if len(equation_2) < 6:
            equation_2 = equation_2 + ["<PAD>"] * (6 - len(equation_2))
        print(equation_1)
        equation_1 = equation_tree_dataset.encode_equation(equation_1)
        equation_2 = equation_tree_dataset.encode_equation(equation_2)

        encoded_1 = model.encode(torch.tensor([equation_1]), torch.tensor([[c_1]]))
        encoded_2 = model.encode(torch.tensor([equation_2]), torch.tensor([[c_2]]))
        if len(encoded_1) == 2:
            mean1, logvar1 = encoded_1
            mean2, logvar2 = encoded_2
            z1 = model.reparameterize(mean1, logvar1).detach().numpy()
            z2 = model.reparameterize(mean2, logvar2).detach().numpy()
        else:
            z1 = encoded_1.detach().numpy()
            z2 = encoded_2.detach().numpy()
    # generate 3 vectors between z1 and z2
    coords = []
    for i in range(len(z1)):
        l = np.linspace(z1[i], z2[i], num_interpolations + 2, dtype=np.float32)[1:-1]
        coords.append(l)

    # create a list of 3 vectors
    z_list = []
    z_list.append(z1)
    for i in range(num_interpolations):
        z_list.append([coords[k][i] for k in range(len(z1))])
    z_list.append(z2)
    z_list = np.array(z_list)
    if len(z_list.shape) == 3:
        z_list = z_list.squeeze(1)
    if kind == 'regression':
        z_decoded_list, z_decoded_constants = decode_latent(model, equation_tree_dataset, z_list)
    else:
        z_decoded_list, z_decoded_constants = decode_latent_classify(model, equation_tree_dataset, z_list, classes)
    print(f"reconstructed euqation 1: {z_decoded_list[0]}, reconstructed equation 2: {z_decoded_list[-1]}")

    # should I add correct or decoded equations?
    #z_decoded_list[0] = x_decoded_1
    #z_decoded_list[-1] = x_decoded_2

    df = pd.DataFrame(data=z_list[:, :3], columns=["x", "y", "z"])
    df["Category_prefix"] = [str(v) for v in z_decoded_list]
    df["constants"] = [v for v in z_decoded_constants]
    for i in range(len(z_decoded_list)):
        try:
            z_decoded_list[i] = prefix_to_infix(z_decoded_list[i], is_function, is_operator)
        except IndexError as e:
            print(e)
    df["Category"] = [str(v) for v in z_decoded_list]
    return df, z_list



def get_correlation_coefficient(
    latent_space_representation,
    x_decoded,
    is_function,
    is_operator,
    x_constants_p,
    test_values,
    dataset,
):
    # Calculate distance matrices

    df = pd.DataFrame(data=latent_space_representation[:, :3], columns=["x", "y", "z"])
    x_decoded = [dataset.decode_equation(eq) for eq in x_decoded]
    df["Category_prefix"] = [str(eq) for eq in x_decoded]
    df["Category"] = [prefix_to_infix(eq, is_function, is_operator) for eq in x_decoded]
    # replace c_1 with the actual constant
    df["Category"] = [
        eq.replace("c_1", str(round(float(c), 2)))
        for eq, c in zip(df["Category"], x_constants_p)
    ]

    correlation_cor, correlation_dis, _,_ = correlation_coeff(values=torch.stack(test_values)[:,1,:], z=torch.tensor(latent_space_representation))

    distance_matrix_lat = distance_matrix(
        latent_space_representation, latent_space_representation
    )
    distance_df_lat = pd.DataFrame(
        distance_matrix_lat, columns=df["Category"], index=df["Category"]
    )

    test_values_det = np.array([values.detach().numpy() for values in test_values])

    # create distance matrix where the values are the distance between each test values
    distance_matrix_values = np.zeros((len(test_values_det), len(test_values_det)))
    dm_values = np.zeros((len(test_values_det), len(test_values_det)))

    for i in range(len(test_values_det)):
        for j in range(len(test_values_det)):
            if i == j:
                distance_matrix_values[i][j] = 0.0
            else:
                distance_matrix_values[i][j] = np.nan_to_num(
                    np.mean(np.abs(test_values_det[i][1] - test_values_det[j][1]))
                )
                dm_values[i][j] = np.nan_to_num(
                    np.mean(test_values_det[i][1] - test_values_det[j][1])
                )
                # print(test_values_det[i][1])
    distance_matrix_values = np.nan_to_num(distance_matrix_values, posinf=1000, neginf=-1000)
    distance_matrix_lat = np.nan_to_num(distance_matrix_lat, posinf=1000, neginf=-1000)
    distance_df_values = pd.DataFrame(
        distance_matrix_values, columns=df["Category"], index=df["Category"]
    )

    #correlation_coefficient, p_value = pearsonr(
     #   squareform(distance_matrix_lat), squareform(distance_matrix_values)
    #)
    # print(f"Correlation coefficient: {correlation_coefficient}")
    return (
        correlation_cor,
        correlation_dis,
        distance_matrix_lat,
        distance_matrix_values,
        df,
        test_values_det,
        dm_values,
        distance_df_values,
    )
    

def evaluate_different_models(d, batch_size, training_set_proportion, units, num_epochs, learning_rate, kind, weight, klweight = None, classes = None, assignments=None):
    torch.cuda.empty_cache()
    train_data, test_data, test_size = preprocessing(
        dataset=d,
        batch_size=batch_size,
        training_set_proportion=training_set_proportion
    )
    equations = [d.decode_equation(x[0]) for x in d]
    all_symbols = [item for sublist in equations for item in sublist]
    unique_symbols = sorted(list(set(all_symbols)))
    max_len = len(equations[0])
    #try:
    with io.capture_output() as captured:
        if kind == 'VAE':
            model, train_losses, test_losses, correlations_cor, correlations_dis, x_batches, x_hat_batches, df_results = training_VAE(train_data, test_data, units, unique_symbols, num_epochs, learning_rate, test_size, klweight)
        elif kind == 'AE':
            model, train_losses, test_losses, correlations_cor, correlations_dis, x_batches, x_hat_batches, df_results = training_AE(train_data, test_data, units, unique_symbols, num_epochs, learning_rate, test_size)
        elif kind == 'AE_C':
            model, train_losses, test_losses, correlations_cor, correlations_dis, correlations_dis_train, x_batches, x_hat_batches, df_results = training_AE_C(train_data, test_data, units, unique_symbols, num_epochs, learning_rate, test_size, max_len, classes, weight)
            x_hat_equations = [torch.argmax(batch[0], dim=1).tolist() for batch in x_hat_batches]
            x_hat_constants = [batch[:][1] for batch in x_hat_batches]
            for i, batch in enumerate(x_hat_equations):
                for j, eq in enumerate(batch):
                    x_hat_equations[i][j] = classes[eq]
            x_hat_batches = (x_hat_equations, x_hat_constants)
        elif kind == 'VAE_C':
            model, train_losses, test_losses, correlations_cor, correlations_dis, x_batches, x_hat_batches, df_results = training_VAE_C(train_data, test_data, units, unique_symbols, num_epochs, learning_rate, test_size, klweight, classes, max_len, weight)
            x_hat_equations = [torch.argmax(batch[0], dim=1).tolist() for batch in x_hat_batches]
            x_hat_constants = [batch[:][1] for batch in x_hat_batches]
            for i, batch in enumerate(x_hat_equations):
                for j, eq in enumerate(batch):
                    x_hat_equations[i][j] = classes[eq]
            x_hat_batches = (x_hat_equations, x_hat_constants)
        results, x_batches_p, x_hat_batches_p, x_constants_p, x_hat_constants_p = evaluation_ec(
            x_batches=x_batches,
            x_hat_batches=x_hat_batches, #(x_hat_equations, x_hat_constants),
            equation_tree_dataset=d,
            max_len=max_len,
            kind=kind,)
        dct = {
            'latent dims': units, 
            #'correlation_cor': float(df_results['correlation_cor']), 
            'correlation_dis' : float(df_results['correlation_dis']),
            'correlation_cor last 10 epochs': np.sum(correlations_cor[-10:]) / 10, 
            'correlation_dis last 10 epochs': np.sum(correlations_dis[-10:]) / 10, 
            'accuracy (individual)':results['accuracy (individual)'], 
            'accuracy equations': results['accuracy (equations)'], 
            'constant MSE': results['average mse constants'], 
            'average distance constants': results['average distance constants'],
            'learning_rate': learning_rate,
            'weight': weight,
            'kl_weight': klweight,
            
        }
        if kind == 'AE':
            dct['recovered equations'] = random_embedding(kind, model, d, units, assignments, classes),
        if kind == 'VAE':
            dct['recovered equations'] = random_embedding(kind, model, d, units, assignments, classes),
            #dct['weight'] = klweight
            dct['test_reconstruction_loss']= df_results['test_reconstruction_loss'][-1]
            dct['test_constant_loss']= df_results['test_constant_loss'][-1]
            dct['test_latent_correlation_loss']= df_results['test_latent_correlation_loss'][-1]
            dct['test_kl_divergence']= df_results['test_kl_divergence'][-1]
        if kind == 'AE_C':
            #dct['weight'] = weight
            dct['test_reconstruction_loss']= float(df_results['test_reconstruction_loss'][-1])
            dct['test_constant_loss']= float(df_results['test_constant_loss'][-1])
            dct['test_latent_correlation_loss']= float(df_results['test_latent_correlation_loss'][-1])
            dct['correlations_dis_train']= float(correlations_dis_train[-1])
        if kind == 'VAE_C':
            #dct['weight'] = klweight
            dct['test_reconstruction_loss']= float(df_results['test_reconstruction_loss'][-1])
            dct['test_constant_loss']= float(df_results['test_constant_loss'][-1])
            dct['test_latent_correlation_loss']= float(df_results['test_latent_correlation_loss'][-1])
            dct['test_kl_divergence'] = float(df_results['test_kl_divergence'][-1])
            #dct['correlations_dis_train']= float(correlations_dis_train[-1])

    return dct
            
    #except Exception as e:
    #    print(e)