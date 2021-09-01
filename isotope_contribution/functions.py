import re

import numpy as np
import pandas as pd


def get_atomic_number(element):
    """
    Gets the atomic number of the extracted isotopic element from atomic_number.csv.

    Parameters:
    -----------
    element: str
        Element extracted from Gaussian log file - extract_isotope()

    Returns:
    --------
    atomic_number: int
        atomic number of the extracted element
    """

    # read in csv file as dataframe
    df = pd.read_csv("isotope_contribution/atomic_number.csv", header=0)
    # select the row that has the element in the log file in the Element column of the dataframe
    # only if the element exists.
    if element in df.values:
        result = df.loc[df["Element"] == element]
        # extract the atomic number by indexing the Atomic Number column
        atomic_number = result.iloc[0]["Atomic Number"]
        print("The atomic number of %s is %i" % (element, atomic_number))
    else:  # if the element does not exist in the csv file, print a warning and exit.
        print(
            "The element extracted from the log file does not exist in atomic_number.csv. Please add it to the csv file. Exiting."
        )
        exit()

    return atomic_number


def sum_coord(filename, atomic_number):
    """
    Extracts the isotope's XYZ coordinates for each individual frequency and sums them together,
    returning an array that represents approximately how much the isotope moves for each frequency.

    Parameters:
    -----------
    filename: str
        path to log file
    atomic_number: int
        atomic number of element

    Returns:
    --------
    coord_sum: list
        sum of isotope's XYZ coordinates for each frequency
    """
    # opening file
    with open(filename, "rt") as file:

        text = file.read()  # reading file into string
        # regex pattern to find atomic coordinate matrices:
        # "^.*?" - at the beginning of the string, match as few of any character (aside from new lines) as possible
        # "Z(?:\n.*(\d\.\d+)){1,}" - match "Z", and then in a non capturing group "(?:"
        # match a new line and any character (aside from new lines) as many times as possible "\n.*"
        # then in a capture group, match the format 0.00 "(\d\.\d+)"
        # then match the entire non capture group at least 1 time
        result = re.finditer(r"^.*?Z(?:\n.*(\d\.\d+)){1,}", text, re.MULTILINE)
        coord_list = []  # initialise list to store coordinates
        for m in result:
            x = m.group()  # x is a string of the entire atomic coordinate table
            # regex pattern to get lines of coordinate matrices
            # "\s+\d*\s+" search for at least 1 whitespace, as many digits as possible, and at least one whitespace.
            # (\d+) - in 1st capture group, match at least 1 digit - this is the atomic number of all the atoms.
            # "((?:(?:\s*)(?:\s|-)\d\.\d\d){1,})" - ((?:){1,}) - match the non capture group at least once
            # "(?:\s*)(?:\s|-)\d\.\d\d" - in a non capture group, look for any number of whitespace
            # in a second non capture group, look for either a whitespace or a "-" - this is to account for negative coordinates
            # "\d\.\d\d" - then look for 0.00
            atom_line = re.finditer(
                r"\s+\d*\s+(\d+)((?:(?:\s*)(?:\s|-)\d\.\d\d){1,})", x
            )

            for match in atom_line:  # for each match in the iterator
                if (
                    int(match.group(1)) == atomic_number
                ):  # if the first capture group (atomic number) equals the desired atomic number
                    x = (
                        match.group()
                    )  # x is the string of the coordinate line of the desired atomic number
                    x = x.lstrip()  # strips leading whitespace
                    x = list(
                        map(float, x.split())
                    )  # splits the line at whitespace, maps the resulting strings to a float, and then converts the floats to a list
                    x = x[
                        2:
                    ]  # removing the atom index number and the atomic number from the list to get the coordinates
                    coord_list += x  # appends sublist - coordinates of one row of frequencies to the full coordinate list
        # list comprehension to get a list for the coordinate sum
        # for x in the range from 0 to the length of the coordinate list, with a step of 3 (x coord, y coord, z coord)
        # add the coordinates from x to x+3 (x,y,z), and round the value to 3 decimal places
        coord_sum = np.asarray(
            [round(sum(coord_list[x : x + 3]), 3) for x in range(0, len(coord_list), 3)]
        )
    return coord_sum
