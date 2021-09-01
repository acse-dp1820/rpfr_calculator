# Written by Devang Patel
# GitHub username: acse-dp1820

import os
import re


def filename_check(filename):
    """
    Checks if the filename provided exists and exits the program if not.

    Parameters
    ----------
    filename: str
        The file location of the Gaussian log file
    """
    # if the filename doesn't exist, exit.
    if not os.path.isfile(filename):
        print("ERROR - %s does not exist! Exiting...." % filename)
        exit()


def inspect_file(filename, pattern):
    """
    Inspects file for regex patterns required by other functions.

    Parameters:
    -----------
    filename: str
        location of Gaussian log file
    pattern: str
        the regex pattern to look for within the file

    Returns:
    --------
    check: bool
        Indicates the presence of the specific regex pattern in the log file.
    """
    with open(filename, "rt") as file:  # opens file
        text = file.read()  # reads file into string
        if (
            pattern == r"(^.*?Converged\?(?:\n.*(YES)){4})"
        ):  # pattern for the item convergence table
            check = bool(
                re.search(pattern, text, re.MULTILINE)
            )  # the regex search needs to be a multiline search.
        else:  # if not
            check = bool(
                re.search(pattern, text)
            )  # regex is a normal search with no flags.
        return check


def check_optimisation(filename):
    """
    Checks convergence of item convergence table and informs user of convergence via terminal.

    Parameters:
    -----------
    filename: str
        location of log file

    Returns:
    --------
    table: str
        Item convergence table

    """
    # complex regex method
    with open(filename, "rt") as file:
        # reads file into a single string
        text = file.read()
        # pattern searched as a multiline regex search through the entire file
        # "^.*?"" - match as few non line-break characters as possible at the beginning of string
        # match "Converged?"
        # "(?:\n.*"" - in a non capture group, match a new line and any non line break characters
        # "(YES){4}" in a capture group, match "YES" 4 times
        # ensure only picks up the convergence tables that indicate full convergence
        result = re.finditer(r"^.*?Converged\?(?:\n.*(YES)){4}", text, re.MULTILINE)
        # ensuring last match is the one extracted
        match = None
        for match in result:
            pass
        table = match.group()

        for x in re.finditer(
            # pattern searched as a multiline regex search within the result groups
            # "^ " - Match beginning of string and a space
            # "(Maximum|RMS)" - in 1st capture group, match "Maximum" or "RMS"
            # ".*?" - match as few non line break characters as possible
            # "(Force|Displacement)" - in 2nd capture group match "Force" or "Displacement"
            # "(YES|NO )$" in 3rd capture group, match "YES" or "NO " at the end of the string
            r"^ (Maximum|RMS).*?(Force|Displacement).*?(YES)$",
            table,
            re.MULTILINE,
        ):
            # if the third capture group is "YES", print that groups 1 and 2 have converged
            if x.group(3) == "YES":
                print(str(x.group(1)) + " " + str(x.group(2)) + " converged.")

            # commented out as no longer needed, kept in for posterity.
            # # if capture group 3 is NO, print that groups 1 and 2 did not converge.
            # else:
            #     print(str(x.group(1)) + " " + str(x.group(2)) + " did not converge.")
            #     # asking user if they want to continue even though the molecule may be unoptimised.
            #     conv_check = input(
            #         "WARNING - Frequencies may be from an unoptimised molecule.\nWould you like to continue? [y/n]: "
            #     )
            #     if conv_check == "n":
            #         exit()
            #     elif conv_check == "y":
            #         continue
            #     else:
            #         print("Please enter [y/n]. Exiting.")
            #         exit()

    return table


def check_low_freq(filename):
    """
    Checks if low frequencies meet a threshold of +/- 30 cm-1.

    Parameters:
    -----------
    filename: str
        location of log file

    Returns:
    --------
    low_freq: list
        List of low frequencies

    """
    # low frequencies
    low_freq = []  # initialise low frequency list
    pattern = re.compile(r"Low frequencies ---")
    with open(filename, "rt") as file:
        for line in file:
            if pattern.search(line) is not None:  # ensuring a match exists
                # Strip line to get string of frequencies only
                line = line.lstrip("Low frequencies ---").rstrip("\n")
                # splits line, maps string to float + converts to list
                freq_list = list(map(float, line.split()))
                low_freq += freq_list  # concatenates sublists to single list
    # print low freq + warning
    print("\nLow frequencies: " + str(low_freq))
    if any(f > 30.0 for f in low_freq) or any(f < -30.0 for f in low_freq):
        print(
            "\nWarning! Some low frequencies exceed the +/- 30 cm-1 threshold! Treat results with caution. \n"
        )

    return low_freq
