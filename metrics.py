import numpy as np 

def calculate_mean(results):
    return np.mean(results, axis=0)

def calculate_standard_deviation(results):
    return np.std(results, axis=0)


def calculate_minimum(results):
    return np.min(results, axis=0)


def calculate_maximum(results):
    return np.max(results, axis=0)