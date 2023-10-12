from copy import deepcopy
from typing import List, Union
import matplotlib.pyplot as plt

ISOTOPES = {
    "Ag": [[106.905095, 51.84], [108.904754, 48.16]],
    "Al": [[26.981541, 100.0]],
    "Ar": [[35.967546, 0.34], [37.962732, 0.063], [39.962383, 99.6]],
    "As": [[74.921596, 100.0]],
    "Au": [[196.96656, 100.0]],
    "B": [[10.012938, 19.8], [11.009305, 80.2]],
    "Ba": [
        [129.906277, 0.11],
        [131.905042, 0.1],
        [133.90449, 2.42],
        [134.905668, 6.59],
        [135.904556, 7.85],
        [136.905816, 11.23],
        [137.905236, 71.7],
    ],
    "Be": [[9.012183, 100.0]],
    "Bi": [[208.980388, 100.0]],
    "Br": [[78.918336, 50.69], [80.91629, 49.31]],
    "C": [[12.0, 98.9], [13.003355, 1.1]],
    "Ca": [
        [39.962591, 96.95],
        [41.958622, 0.65],
        [42.95877, 0.14],
        [43.955485, 2.086],
        [45.953689, 0.004],
        [47.952532, 0.19],
    ],
    "Cd": [
        [105.906461, 1.25],
        [107.904186, 0.89],
        [109.903007, 12.49],
        [110.904182, 12.8],
        [111.902761, 24.13],
        [112.904401, 12.22],
        [113.903361, 28.73],
        [115.904758, 7.49],
    ],
    "Ce": [
        [135.90714, 0.19],
        [137.905996, 0.25],
        [139.905442, 88.48],
        [141.909249, 11.08],
    ],
    "Cl": [[34.968853, 75.77], [36.965903, 24.23]],
    "Co": [[58.933198, 100.0]],
    "Cr": [[49.946046, 4.35], [51.94051, 83.79], [52.940651, 9.5], [53.938882, 2.36]],
    "Cs": [[132.905433, 100.0]],
    "Cu": [[62.929599, 69.17], [64.927792, 30.83]],
    "Dy": [
        [155.924287, 0.06],
        [157.924412, 0.1],
        [159.925203, 2.34],
        [160.926939, 18.9],
        [161.926805, 25.5],
        [162.928737, 24.9],
        [163.929183, 28.2],
    ],
    "Er": [
        [161.928787, 0.14],
        [163.929211, 1.61],
        [165.930305, 33.6],
        [166.932061, 22.95],
        [167.932383, 26.8],
        [169.935476, 14.9],
    ],
    "Eu": [[150.91986, 47.8], [152.921243, 52.2]],
    "F": [[18.998403, 100.0]],
    "Fe": [[53.939612, 5.8], [55.934939, 91.72], [56.935396, 2.2], [57.933278, 0.28]],
    "Ga": [[68.925581, 60.1], [70.924701, 39.9]],
    "Gd": [
        [151.919803, 0.2],
        [153.920876, 2.18],
        [154.822629, 14.8],
        [155.92213, 20.47],
        [156.923967, 15.65],
        [157.924111, 24.84],
        [159.927061, 21.86],
    ],
    "Ge": [
        [69.92425, 20.5],
        [71.92208, 27.4],
        [72.923464, 7.8],
        [73.921179, 36.5],
        [75.921403, 7.8],
    ],
    "H": [[1.007825, 99.99], [2.014102, 0.015]],
    "He": [[3.016029, 0.0001], [4.002603, 100.0]],
    "Hf": [
        [173.940065, 0.16],
        [175.94142, 5.2],
        [176.943233, 18.6],
        [177.94371, 27.1],
        [178.945827, 13.74],
        [179.946561, 35.2],
    ],
    "Hg": [
        [195.965812, 0.15],
        [197.96676, 10.1],
        [198.968269, 17.0],
        [199.968316, 23.1],
        [200.970293, 13.2],
        [201.970632, 29.65],
        [203.973481, 6.8],
    ],
    "Ho": [[164.930332, 100.0]],
    "I": [[126.904477, 100.0]],
    "In": [[112.904056, 4.3], [114.903875, 95.7]],
    "Ir": [[190.960603, 37.3], [192.962942, 62.7]],
    "K": [[38.963708, 93.2], [39.963999, 0.012], [40.961825, 6.73]],
    "Kr": [
        [77.920397, 0.35],
        [79.916375, 2.25],
        [81.913483, 11.6],
        [82.914134, 11.5],
        [83.911506, 57.0],
        [85.910614, 17.3],
    ],
    "La": [[137.907114, 0.09], [138.906355, 99.91]],
    "Li": [[6.015123, 7.42], [7.016005, 92.58]],
    "Lu": [[174.940785, 97.4], [175.942694, 2.6]],
    "Mg": [[23.985045, 78.9], [24.985839, 10.0], [25.982595, 11.1]],
    "Mn": [[54.938046, 100.0]],
    "Mo": [
        [99.907473, 9.63],
        [91.906809, 14.84],
        [93.905086, 9.25],
        [94.905838, 15.92],
        [95.904676, 16.68],
        [96.906018, 9.55],
        [97.905405, 24.13],
    ],
    "N": [[14.003074, 99.63], [15.000109, 0.37]],
    "Na": [[22.98977, 100.0]],
    "Nb": [[92.906378, 100.0]],
    "Nd": [
        [141.907731, 27.13],
        [142.909823, 12.18],
        [143.910096, 23.8],
        [144.912582, 8.3],
        [145.913126, 17.19],
        [147.916901, 5.76],
        [149.9209, 5.64],
    ],
    "Ne": [[19.992439, 90.6], [20.993845, 0.26], [21.991384, 9.2]],
    "Ni": [
        [57.935347, 68.27],
        [59.930789, 26.1],
        [60.931059, 1.13],
        [61.928346, 3.59],
        [63.927968, 0.91],
    ],
    "O": [[15.994915, 99.76], [16.999131, 0.038], [17.999159, 0.2]],
    "Os": [
        [183.952514, 0.02],
        [185.953852, 1.58],
        [186.955762, 1.6],
        [187.95585, 13.3],
        [188.958156, 16.1],
        [189.958455, 26.4],
        [191.961487, 41.0],
    ],
    "P": [[30.973763, 100.0]],
    "Pb": [
        [203.973037, 1.4],
        [205.974455, 24.1],
        [206.975885, 22.1],
        [207.976641, 52.4],
    ],
    "Pd": [
        [101.905609, 1.02],
        [103.904026, 11.14],
        [104.905075, 22.33],
        [105.903475, 27.33],
        [107.903894, 26.46],
        [109.905169, 11.72],
    ],
    "Pr": [[140.907657, 100.0]],
    "Pt": [
        [189.959937, 0.01],
        [191.961049, 0.79],
        [193.962679, 32.9],
        [194.964785, 33.8],
        [195.964947, 25.3],
        [197.967879, 7.2],
    ],
    "Rb": [[84.9118, 72.17], [86.909184, 27.84]],
    "Re": [[184.952977, 37.4], [186.955765, 62.6]],
    "Rh": [[102.905503, 100.0]],
    "Ru": [
        [99.904218, 12.6],
        [100.905581, 17.0],
        [101.904348, 31.6],
        [103.905422, 18.7],
        [95.907596, 5.52],
        [97.905287, 1.88],
        [98.905937, 12.7],
    ],
    "S": [[31.972072, 95.02], [32.971459, 0.75], [33.967868, 4.21], [35.967079, 0.02]],
    "Sb": [[120.903824, 57.3], [122.904222, 42.7]],
    "Sc": [[44.955914, 100.0]],
    "Se": [
        [73.922477, 0.9],
        [75.919207, 9.0],
        [76.919908, 7.6],
        [77.917304, 23.5],
        [79.916521, 49.6],
        [81.916709, 9.4],
    ],
    "Si": [[27.976928, 92.23], [28.976496, 4.67], [29.973772, 3.1]],
    "Sm": [
        [143.912009, 3.1],
        [146.914907, 15.0],
        [147.914832, 11.3],
        [148.917193, 13.8],
        [149.917285, 7.4],
        [151.919741, 26.7],
        [153.922218, 22.7],
    ],
    "Sn": [
        [111.904826, 0.97],
        [113.902784, 0.65],
        [114.903348, 0.36],
        [115.901744, 14.7],
        [116.902954, 7.7],
        [117.901607, 24.3],
        [118.90331, 8.6],
        [119.902199, 32.4],
        [121.90344, 4.6],
        [123.905271, 5.6],
    ],
    "Sr": [[83.913428, 0.56], [85.909273, 9.86], [86.908902, 7.0], [87.905625, 82.58]],
    "Ta": [[179.947489, 0.012], [180.948014, 99.99]],
    "Tb": [[158.92535, 100.0]],
    "Te": [
        [119.904021, 0.096],
        [121.903055, 2.6],
        [122.904278, 0.91],
        [123.902825, 4.82],
        [124.904435, 7.14],
        [125.90331, 18.95],
        [127.904464, 31.69],
        [129.906229, 33.8],
    ],
    "Th": [[232.038054, 100.0]],
    "Ti": [
        [45.952633, 8.0],
        [46.951765, 7.3],
        [47.947947, 73.8],
        [48.947871, 5.5],
        [49.944786, 5.4],
    ],
    "Tl": [[202.972336, 29.52], [204.97441, 70.48]],
    "Tm": [[168.934225, 100.0]],
    "U": [[234.040947, 0.006], [235.043925, 0.72], [238.050786, 99.27]],
    "V": [[49.947161, 0.25], [50.943963, 99.75]],
    "W": [
        [179.946727, 0.13],
        [181.948225, 26.3],
        [182.950245, 14.3],
        [183.950953, 30.67],
        [185.954377, 28.6],
    ],
    "Xe": [
        [123.905894, 0.1],
        [125.904281, 0.09],
        [127.903531, 1.91],
        [128.90478, 26.4],
        [129.90351, 4.1],
        [130.905076, 21.2],
        [131.904148, 26.9],
        [133.905395, 10.4],
        [135.907219, 8.9],
    ],
    "Y": [[88.905856, 100.0]],
    "Yb": [
        [167.933908, 0.13],
        [169.934774, 3.05],
        [170.936338, 14.3],
        [171.936393, 21.9],
        [172.938222, 16.12],
        [173.938873, 31.8],
        [175.942576, 12.7],
    ],
    "Zn": [
        [63.929145, 48.6],
        [65.926035, 27.9],
        [66.927129, 4.1],
        [67.924846, 18.8],
        [69.925325, 0.6],
    ],
    "Zr": [
        [89.904708, 51.45],
        [90.905644, 11.27],
        [91.905039, 17.17],
        [93.906319, 17.33],
        [95.908272, 2.78],
    ],
}


def ischar(character: str) -> bool:
    """
    Check whether a character represents a letter or a number.

    Arguments
    ---------
    character: str
        The string containing the character to be tested.

    Returns
    -------
    bool
        True if the character is a letter, False if the character is a number.
    """
    return False if character in "0123456789" else True


def isupper(character: str) -> bool:
    """
    Check whether a character is uppercase or not.

    Arguments
    ---------
    character: str
        The string containing the character to be tested.

    Returns
    -------
    bool
        True if the character is uppercase else False.
    """
    return True if character in "ABCDEFGHIJKLMNOPQRSTUWXYZ" else False


def parse_formula(formula: str) -> List[List[Union[str, int]]]:
    """
    Parse a brute formula extracting a list of lists encoding the element (key) type and
    the number (item) of atoms of that type in the molecule.

    Arguments
    ---------
    formula: str
        The string econding the brute formula of the compound.

    Returns
    -------
    List[List[Union[str, int]]]
        The list of lists encoding the composition of the molecule. The first element of each
        couple encodes the element while the values the number of that type of atom in the molecule.
    """

    # Parse the string dividing the atom symbol from the number of
    # atoms using , and the different atom types with ;
    new_peaks = ""
    for i, c in enumerate(formula):
        # Check if the end of the formula string is reached and copy the last character
        if i + 1 == len(formula):
            new_peaks += f"{c}"

        # Detect the switch between characters and numbers to add the proper separator (, or ;)
        elif ischar(c) != ischar(formula[i + 1]):
            new_peaks += f"{c};" if not ischar(c) else f"{c},"

        # Detect two adjacent element with lower and upper case characters
        elif not isupper(c) and ischar(formula[i + 1]):
            new_peaks += f"{c},1;"

        # Detect two adjacent uppercase element symbols
        elif isupper(c) and isupper(formula[i + 1]):
            new_peaks += f"{c},1;"

        else:
            new_peaks += f"{c}"

    if ischar(new_peaks[-1]):
        new_peaks += ",1"

    composition = []
    for field in new_peaks.split(";"):
        element, number = field.split(",")
        composition.append([element, int(number)])

    return composition


def process(
    composition: List[List[Union[str, int]]],
    equivalent: float = 1e-6,
    dump: float = 1e-10,
    normalize: bool = False,
) -> List[List[float]]:
    """
    Run an iterative procedure to evaluate all the possible combinations of isotopes
    masses.

    Arguments
    ---------
    composition: List[List[Union[str, int]]]
        The disctionary encoding the composition of the molecule.
    equivalent: float
        The threshold in a.m.u under which the masses are considered equivalent.
    dump: float
        The abbundance threshold under which a given combination is discarded.
    normalize: bool
        If set to False (default) will return the percentage abbundance else it will
        set the largest peak to 100.

    Returns
    -------
    List[List[float]]
        The list of lists encoding the mass and abbundance of each peak.
    """

    # Start the iterative process from the first element block of the composition
    element, number = composition[0]
    reminder = [] if len(composition) == 1 else composition[1::]

    # If the current block contains only one atom pass directly the reminder to the next iteration
    if number == 1 and reminder != []:
        new = reminder

    # If the current block contains only one atom and is the last one return its isotopes.
    elif number == 1:
        isotopes = ISOTOPES[element]
        return isotopes

    # If the block is generic pass the composition to the next iteration subtracting one atom form the current block.
    else:
        new = [[element, number - 1]]
        for b in reminder:
            new.append(b)

    # Call the next iteration on the reduced block
    peaks = process(new)

    # Obtain all the isotopes of the current element
    isotopes = ISOTOPES[element]

    # Create a new split combining the mass peaks of the next iteration with the isotopes of the current element.
    new_peaks = []
    for isotope in isotopes:
        for peak in peaks:
            mass = peak[0] + isotope[0]
            abbundance = peak[1] * isotope[1] / 100

            # Drop all the peaks with abbundances lower than the dump threshold
            if abbundance / 100 < dump:
                continue

            # Append the new peak to the list
            new_peaks.append([mass, abbundance])

    # Eliminate duplicates of the same mass values
    peaks = []
    for peak in new_peaks:
        masses = [p[0] for p in peaks]
        for i, mass in enumerate(masses):
            if abs(peak[0] - mass) / mass < equivalent:
                peaks[i][1] += peak[1]
                break
        else:
            peaks.append(peak)

    # If required normalize the peaks by the largest one
    if normalize is True:
        maximum = max([p[1] for p in peaks])
        new_peaks = deepcopy(peaks)
        for i, _ in enumerate(peaks):
            new_peaks[i][1] *= 100 / maximum
        return new_peaks

    return peaks


if __name__ == "__main__":
    formula = input("Enter the brute formula of the compound: ")

    composition = parse_formula(formula)
    peaks = process(composition, normalize=True)

    masses = [peak[0] for peak in peaks]
    intensities = [peak[1] for peak in peaks]

    print("\n  Mass (amu) | Intensity  ")
    print("--------------------------")
    for mass, intensity in zip(masses, intensities):
        print("{0:>12} | {1:>6}".format(f"{mass:.6f}", f"{intensity:.4e}"))

    plt.figure(figsize=(8, 5))

    plt.stem(masses, intensities, basefmt="none", markerfmt="none")
    plt.ylim([0, 105])

    plt.xlabel("Mass [amu]")
    plt.ylabel("Intensity [a.u.]")

    plt.savefig(f"exact_mass_{formula}.png", dpi=600)
    plt.show()
