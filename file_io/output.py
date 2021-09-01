# Written by Devang Patel
# GitHub username: acse-dp1820

import os


def output_file(filename):
    """
    Checks if the file exists + creates filepath with any associated directories.

    Parameters:
    -----------
    filename: str
        location of output file
    """
    # if file exists, print filepath
    if os.path.isfile(filename):
        print("The output filepath is: " + filename)
    # if file doesn't exist, create the filepath even if some directories exist and print filepath
    else:
        print("Creating file + associated directories.")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        print("The output filepath is: " + filename)
