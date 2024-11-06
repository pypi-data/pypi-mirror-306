# Purpose: Some preprocess methods
# Author: Minzhe Hu, Hanwen Zou
# Date: 2023.8.27
# Email: hmz2018@mail.ustc.edu.cn
import numpy as np
from scipy.special import hankel1
from daspy.basic_tools.freqattributes import spectrum


def fj_method(data, dx, fs, nfft='default', f=None, v=np.arange(100, 3000, 5),
              verbose=False):
    x = np.arange(1, len(data) + 1) * dx
    spec, ff = spectrum(data, fs, tpad=nfft)
    if f is None:
        f = ff

    # F-J method
    dispen = np.zeros((len(f), len(v)), complex)
    for i, fi in enumerate(f):
        for j, vj in enumerate(v):
            k = 2 * np.pi * fi / vj
            bssh1 = hankel1(0, k * x)
            c = spec[:, round(fi / (ff[1] - ff[0]))]
            dispen[i, j] = np.sum(c * bssh1 * x)
    if verbose:
        return dispen, f, v
    return dispen
