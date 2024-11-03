import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np

def correlation_coeff(values, z):
    """
    Compute the correlation coefficient between the values and the latent variables.
    
    Args:
    - values (torch.Tensor): Values of the functions.
    - z (torch.Tensor): Latent variables.
    
    Returns:
    - torch.Tensor: Correlation coefficient between the values and the latent variables.
    """
    # TODO find better solutions to deal with inf values (remove them before computing the correlation coefficient?)
    distance_values = torch.nan_to_num(torch.cdist(values, values, p=1.0)/25, posinf=1000, neginf=-1000)

    area_values = []     
    #for i,_ in enumerate(values):
    #    for k,_ in enumerate(values):
    #        area_values.append(torch.nan_to_num(torch.sum(torch.abs(torch.sub(values[i], values[k]))))/2)

    correlation_values = torch.nan_to_num(torch.corrcoef(values), posinf=1000, neginf=-1000)
    distance_z = torch.nan_to_num(torch.cdist(z, z, p=1.0), posinf=1000, neginf=-1000)

    correlation_dis = torch.corrcoef(torch.stack((distance_values.flatten(), distance_z.flatten())))[0, 1]
    correlation_cor = torch.corrcoef(torch.stack((correlation_values.flatten(), distance_z.flatten())))[0, 1]
    covariance_dis = torch.cov(torch.stack((distance_values.flatten(), distance_z.flatten())))[0, 1]
    covaraince_cor = torch.cov(torch.stack((correlation_values.flatten(), distance_z.flatten())))[0, 1]
    
    return correlation_cor, correlation_dis, covaraince_cor, covariance_dis


class LatentCorrelationLoss(nn.Module):
    def __init__(self):
        super(LatentCorrelationLoss, self).__init__()
    
    def forward(self, values, z):
        correlation_cor, correlation_dis, covariance_cor, covariance_dis = correlation_coeff(values, z)
        #return -covariance_dis
        #return 1/((covariance_dis+1)*0.5)
        return - correlation_dis + 1 
        #return correlation_dis + 1 #1/((correlation_cor+1)*0.5)
        #return -(correlation_cor + 1) +2