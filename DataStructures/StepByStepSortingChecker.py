# -*- coding: utf-8 -*-
"""
Created on April 11, 2020.

@author: Camilo Martínez
"""
from EntryManager import EntryManager
from DataStructures.SortingAlgorithms import HeapSort, SelectionSort

# Entry manager. Required to handle user input.
Entry_Manager = EntryManager(__file__)

class Checker:

    @staticmethod
    def show_step_by_step(array: list, sorting_algorithm: str = 'heapsort') -> None:
        if sorting_algorithm == "heapsort":
            HeapSort.sort(array)
        elif sorting_algorithm == "selectionsort":
            SelectionSort.sort(array)

def main():
    sorting_algorithm = Entry_Manager.get_str_input("Sorting algorithm", ["heapsort", "selectionsort"], "heapsort")
    type_value = Entry_Manager.get_str_input("Define the type of array", ["str", "float", "int", "mixed"], "float")
    array = Entry_Manager.get_list("Define your array", type_value)
    print("")
    Checker.show_step_by_step(array, sorting_algorithm)