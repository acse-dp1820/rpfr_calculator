# Written by Devang Patel
# GitHub username: acse-dp1820

import numpy as np

from calculations.calculations import reduced_partition_function_ratio
from extractions.extract import extract_frequencies, extract_temp


def test_extraction(l_filename, h_filename, linear_check, m_light_freq, m_heavy_freq):
    """
    Tests the extraction function, `extract_frequencies()` by comparing values from ./tests/test_files/calculations.xlsx

    Parameters:
    -----------
    l_filename: str
        location of light isotope log file
    h_filename: str
        location of heavy isotope log file
    linear_check: str
        Variable that states if the molecule in the log file(s) is linear
    m_light_freq: list
        list of manually extracted frequencies from the light isotope log file
    m_heavy_freq: list
        list of manually extracted frequencies from the heavy isotope log file
    """
    # computationally extracted frequencies
    print("Extracting from %s." % (l_filename))
    light_freq = extract_frequencies(l_filename, linear_check)

    # if the frequencies are the same:
    if np.allclose(m_light_freq, light_freq):
        print(
            "The light isotope frequencies extracted computationally are identical to those extracted manually.\n"
        )
    else:
        print(
            "The light isotope frequencies extracted computationally are NOT identical to those extracted manually!\n"
        )

    print("Manually extracted values: ", m_light_freq)
    print("Computationally extracted values: ", light_freq)

    print("Extracting from %s." % (h_filename))
    heavy_freq = extract_frequencies(h_filename, linear_check)

    if np.allclose(m_heavy_freq, heavy_freq):
        print(
            "The heavy isotope frequencies extracted computationally are identical to those extracted manually.\n"
        )
    else:
        print(
            "The heavy isotope frequencies extracted computationally are NOT identical to those extracted manually!\n"
        )

    print("Manually extracted values: ", m_heavy_freq)
    print("Computationally extracted values: ", heavy_freq)


def test_calculation(
    l_filename, h_filename, linear_check, m_beta, m_ratio, m_Qlight, m_Qheavy
):
    """
    Tests calculation functions by comparing values to those found in ./tests/test_files/calculations.xlsx

    Parameters:
    -----------
    l_filename: str
        location of light isotope log file
    h_filename: str
        location of hevay isotope log file
    linear_check: str
        Variable that states if the molecule in the log file(s) is linear
    m_beta: float
        manually calculated beta value
    m_ratio: float
        manually calculated value of the ratio of heavy / light frequencies
    m_Qlight: float
        manually calculated natural log of the light isotope's vibrational partition function
    m_Qheavy: float
        manually calculated natural log of the heavy isotope's vibrational partition function
    """
    # extracting from light isotope
    print("Extracting from %s." % (l_filename))
    light_freq = extract_frequencies(l_filename, linear_check)
    # extracting from heavy isotope
    print("Extracting from %s." % (h_filename))
    heavy_freq = extract_frequencies(h_filename, linear_check)
    # extracting temperature
    print(
        "Extracting temperature - comparison not carried out, assumed the same in both input files."
    )
    temp = extract_temp(l_filename)

    print("Now calculating the reduced partition function ratio...\n")
    beta, ratio, Q_heavy, Q_light = reduced_partition_function_ratio(
        light_freq, heavy_freq, temp
    )  # calculated RPFR

    # manual values from spreadsheet
    print("\nManual values:")
    print("ln(v/v'): ", m_ratio)
    print("lnQ: ", m_Qheavy)
    print("lnQ': ", m_Qlight)
    print("1000*lnB : ", m_beta)

    # creating arrays for comparison
    manual_values = [m_beta, m_ratio, m_Qheavy, m_Qlight]
    calc_values = [beta, ratio, Q_heavy, Q_light]

    # comparison
    if np.allclose(calc_values, manual_values, rtol=1e-5, atol=1e-8):
        print(
            "\nAll the calculated values agree within an absolute tolerance of: 1e-8, and the computational value has significantly more precision."
        )
    else:
        print("The calculated values do not agree.")


if __name__ == "__main__":  # only execute this if this file is run as a script

    print("----------------------- TESTING ------------------------\n")

    # run extraction tests
    extract = input("Would you like to run extraction tests? [y/n]: ")
    if extract == "y":

        print("Frequencies manually extracted from log files.\n")
        print("----------------- ZnCl4 - EXTRACTION -------------------\n")
        print(
            "Testing frequency extraction on ZnCl4, as it's a small, non linear molecule."
        )

        # set filenames for ZnCl4 files and if the molecule is linear
        l_filename = "tests/log_files/zinc/ZNCL4_B_64.LOG"
        h_filename = "tests/log_files/zinc/ZNCL4_B_66.LOG"
        linear_check = "n"

        # manually extracted frequencies
        manual_light_freq = np.asarray(
            [
                78.5452,
                78.5452,
                126.6746,
                126.6746,
                126.6746,
                232.1478,
                232.2047,
                232.2047,
                232.2047,
            ]
        )
        manual_heavy_freq = np.asarray(
            [
                78.5452,
                78.5452,
                126.2453,
                126.2453,
                126.2453,
                230.5599,
                230.5599,
                230.5599,
                232.1478,
            ]
        )

        test_extraction(
            l_filename, h_filename, linear_check, manual_light_freq, manual_heavy_freq
        )

    elif extract == "n":
        print("Not running extraction tests.")
    else:
        print("Unknown input. Exiting")
        exit()

    # run calculation tests
    calc = input("Would you like to run calculation tests? [y/n]: ")
    if calc == "y":

        print(
            "This tests the calculated values of the RPFR against manually determined values for light/heavy isotopologues of ZnCl4 and ZnH2O."
        )
        print("Manual calculations carried out in ./tests/calculations.xlsx\n")

        cl = input("Would you like to run the ZnCl4 tests? [y/n]: ")
        if cl == "y":
            print("----------------- ZnCl4 - CALCULATION ------------------\n")
            print("Testing calculations on ZnCl4.")

            # taken from spreadsheet
            m_ratio = -0.0315100969
            m_Qlight = 2.6961634304
            m_Qheavy = 2.7301585764
            m_beta = 2.485049102

            l_filename = "tests/log_files/zinc/ZNCL4_B_64.LOG"
            h_filename = "tests/log_files/zinc/ZNCL4_B_66.LOG"
            linear_check = "n"

            test_calculation(
                l_filename,
                h_filename,
                linear_check,
                m_beta,
                m_ratio,
                m_Qlight,
                m_Qheavy,
            )
        else:
            print("Not running calculation tests on ZnCl4")
        h2o = input("Would you like to run the ZnH2O tests? [y/n]: ")
        if h2o == "y":
            print("----------------- ZnH2O - CALCULATION ------------------\n")
            print("Testing calculations on ZnH2O.")

            # taken from spreadsheet
            m_ratio = -0.0288207750
            m_Qlight = -140.4897585114
            m_Qheavy = -140.4570333614
            m_beta = 3.904374908

            l_filename = "tests/log_files/zinc/ZnH2O_A_Freq_64_Th.log"
            h_filename = "tests/log_files/zinc/ZnH2O_A_Freq_66_Th.log"
            linear_check = "n"

            test_calculation(
                l_filename,
                h_filename,
                linear_check,
                m_beta,
                m_ratio,
                m_Qlight,
                m_Qheavy,
            )
        else:
            print("Not running calculation tests on ZnH2O.")
    elif calc == "n":
        print("Not running calculation tests.")
    else:
        print("Unknown input. Exiting.")
        exit()
