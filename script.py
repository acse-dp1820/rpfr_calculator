# Written by Devang Patel
# GitHub username: acse-dp1820

import sys

from calculations.calculations import reduced_partition_function_ratio
from extractions.extract import extract_frequencies, extract_isotope, extract_temp
from file_io.check import (
    check_low_freq,
    check_optimisation,
    filename_check,
    inspect_file,
)
from file_io.output import output_file
from isotope_contribution.functions import get_atomic_number, sum_coord

# checking corrent number of arguments has been passed
if len(sys.argv) != 6:  # including script.py as argument 0
    print("ERROR - Incorrect number of arguments given!")
    raise SystemExit(
        f"Usage: {sys.argv[0]} <'path to light isotope file'> <'path to heavy isotope file'> <'y' or 'n'> <'path to output file'> <'True' or 'False'>"
    )

# first argument as light isotope filename variable
l_filename = sys.argv[1]
# second argument as heavy isotope filename variable
h_filename = sys.argv[2]
# linear molecule check
linear_check = sys.argv[3]
# output filename
output = sys.argv[4]
# print variable
print_var = sys.argv[5]

# Checking filenames exist
filename_check(l_filename)
filename_check(h_filename)

# Inspecting isotope files for the required extraction patterns

# light
l_temp_check = inspect_file(l_filename, r"Temperature(?:\s|=)*(\d*.\d*)")
light_iso_check = inspect_file(l_filename, r"([A-Za-z]*)\(Iso=(\d*)\)")
l_opt_check = inspect_file(l_filename, r"(^.*?Converged\?(?:\n.*(YES)){4})")
l_lowfreq_check = inspect_file(l_filename, r"Low frequencies ---")
l_freq_check = inspect_file(l_filename, r"Frequencies --")

# heavy
h_temp_check = inspect_file(h_filename, r"Temperature\s*(\d*.\d*)")
heavy_iso_check = inspect_file(h_filename, r"([A-Za-z]*)\(Iso=(\d*)\)")
h_opt_check = inspect_file(h_filename, r"(^.*?Converged\?(?:\n.*(YES)){4})")
h_lowfreq_check = inspect_file(h_filename, r"Low frequencies ---")
h_freq_check = inspect_file(h_filename, r"Frequencies --")

print("\n------------------ TEMPERATURE CHECK ------------------\n")

if l_temp_check and h_temp_check:  # if temp checks are True
    print("Extracting temperature values from the log files...")
    # extract temperature values from log files
    l_temp = extract_temp(l_filename)
    h_temp = extract_temp(h_filename)
    print("Checking the temperature values in both log files are equal.")
    # if temperatures are equal, set the temperature equal to light isotope temp (arbitrary)
    if l_temp == h_temp:
        temperature = l_temp
        print("Temperature: ", temperature, " K\n")
    # if not, there are inconsistencies between the log files, program does not continue.
    elif l_temp != h_temp:
        print(
            "The temperatures are not the same! Please check for inconsistencies in log files. Exiting..."
        )
        exit()

else:  # Temperature checks fail, program exits
    print("Temperature not found in either log file.")
    print("The reduced partition function will not be calculated. Exiting...")
    exit()

print("\n----------- LIGHT ISOTOPE FREQ. EXTRACTION -----------\n")

# light isotope log file
print("The light isotope log file is: ", l_filename)

# elemental + isotopic information
if light_iso_check:  # if isotopic information exists
    print("Extracting isotopic information.")
    element, l_isotope = extract_isotope(l_filename)
else:
    print("Light isotope nonexistent. Unable to extract.")

# check item convergence table
if l_opt_check:  # if convergence table exists
    print("Extracting item convergence table")
    l_table = check_optimisation(l_filename)
else:
    print("Convergence table for optimised molecule not found.")
    if (
        input("Your molecule may be unoptimised - would you like to continue? [y/n]")
        == "n"
    ):
        exit()

# check low frequencies
if l_lowfreq_check:  # if low frequencies exist
    print("Extracting low frequencies.")
    l_low_freq = check_low_freq(l_filename)
else:
    print("Low frequencies not found.")

# extracting frequencies
if l_freq_check:  # if frequencies exist
    print("Extracting frequencies.")
    light_freq = extract_frequencies(l_filename, linear_check)
else:
    print("Frequencies not found.")
    # ask user if they would like to continue
    if input("Would you like to continue? [y/n] ") == "n":
        exit()

print("\n----------- HEAVY ISOTOPE FREQ. EXTRACTION -----------\n")

print("The heavy isotope log file is: ", h_filename)

# checking isotopic information
if heavy_iso_check:
    print("Extracting isotopic information.")
    element, h_isotope = extract_isotope(h_filename)
else:
    print("Heavy isotope nonexistent. Unable to extract.")

# checking item convergence table
if h_opt_check:
    print("Extracting item convergence table")
    h_table = check_optimisation(h_filename)
else:
    print("Convergence table for optimised molecule not found.")
    if (
        input("Your molecule may be unoptimised - would you like to continue? [y/n]")
        == "n"
    ):
        exit()

# checking low frequencies
if h_lowfreq_check:
    print("Extracting low frequencies.")
    h_low_freq = check_low_freq(h_filename)
else:
    print("Low frequencies not found.")

# extracting frequencies
if h_freq_check:
    print("Extracting frequencies.")
    heavy_freq = extract_frequencies(h_filename, linear_check)
else:
    print("Frequencies not found.")
    # ask user if they would like to continue
    if input("Would you like to continue? [y/n] ") == "n":
        exit()

print("\n--------------------- CALCULATION ---------------------\n")

# calculating RPFR, if frequencies and temperatures exist.
if l_freq_check and h_freq_check and (l_temp_check or h_temp_check):
    print("Now calculating the reduced partition function ratio...")
    beta, ratio, Q_heavy, Q_light = reduced_partition_function_ratio(
        light_freq, heavy_freq, temperature
    )
else:
    print("Unable to calculate the reduced partition function ratio.")

if l_freq_check and h_freq_check:
    print("\n-------------- CONTRIBUTIONS TO FREQUENCY --------------\n")

    print(
        "This section calculates the extent to which the isotope moves for each frequency."
    )
    print(
        "The atomic number is extracted from isotope_contribution/atomic_number.csv. If the element you need is not present, please add it."
    )
    print(
        "The absolute sum of the X,Y,Z coordinates is calculated for each frequency and stored in an array."
    )

    # getting atomic number
    atomic_number = get_atomic_number(element)

    # getting frequency contributions and asserting the arrays are the same length as frequency arrays
    l_cont = sum_coord(l_filename, atomic_number)
    assert len(l_cont) == len(
        light_freq
    ), "Error - length of light frequency contribution array does not equal the length of the light frequency array!"

    h_cont = sum_coord(h_filename, atomic_number)
    assert len(h_cont) == len(
        heavy_freq
    ), "Error - length of heavy frequency contribution array does not equal the length of the heavy frequency array!"

    # determining the frequencies that have a non-zero coordinate sum - i.e. the isotope vibrates
    # this is done by indexing the frequency arrays with the coordinate array values that are nonzero
    l_freq_cont = light_freq[(l_cont != 0.0)]
    h_freq_cont = heavy_freq[(h_cont != 0.0)]

    print(
        "Frequency contributions ascertained.\nNumber of frequencies that have light isotope movement: %i.\nNumber of frequencies that have heavy isotope movement: %i.\n"
        % (len(l_freq_cont), len(h_freq_cont))
    )

    if len(l_freq_cont) != len(h_freq_cont):
        print(
            "The number of light / heavy frequencies that contain isotope movement are not the same. Unable to calculate secondary RPFR."
        )
    else:
        print(
            "The number of light / heavy frequencies that contain isotope movement are the same.\nCalculating RPFR with selected frequencies - treat this result with caution."
        )
        if l_freq_check and h_freq_check and (l_temp_check or h_temp_check):
            print("Now calculating the reduced partition function ratio...")
            (
                beta_test,
                ratio_test,
                Q_heavy_test,
                Q_light_test,
            ) = reduced_partition_function_ratio(l_freq_cont, h_freq_cont, temperature)
        else:
            print(
                "Unable to calculate the reduced partition function ratio with selected frequencies."
            )
else:
    print("Unable to ascertain isotope movement for individual frequencies.")

print("\n--------------- WRITING TO OUTPUT FILE ----------------\n")

# checking if file exists + creating directories
output_file(output)

print("\nBasic information saved to file (if print variable == False):")
print(
    "Input filepaths\nIsotopic information\nTemperature\nRPFR - for all frequencies\nIf applicable, RPFR for freq. with isotopic movement\nFull list of frequencies\nSubset of frequencies that have isotopic movement.\n"
)

print("Full information saved to file (if print variable == True):")
print(
    "Individual components of RPFR\nFull isotopic motion arrays\nItem convergence tables\nLow frequencies\n"
)
if print_var == "True":  # write all extracted information to file
    print("Writing all extracted information to %s" % (output))
elif print_var == "False":  # only temp, RPFR + frequency lists
    print("Writing basic information to %s" % (output))
else:  # if variable not recognised, print basic information
    print("Print variable not recognised. Writing basic information to %s" % (output))

# Writing RPFR to file
print("Writing data to file...")

with open(output, "w") as f:
    # write basic information to file
    # what files the data comes from
    f.write("This output file is generated from the following files: \n")
    f.write(
        "Light isotope file: %s\nHeavy isotope file: %s\n\n" % (l_filename, h_filename)
    )

    # write isotopic information
    if light_iso_check and heavy_iso_check:
        f.write(
            "%s isotopes extracted: %s and %s\n"
            % (element, str(l_isotope), str(h_isotope))
        )
    elif light_iso_check or heavy_iso_check:
        if light_iso_check:
            f.write("%s isotope extracted: %s\n" % (element, str(l_isotope)))
        else:
            print("Unable to write light isotopic information.")
        if heavy_iso_check:
            f.write("%s isotope extracted: %s\n" % (element, str(h_isotope)))
        else:
            print("Unable to write heavy isotopic information.")
    else:
        print("Unable to write isotopic information.")

    # Temperature of optimisation simulation
    if l_temp_check and h_temp_check:
        f.write("Temperature = " + str(temperature) + " K\n\n")
    else:
        print("Unable to write temperature to file.")

    # number of frequencies
    if l_freq_check:
        f.write(
            "Number of frequencies used in calculating FULL RPFR: %i\n"
            % len(light_freq)
        )

    # reduced partition function ratio
    # print components of RPFR if print variable is set to True
    if l_freq_check and h_freq_check and (l_temp_check or h_temp_check):
        if print_var == "True":
            f.write("ln(v/v'): %s\n" % (str(ratio)))
            f.write("lnQ: %s\n" % (str(Q_heavy)))
            f.write("lnQ': %s\n" % (str(Q_light)))
        f.write("RPFR: %s\n\n" % (str(beta)))
    else:
        print("Unable to write RPFR to file.")

    if l_freq_check and h_freq_check:
        # reduced partition function ratio with selected frequencies that contain isotope movement
        if len(l_freq_cont) == len(h_freq_cont):
            f.write(
                "Number of frequencies used in calculating secondary RPFR: %i\n"
                % len(l_freq_cont)
            )
            f.write(
                "This is the RPFR calculated using the frequencies that contain isotope movement.\n"
            )
            # print components of RPFR if print variable is set to True
            if l_freq_check and h_freq_check and (l_temp_check or h_temp_check):
                if print_var == "True":
                    f.write("ln(v/v'): %s\n" % (str(ratio_test)))
                    f.write("lnQ: %s\n" % (str(Q_heavy_test)))
                    f.write("lnQ': %s\n" % (str(Q_light_test)))
                f.write("RPFR: %s\n" % (str(beta_test)))
            else:
                print(
                    "Unable to write RPFR (with selected frequencies) to file. This is due to the number of frequencies not being the same between light and heavy isotopes."
                )

    # Writing frequencies and contributions to file if frequency checks are True
    if l_freq_check:
        f.write("\nLight isotope frequencies:\n%s\n" % str(light_freq))
        if print_var == "True":  # print full isotope frequency contribution array
            f.write(
                "\nIsotope contributions - estimation of isotope movement in each frequency:\n%s\n"
                % str(l_cont)
            )
        f.write(
            "\nThe frequencies that contain movement of the isotope:\n%s\n"
            % str(l_freq_cont)
        )
    else:
        print("Unable to write light isotope frequencies to file.")

    if h_freq_check:
        f.write("\nHeavy isotope frequencies:\n%s\n" % str(heavy_freq))
        if print_var == "True":
            f.write(
                "\n Isotope contributions - estimation of isotope movement in each frequency:\n%s\n"
                % str(h_cont)
            )
        f.write(
            "\nThe frequencies that contain movement of the isotope:\n%s\n"
            % str(h_freq_cont)
        )
    else:
        print("Unable to write heavy isotope frequencies to file.")

    # write extra information to file if print_var is True
    if print_var == "True":  # print item convergence and low frequencies

        # Light Isotope
        if l_opt_check:
            f.write("\nLight isotope convergence table:\n")
            f.write("%s\n" % (l_table))  # write table to file
        else:
            print("\nUnable to write light isotope convergence table to file.")
        if l_lowfreq_check:
            f.write("\nLow frequencies: ")
            # write low frequency list to file
            f.write("%s\n" % (str(l_low_freq)))
        else:
            print("Unable to write light isotope low frequencies to file.")

        # Heavy Isotope
        if h_opt_check:
            f.write("\nHeavy isotope convergence table: \n")
            f.write("%s\n" % (h_table))  # write table to file
        else:
            print("Unable to write heavy isotope convergence table to file.")
        if h_lowfreq_check:
            f.write("\nLow frequencies: ")
            # write low frequency list to file
            f.write("%s\n" % (str(h_low_freq)))
        else:
            print("Unable to write heavy isotope low frequencies to file.")

    print(
        "Program complete. Please check command line output for any issues that may have occurred."
    )
