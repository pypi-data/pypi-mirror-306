# Purpose: Magnitude estimation
# Author: Minzhe Hu
# Date: 2023.8.26
# Email: hmz2018@mail.ustc.edu.cn
import numpy as np


def _phase2ab(phase):
    if phase in ['p', 'P', 0]:
        a = 0.437
        b = 1.269
    elif phase in ['s', 'S', 1]:
        a = 0.690
        b = 1.588
    else:
        raise ValueError("Phase must be 'P' or 'S'")
    return a, b


def fit_K(M, E, D, phase, ord=2):
    '''
    Fit Ki for n channels with m events.
    :param M: 1D array. magnitude for each event
    :param E: m*n array or float. peak amplitude of stain rate
    :param D: m*n array or float. hypocentral distance
    :param phase: only for p or s wave
    '''
    a, b = _phase2ab(phase)
    M = np.tile(M, (len(D[0]), 1)).T
    K = np.sum((np.log10(E) - a * M - b * D), 0)
    return K


def magnitude(E, D, K, phase):
    '''
    Estimate magnitude for one or multiple events.
    :param E: 1-D array or float. peak amplitude of stain rate
    :param D: 1-D array or float. hypocentral distance
    :param K: 1-D array or float. site calibration terms
    :param phase: only for p or s wave
    '''
    a, b = _phase2ab(phase)
    return (np.log10(E) - b * np.log10(D) - K) / a
