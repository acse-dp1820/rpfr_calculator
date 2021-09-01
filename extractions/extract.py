# Written by Devang Patel
# GitHub username: acse-dp1820

import re

import numpy as np


def extract_frequencies(filename, linear_check):
    """Extracts vibrational frequencies from the log file and
    checks that the expected number and actual number of frequencies match.

    Parameters:
    -----------
    filename: str
        The location of the Gaussian log file

    Returns:
    --------
    freq: ndarray
        1D array of vibrational frequencies

    """

    # checks that number of frequencies extracted is the expected. 3N-6 for non linear, 3N-5 for linear.

    # regex to extract the number of atoms
    # matches "NAtoms=", any number of whitespace, and any number of digits after.
    # brackets around \d* to ensure regex grouping occurs
    pattern = re.compile(r"NAtoms=\s*(\d*)")
    with open(filename, "rt") as file:
        for line in file:  # opening and searching through the file
            if pattern.search(line) is not None:  # ensuring a match exists
                # finds the regex pattern in file
                result = re.search(pattern, line)
                # converts the required string - (\d*), to an integer
                num_atoms = int(result.group(1))

    # Checking for linearity and calculating expected number of frequencies
    if linear_check == "y":
        exp_freq = 3 * (num_atoms) - 5
    elif linear_check == "n":
        exp_freq = 3 * (num_atoms) - 6
    else:
        "Please enter [y/n]. Exiting."
        exit()

    print("The number of expected frequencies is:", exp_freq)

    # using regex to find the string "Frequencies --"
    freq = []  # initialise list to store frequencies
    pattern = re.compile(r"Frequencies --")  # compiling the required regex

    with open(filename, "rt") as file:
        for line in file:  # opening and searching through the file
            if pattern.search(line) is not None:  # ensuring a match exists
                # Strip line to get string of frequencies only
                line = line.lstrip("Frequencies --").rstrip("\n")
                # splits line at whitespace, maps resulting strings to float + converts to list
                freq_list = list(map(float, line.split()))
                freq += freq_list  # concatenates sublists to single list

    # convert list to numpy array
    freq = np.array(freq)
    # variable to store number of frequencies
    num_freq = len(freq)

    # Performing frequency number check
    if num_freq != exp_freq:
        print(
            " ERROR - The number of extracted frequencies ("
            + str(num_freq)
            + ") is not equal to the expected number ("
            + str(exp_freq)
            + ")! \n"
        )
        print("Please check your log files for any inconsistencies. Exiting.")
        exit()
    else:
        print(num_freq, "frequencies extracted. \n")
    return freq


def extract_temp(filename):
    """
    Extracts the temperature value from the given log file.

    Parameters:
    -----------
    filename: str
        The location of the Gaussian log file

    Returns:
    --------
    temp: float
        Temperature value of the simulation


    """
    # example pattern "Temperature    298.150"
    # pattern
    # "Temperature(?:\s|=)*" - search for "Temperature" and any number of whitespace characters OR an = character, in a non capturing group
    # (\d*.\d*) - in 1st capture group, match any number of digit characters with a "." in between
    pattern = re.compile(r"Temperature(?:\s|=)*(\d*.\d*)")
    with open(filename, "rt") as file:
        for line in file:  # opening and searching through the file
            if pattern.search(line) is not None:  # ensuring a match exists
                # finds the regex pattern in file
                result = re.search(pattern, line)
                temp = float(
                    result.group(1)
                )  # convert regex group 1 - the temperature value, to float
    return temp


def extract_isotope(filename):
    """
    Extracts the isotopic information from an input file. N.B. only molecules with a single isotope.

    Parameters:
    -----------
    filename: str
        location of log file

    Returns:
    --------
    element: str
        Element that has isotopic information
    isotope: int
        Mass number of the isotope
    """
    # pattern
    # ([A-Za-z]*) - In 1st capture group, match any alphabetical character
    # \(Iso= - match "(Iso="
    # (\d*)\) - in a 2nd capture group, match any number of digit characters, and a ")"
    pattern = re.compile(r"([A-Za-z]*)\(Iso=(\d*)\)")
    with open(filename, "rt") as file:
        for line in file:  # opening and searching through the file
            if pattern.search(line) is not None:  # ensuring a match exists
                result = re.search(pattern, line)
                element = str(result.group(1))  # element identifier
                isotope = int(result.group(2))  # isotope number
    return element, isotope
