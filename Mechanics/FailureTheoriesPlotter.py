# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:35:58 2020

@author: Camilo Martínez
"""
from Mechanics import FailureTheories
from os.path import basename, isfile, splitext
from os import getcwd, listdir
from ExceptionHandling import exceptions
from EntryManager import EntryManager
from typing import List, Tuple, Union
from adjustText import adjust_text
from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rcParams['font.family'] = "cmr10"
rcParams['axes.unicode_minus'] = False
rcParams.update({'font.size': 13})
    
# Entry manager. Required to handle user input.
Entry_Manager = EntryManager(__file__)

class FailureTheoriesPlotter:
    """ Plots the complete diagram of failure theories according to the parameters provided.
    """
    def __init__(self, Sy: float, sigmas: List[Tuple[float, float]], St: float, Sc: float, units: str, names: List[str]) -> None:
        """       
        Args:
            Sy (float): Yield strength of material.
            sigmas (List[tuple]): List of tuples which corresponds to x, y coordinates of stress states.
            St (float): Tensile yield strength of material.
            Sc (float): Compressive yield strength of material.
            names (List[str], optional): List of names for each x, y in sigmas (list).
        """
        self.MSST = FailureTheories.MaximumShearStress(Sy, St, Sc, 'MSST')
        self.DET = FailureTheories.DistortionEnergy(Sy, St, Sc, 'DET')
        self.CMT = FailureTheories.CoulombMohr(Sy, St, Sc, 'MCT')
        self.stress_conditions = sigmas
        self.names = names
        self.units = units
        
    def plot(self):
        """ Plots the diagram of failure theories.
        """
        colors = ['r', 'b', 'k']
        plt.figure(figsize=(8, 6), dpi=80)
        added_label = False
        for i, failureTheory in enumerate([self.MSST, self.DET, self.CMT]):
            for eqn in failureTheory.no_failure_region_equations():
                if failureTheory.label == 'MSST':
                    ls = '--'
                elif failureTheory.label == 'MCT':
                    ls = ':'
                else:
                    ls = '-'
                    
                if eqn[0] == 'HorizontalLine':
                    if not added_label:
                        plt.hlines(eqn[1], eqn[2], eqn[3], linestyle=ls, colors=colors[i], label=failureTheory.label)
                        added_label = True
                    else:
                        plt.hlines(eqn[1], eqn[2], eqn[3], linestyle=ls, colors=colors[i])                        
                elif eqn[0] == 'VerticalLine':
                    plt.vlines(eqn[1], eqn[2], eqn[3], linestyle=ls, colors=colors[i])
                elif eqn[0] == 'Equation':
                    x = np.arange(eqn[2], eqn[3], 0.1)
                    p = np.poly1d(eqn[1])
                    y = p(x)
                    plt.plot(x, y, color=colors[i], linestyle=ls)
                elif eqn[0] == 'Ellipse':
                    ellipse = eqn[1]
                    plt.plot(ellipse[0,:], ellipse[1,:], label=failureTheory.label, linestyle=ls)
                    
            added_label = False
        
        if self.stress_conditions is not None:
            x_sc, y_sc = tuple(zip(*self.stress_conditions))
            plot_sc = []
            
            for i in range(len(x_sc)):
                plot_sc.append(plt.scatter(x_sc[i], y_sc[i]))
            
            if self.names is not None:
                legend1 = plt.legend(plot_sc, ['x = ' + str(self.names[i]) + ' m' for i in range(len(self.names))], loc='lower right')
                plt.gca().add_artist(legend1)

        plt.xlabel('$\sigma_1$ [' + self.units + ']')
        plt.ylabel('$\sigma_2$ [' + self.units + ']')
        plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.2)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.1)
        plt.minorticks_on()
        plt.legend(loc='upper left')
        plt.savefig('Grafica.jpg', dpi=1200)
        plt.show()

def get_material_properties() -> Tuple[float, float, float]:
    """ Gets the properties of the material.
        Sy: Yield strength, St: Tensile yield strength, Sc: Compressive yield strength.
    
    Returns:
        Tuple[float, float, float]: First element is Sy; second, St; and third, Sc.
    """
    Sy = Entry_Manager.get_simple_numerical_entry("\tYield strength of material, Sy", "float", '+')
    St = Entry_Manager.get_simple_numerical_entry("\tTensile yield strength of material (DF = Sy), St", "float", '+', Sy)
    Sc = Entry_Manager.get_simple_numerical_entry("\tCompressive yield strength of material (DF = Sy), Sc", "float", '+', Sy)
    return (Sy, St, Sc)

def get_stress_states_input_option(show_title: bool, show_options: bool = True) -> str:
    """ Gets the option from the user regarding the way (s)he wants to input
        stress states.

    Args:
        show_title (bool): True if the title is to be shown.
        show_options (bool, optional): True if options are to be displayed.

    Returns:
        str: 1, 2 or 3.
    """
    title = "Please select one of the following options to input stress states:"
    options = "\t1. I want to input them manually.\n\t2. I have a file with the data.\n\t3. I don't want to input any stress state!"

    option = Entry_Manager.get_menu_option(title, options, [1, 2, 3], True, True)
    return option

def get_stress_states_and_names() -> Union[Tuple[List[Tuple[float, float]], List[str]], None]:
    """ Gets the stress states manually or from a file.
    
    Returns:
        List[Tuple[float, float]]: List of tuples which corresponds to x, y coordinates of stress states.
    """
    option = get_stress_states_input_option(True)
    ss = list()
    names = None
    if option == 1:
        print("")
        n = Entry_Manager.get_simple_numerical_entry("Number of stress states", "int", '+', __file__)
        print("")
        print("Separate each value by a comma (,) and a space, i.e, 24.52, 3.4: ")
        ss = Entry_Manager.get_list_of_tuples("Stress state", n, "float")
    elif option == 2:
        print("\nPlease copy and paste your data file inside the current directory, which is: ")
        print(getcwd())
        print("... and NAME IT 'data'.")
        print("\nKeep in mind the file must have the following format:")
        print("[Maximum principal stress]  [Minimum principal stress] [name (optional)]")
        print("\nAnd the data types supported are: xlsx, xls, txt, csv")
        input("\nPress any key to continue...")
        print("")

        # Reads which files are inside the current directory.
        files = [f for f in listdir('.') if isfile(f)]
        if files:
            filetype = ""
            for f in files:
                if splitext(basename(f))[0] == "data":
                    try:
                        t = f.split(".")
                        filetype = t[1]
                        break
                    except:
                        print("Your data file does not have an extension, but we'll try to read it anyways.")
                        e = exceptions.InvalidFileExtensionError("'data' doesn't have a file extension.", basename(__file__))
                        del e
            
            print("Your data file was found!")
            
            import pandas as pd
            if filetype == "txt" or filetype == "csv" or filetype == "":
                separator = input("Separator used in your file (press enter if default), i.e, \, //, ;, etc.: ")
                if separator.strip() == "":
                    df = pd.read_csv('data.' + filetype, header=None)
                else:
                    df = pd.read_csv('data.txt', sep=separator, header=None)
            elif filetype == "xlsx" or filetype == "xls":
                df = pd.read_excel('data.' + filetype)
            else:
                print("Your data file has an unsupported file extension. Please try again after changing it.")
                e = exceptions.InvalidFileExtensionError("'data' has an unsupported file extension: " + filetype, \
                    basename(__file__))
                del e
                option = get_stress_states_input_option(True)

            if len(df.columns) == 2:
                df.columns = ["S1", "S2"]
            elif len(df.columns) == 3:
                df.columns = ["S1", "S2", "names"]
                names = df["names"]
            else:
                print("\nCheck your data file format. We found " + str(len(df.columns)) + " but must be 2 or 3.")
                ef = exceptions.InvalidFileFormatError("data file has invalid format. Expected number of columns" \
                        ": 3 and got: " + str(len(df.columns)))
                del ef
                option = get_stress_states_input_option(True)

            i = 0
            while i < len(df["S1"]) and i < len(df["S2"]):
                ss.append((float(df["S1"][i]), float(df["S2"][i])))
                i += 1
        else:
            print("It seems you didn't put your data file inside the current directory. Please, try again!")
            ef = exceptions.InvalidFileFormatError("data file not found in current directory.")
            del ef
            option = get_stress_states_input_option(True)
    elif option == 3:
        return (None, None)
    else:
        print("That is not a valid option.")
        print("")
        option = get_stress_states_input_option(False)
    
    return (ss, names)

def main():
    """ Plots the failure theories diagram. It allows the user to input stress states and its names
        to customize the plot.
    """
    print("* Please, input valid data at all times! *\n")
    units = input("Units (MPa, psi, ksi, etc.): ")
    print("\nMaterial properties:")
    print("* Press enter if DF, i.e, default value, is to be used. *\n")
    Sy, St, Sc = get_material_properties()
    print("")
    stress_states, names = get_stress_states_and_names()
    print("\nLoading theories...")
    FTP = FailureTheoriesPlotter(Sy, stress_states, St, Sc, units, names)
    print("\nPlotting the diagram...")
    FTP.plot()
    print("\nYour plot was saved inside the current directory. Go check it out!")