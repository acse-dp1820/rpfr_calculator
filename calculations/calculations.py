# Written by Devang Patel
# GitHub username: acse-dp1820

import numpy as np
import scipy.constants


def partition_function(array, temp):
    """
    Given an array of vibrational frequencies, the natural log of the vibrational partition function is calculated.

    Calculations taken from: Blanchard, M., Balan, E. and Schauble, E.A., 2017. Reviews in Mineralogy and Geochemistry, 82(1), pp.27-63.

    Parameters:
    ------
    array: ndarray
        1-dimensional numpy array of vibrational frequencies

    Returns:
    -------
    Q: float
        natural log of the vibrational partition function
    """

    # Constants imported from scipy.constants
    h = scipy.constants.h  # Planck's constant
    # speed of light must be in cm/s as wavenumber is in cm-1
    c = scipy.constants.c * 100
    k = scipy.constants.k  # Boltzmann constant
    T = temp  # extracted from log file using extract_temp()

    # check if inputs are numpy arrays and convert if not.
    if not isinstance(array, np.ndarray):
        np.asarray(array)

    # conversion to exponent
    u = (h * array * c) / (k * T)

    # calculates natural log of an individual frequency contribution to the partition function
    Q_ = np.log(np.exp(-(u / 2)) / (1 - np.exp(-u)))
    # sums all the contributions together, giving the final result.
    Q = np.sum(Q_)
    return Q


def reduced_partition_function_ratio(light_freq, heavy_freq, temp):
    """
    Using the vibrational frequency lists of 2 singly substituted isotopologues, this function calculates the reduced partition function ratio between the 2.

    Calculations taken from: Blanchard, M., Balan, E. and Schauble, E.A., 2017. Reviews in Mineralogy and Geochemistry, 82(1), pp.27-63.

    Parameters:
    -------
    light_freq: ndarray
        vibrational frequencies of the light isotopologue
    heavy_freq: ndarray
        vibrational frequencies of the heavy isotopologue

    Returns:
    --------
    beta: float
        1000*lnB, where B is the reduced partition function ratio.
    """
    # check lengths of arrays are the same.
    # The error would only occur if the 2 molecules are different.
    assert len(light_freq) == len(
        heavy_freq
    ), "Array lengths do not match - please ensure both your chosen log files optimise the same molecule!"

    # check if numpy array and convert if not.
    if not isinstance(light_freq, np.ndarray):
        np.asarray(light_freq)
    if not isinstance(heavy_freq, np.ndarray):
        np.asarray(heavy_freq)

    # calculate ln of ratio of heavy / light frequencies
    ratio = np.log(np.divide(heavy_freq, light_freq))
    # check if length of ratio array is the same as the frequency arrays
    assert len(ratio) == len(light_freq) == len(heavy_freq)

    # add the ratios together
    ratio = np.sum(ratio)

    # calculate vibrational partition functions
    Q_light = partition_function(light_freq, temp)
    Q_heavy = partition_function(heavy_freq, temp)

    # print variables used to calculate RPFR
    print("Primed variables (v', Q') refer to the light isotope.")
    print("ln(v/v'): ", ratio)
    print("lnQ: ", Q_heavy)
    print("lnQ': ", Q_light)

    # calculate RPFR, defined as 1000*ln(beta).
    beta = 1000 * (ratio + Q_heavy - Q_light)
    print("1000*lnB: ", beta)
    return beta, ratio, Q_heavy, Q_light
