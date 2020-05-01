# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:35:58 2020

@author: Camilo Martínez
"""
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

class ShearAndMomentsPlotter:
    """ Plots the complete diagram of failure theories according to the parameters provided.
    """
    def __init__(self, units_x: str, units_f: str, forces: Tuple[float, float]) -> None:
        self.forces = forces
        self.units_x = units_x
        self.units_f = units_f
        self.equations = self.build_equations()
        
    def build_equations(self) -> list:
        eqns = list()
        previous_f = 0
        for i in range(len(self.forces)):
            x, f = self.forces[i]
            if i < len(self.forces) - 1:
                next_x, next_f = self.forces[i+1]
            else:
                next_x, next_f = 0, 0

            eqns.append(['HorizontalLine', x, next_x, f + previous_f])
            eqns.append(['VerticalLine', previous_f + f, f + next_f, x])
            previous_f = f
        
        return eqns

    def plot(self):
        """ Plots the diagram of failure theories.
        """
        color = 'k'
        plt.figure(figsize=(8, 6), dpi=80)
        for eqn in self.equations:        
            if eqn[0] == 'HorizontalLine':
                plt.hlines(eqn[3], eqn[1], eqn[2], colors=color)                        
            elif eqn[0] == 'VerticalLine':
                ymin, ymax = min(eqn[1], eqn[2]), max(eqn[1], eqn[2])
                plt.vlines(eqn[3], ymin, ymax, colors=color)

        xticks, yticks = tuple(zip(*self.forces))
        plt.xlim(left=0)
        plt.xticks(xticks)
        # plt.yticks(yticks)
        plt.xlabel('x [' + self.units_x + ']')
        plt.ylabel('F [' + self.units_f + ']')
        plt.grid(b=True, which='major', color='k', linestyle='-', alpha=0.2)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.1)
        plt.minorticks_on()
        plt.savefig('Grafica.jpg', dpi=1200)
        plt.show()

    @classmethod
    def get_forces(cls):
        """ Gets the stress states manually or from a file.
        
        Returns:
            List[Tuple[float, float]]: List of tuples which corresponds to x, y coordinates of stress states.
        """
        print("")
        n = Entry_Manager.get_simple_numerical_entry("Number of forces", "int", '+', __file__)
        print("")
        print("Separate each value by a comma (,) and a space, i.e, 24.52, 3.4: ")
        forces = Entry_Manager.get_list_of_tuples("Position and magnitude of force", n, "float")
        return forces

def main():
    """ Plots the failure theories diagram. It allows the user to input stress states and its names
        to customize the plot.
    """
    print("* Please, input valid data at all times! *\n")
    units_f = input("Unit of force (N, lbf): ")
    units_x = input("Unit of distance (m, in): ")
    forces = ShearAndMomentsPlotter.get_forces()
    print("\nLoading equations...")
    FTP = ShearAndMomentsPlotter(units_x, units_f, forces)
    print("\nPlotting the diagram...")
    FTP.plot()
    print("\nYour plot was saved inside the current directory. Go check it out!")