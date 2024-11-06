# Purpose:
# Author:
# Date:
# Email:

import numpy as np


def X_corr(a, b):
    a = (a - np.mean(a)) / np.std(a)
    b = (b - np.mean(b)) / np.std(b)
    return sum(a*b) / len(a)