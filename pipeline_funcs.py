import numpy as np

def trans_func(x):
    return np.log(x+1)

def inv_func(x):
    return np.exp(x) - 1
