import matplotlib.pyplot as plt

import seaborn as sns

import torch

import numpy as np

from equation_tree.util.conversions import infix_to_prefix, prefix_to_infix
from equation_tree.tree import EquationTree, node_from_prefix, instantiate_constants

from sympy import *

import pandas as pd


# is_function = lambda x: x in ["sin", "cos", "tan", "exp", "log", "sqrt", "abs", "acos","asin",]
# is_operator = lambda x : x in ["+", "-", "*", "/", "**", "max", "min"]
# is_variable = lambda x : x in ["x_1"]



def try_infix(equation, constant):
    if type(constant) == list:
        constant = constant[0]
    try: 
        return prefix_to_infix(equation, is_function, is_operator).replace(
                            "c_1", str(round(constant, 2))
                        )
    except Exception as e:
        return str(equation)

def mapping_from_spaces(spaces):
    is_function = lambda x : x in spaces[0]
    is_operator = lambda x : x in spaces[1]
    if len(spaces) == 4:
        is_variable = lambda x : x in spaces[2]
        is_constant = lambda x : x in spaces[3]
    else: 
        is_variable = lambda x : x in ["x_1", "x_1", "X"],
        is_constant = lambda x : x in ["c_0", "c_1"]
    return is_function, is_operator, is_variable, is_constant

def decode_latent_classify(model, equation_tree_dataset, z_list, classes):
    z_decoded_equations = []
    z_decoded_constants = []
    for v in z_list:
        v = torch.tensor(2 * [v])
        v_decode, v_constants = model.decode(v)
        v_constants = v_constants.detach().numpy()
        v_decode = v_decode.detach().numpy()
        v_decode = np.argmax(v_decode, axis=1)
        v_decode = [classes[i] for i in v_decode]
        v_decode = equation_tree_dataset.decode_equation(v_decode[0])
        z_decoded_equations.append(v_decode)
        z_decoded_constants.append(v_constants)
    
    return z_decoded_equations, z_decoded_constants

def generate_values(equation, constant, is_function, is_operator, is_variable, is_constant, x_values, infix=None):
    #is_constant = lambda x: x in ["c_1"]

    constant = float(constant)
    if type(equation) == str:
        equation_prefix = infix_to_prefix(equation, is_function, is_operator,)
        
    else:
        if '<PAD>' in equation:
            equation_prefix = [item for item in equation if item != '<PAD>']
        else: 
            equation_prefix = equation
        if infix == None:
            try:
                infix = prefix_to_infix(equation_prefix, is_function, is_operator)
            except:
                print(f"Failed to convert {equation_prefix} to infix")
                return (None,)
    try: 
        equation_node = node_from_prefix(equation_prefix, is_function, is_operator, is_variable, is_constant)
    except:
        print(f"Failed to create tree: {equation_prefix}")
        return (None,)
    equation_tree = EquationTree(equation_node)
    try:
        instantiated_equation = instantiate_constants(equation_tree, lambda: constant)
        # print(f"Instantiated equation: {instantiated_equation}")
        # evaluate the equation at 50 equally spaced points between -1 and 1        
        x_1 = x_values
        input_df = pd.DataFrame({"x_1": x_1.tolist()})
        # get f(x) values
        y = instantiated_equation.evaluate(input_df).astype(float)
        #y= instantiated_equation.get_evaluation(-1, 1, 50)
        if len(y) == 0:
            print(f"Failed to evaluate {equation} (y is empty)")
            return (None,)
        return input_df["x_1"].values.tolist(), y.tolist()
    except Exception as e:
        try: 
            x = symbols('x')
            x_1 = x_values
            input_df = pd.DataFrame({"x_1": x_1.tolist()})
            infix = prefix_to_infix(equation_prefix, is_function, is_operator)
            infix = infix.replace("X", "x").replace("c_0", str(constant))
            expr = sympify(infix)
            y = [expr.subs(x, x_val).evalf() for x_val in input_df["x_1"]]
            #print(y)
            return input_df["x_1"].values.tolist(), y
        except Exception as e:
            print(f"Failed to evaluate {equation}")
            print(e)
            return (None,)

