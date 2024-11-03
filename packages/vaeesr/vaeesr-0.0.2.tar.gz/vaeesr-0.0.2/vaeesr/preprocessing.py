import random
import json
from tqdm import tqdm
import sys, os, io
from contextlib import contextmanager

import equation_tree
from equation_tree import instantiate_constants
from equation_tree.sample import sample, burn
from equation_tree.prior import prior_from_space, structure_prior_from_max_depth
from equation_tree.defaults import DEFAULT_PRIOR
from equation_tree.util.conversions import infix_to_prefix, prefix_to_infix
from equation_tree.tree import node_from_prefix

import numpy as np

import pandas as pd

import torch
from torch.utils.data import DataLoader, random_split, Dataset, Dataset, DataLoader, TensorDataset

from .utils import generate_values


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._oroginal_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._oroginal_stderr

@contextmanager
def silence_stdout_stderr():
    # Save the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    try:
        # Redirect stdout and stderr to devnull
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        yield
    finally:
        # Restore original stdout and stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr


prior = DEFAULT_PRIOR
#prior['functions'] = priors_from_space(['sin', 'cos', 'tan', 'exp', 'log'])
#prior['operators'] = priors_from_space(['+', '-', '*', '**', '/'])

class EquationDatasetClassify(Dataset):
    def __init__(self, equations, conditioning_values, char_to_idx, num_classes, constants):
        self.equations = equations
        self.char_to_idx = char_to_idx
        self.idx_to_char = {idx: char for char, idx in char_to_idx.items()}
        self.conditioning_values = conditioning_values
        self.constants = constants
        self.num_classes = num_classes

    def __len__(self):
        return len(self.equations)

    def encode_equation(self, equation):
        encoded = []
        for element in equation:
            if element in self.char_to_idx:
                num_encoding = self.char_to_idx[element]
                # one hot encoding
                encoded.append(num_encoding)
            else:
                # Handle unknown elements or special cases
                encoded.append(self.char_to_idx["<PAD>"])
        one_hot_equation = []
        for x in range(len(encoded)):
            one_hot_char = [0 for _ in range(self.num_classes)]
            one_hot_char[x] = 1
            one_hot_equation.append(one_hot_char)
        #one-hot encoding is implemented in the model
        return encoded

    def decode_equation(self, encoded):
        # argmax to get the index of the one hot encoding
        #encoded = torch.argmax(encoded, dim=1)
        #encoded = np.argmax(encoded, axis=1)
        #encoded_flatten = encoded.flatten()
        equation = []
        for element in encoded:
            equation.append(self.idx_to_char[int(element)])
        return equation

    def __getitem__(self, idx):
        equation = self.equations[idx]
        equation_encoded = self.encode_equation(equation)  # [idx]
        conditioning_values = self.conditioning_values[idx]
        constants = self.constants[idx]
        # print(equation_encoded)
        return (
            torch.tensor(equation_encoded, dtype=torch.long),
            torch.tensor(constants, dtype=torch.float),
            torch.tensor(conditioning_values, dtype=torch.float),
        )


def generate_dataset(spaces, num_equation_samples, max_tree_depth, x_values, constant_range=(-10, 10)):
    equations = []
    equations_final = []
    values = []
    constants = []
    max_len = 0
    classes_dict = {}
    const_array = np.array([])
    values_array = np.array([])
    equations_array = np.array([])

    function_prior = prior_from_space(spaces[0])
    operator_prior = prior_from_space(spaces[1])
    variable_prior = prior_from_space(spaces[2])
    constant_prior = prior_from_space(spaces[3])
    prior = {
        'structures': structure_prior_from_max_depth(max_tree_depth),
        'functions': prior_from_space(spaces[0]),
        'operators': prior_from_space(spaces[1]),
        'features': {'constants': 0.5, 'variables': 0.5}
    }
    is_function = lambda x: x in spaces[0]
    is_operator = lambda x : x in spaces[1]

    k = 0
    with tqdm(total=num_equation_samples) as pbar:
        while k < num_equation_samples:
            prior= {
                'structures': structure_prior_from_max_depth(max_tree_depth),
                'functions': prior_from_space(spaces[0]),
                'operators': prior_from_space(spaces[1]),
                'features': {'constants': 0.5, 'variables': 0.5}
            }
            #burn(prior)
            # sample equation
            with HiddenPrints():
                equation = sample(n=1, max_num_variables=1, prior=prior)
            #print(equation)
            # only add equation if it has maximum one constant
            if equation[0].n_constants == 1:
                # add equation 3 times (with different constants later)
                try:
                    for _ in range(3):
                        if k  < num_equation_samples:
                            # calculate maximum length of equation for padding later
                            if len(equation[0].prefix) > max_len:
                                max_len = len(equation[0].prefix)
                            # instantiate constant randomly
                            instantiated_equation = instantiate_constants(
                                equation[0], lambda: random.random() * (constant_range[1] - constant_range[0]) + constant_range[0]
                            )
                            # evaluate the equation at 50 equally spaced points between -1 and 1
                            input_df = pd.DataFrame({"x_1": x_values.tolist()})

                            # get f(x) values
                            with HiddenPrints():
                                y = instantiated_equation.evaluate(input_df)
                            try:
                                eq_prefix = infix_to_prefix(equation[0].infix, is_function, is_operator)
                                inf_eq = prefix_to_infix(equation[0].prefix, is_function, is_operator)
                                #test_conversion = node_from_prefix(eq_prefix, is_function, is_operator, is_variable, is_constant)
                                #classes_list.append(eq_prefix)
                                #classes_dict[inf_eq] = eq_prefix
                                # check if there are nan values in y
                                if all(val == val for val in y) and max(y) < 1000:
                                    const = instantiated_equation.constants
                                    if len(const_array) == 0:
                                        const_array = np.array([[float(const[0])]])
                                    else:
                                        const_array = np.append(const_array, [[float(const[0])]], axis=0)
                                    #constants.append([float(const[0])])
                                    #values.append((input_df["x_1"].values, y))
                                    if len(values_array) == 0:
                                        values_array = np.expand_dims(np.append(np.expand_dims(input_df["x_1"].values, axis=0), np.expand_dims(y, axis=0), axis=0), axis=0)
                                    else:
                                        values_array = np.append(values_array, np.expand_dims(np.append(np.expand_dims(input_df["x_1"].values, axis=0), np.expand_dims(y, axis=0), axis=0),axis=0), axis=0)
                                    equations.append(equation)
                                    classes_dict[equation[0].infix] = equation[0].prefix
                                    k += 1
                                    pbar.update(1)
                            except Exception as e:
                                #print(f"{equation[0].infix}: {e}") 
                                continue
                        else: 
                            pass
                        
                except Exception as e:
                    # catch exception in case instantiate_constants() throws 'ComplexInfinity' Exception
                    #print(e)
                    #print(equation)
                    continue
    pbar.close()
    for equation in equations:
        # try block due to complex infinity exception
        eq_prefix = equation[0].prefix
        # add padding so that all equations have the same shape
        if len(eq_prefix) < max_len:
            eq_prefix = eq_prefix + ["<PAD>"] * (max_len - len(eq_prefix))
        # add equations, constants and values to their list
        equations_final.append(eq_prefix)

    all_symbols = [item for sublist in equations_final for item in sublist]
    unique_symbols = sorted(list(set(all_symbols)))

    # obtain mapping from symbols to indices and vice versa
    symb_to_idx = {symbol: idx for idx, symbol in enumerate(unique_symbols)}
    idx_to_symb = {idx: symb for symb, idx in symb_to_idx.items()}
    

    dataset = EquationDatasetClassify(equations_final, values_array, symb_to_idx, len(classes_dict.keys()), const_array)
    classes = set([tuple(i) for i in equations_final])
    classes = [list(i) for i in classes]
    classes = [dataset.encode_equation(i) for i in classes]

    # pd.DataFrame(values, columns).to_csv('values_data.csv')
    return dataset, max_len, classes, unique_symbols


def preprocessing(dataset, batch_size, training_set_proportion):
    # split data into training and test sets
    train_size = int(training_set_proportion * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    # create data loaders
    train_dataloader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, pin_memory=True
    )
    test_dataloader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=True, pin_memory=True
    )

    return train_dataloader, test_dataloader, len(test_dataset)
