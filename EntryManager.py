# -*- coding: utf-8 -*-
"""
Created on April 8, 2020.

@author: Camilo Martínez
"""
from typing import Union, List, Tuple
from ExceptionHandling import exceptions
from os.path import basename

class EntryManager:
    """ Powerful manager to get and parse entries made by the user. In case there is an exception,
        it is logged on with the help of ExceptionHandling.
    """
    def __init__(self, filename: str = None) -> None:
        self.file__ = basename(filename) if filename is not None else basename(__file__)

    def get_simple_numerical_entry(self, msg: str, type_value: str, sign: str = '+', default_value: Union[int, float] = None) -> float:
        """ Gets an entry from the user and parses it to int or float depending on type_value parameter.
        
        Args:
            msg (str): Message to be shown before the user inputs a value.
            type_value (str): int or float.
            sign (str): '+' if a positive non-zero value is to be expected. '-' otherwise.
            default_value (Union[int, float], optional): Default value of variable. Defaults to None.
        
        Returns:
            float, int: Entry made by the user.
        """
        entry_str = ""
        entry = None
        try:
            entry_str = input(msg + ' = ')
            if entry_str.strip() == "" and default_value is not None:
                entry = default_value
            elif entry_str.strip() == "":
                raise Exception("Empty string")
            else:
                if type_value == "float":
                    entry = float(entry_str)  
                elif type_value == "int":
                    entry = int(entry_str)
            
            if entry <= 0 and sign == '+':
                raise Exception("Expected a positive non-zero value.")
        except Exception as e:
            if e.__cause__ is None:
                ef = exceptions.InvalidEntryError("Invalid entry, could not perform parsing. Expected: " + type_value + \
                    sign + " and got: " + entry_str, self.file__)
            else:
                ef = exceptions.InvalidEntryError("Invalid entry, could not perform parsing. Expected: " + type_value + \
                    sign + ". Original message: " + e.__cause__, self.file__)
            del ef
            # Recursion till entry receives a valid value.
            entry = self.get_simple_numerical_entry(msg, type_value, sign, default_value)
        
        return entry

    def get_menu_option(self, title: str, options: str, valid_options: List[int], show_title: bool = True, show_options: bool = True) -> int:
        """ Gets a menu options and parses it to int. It continues to call itself recursively until the
            user inputs a valid entry.
        
        Args:
            title (str): Title of the menu.
            options (str): String which has all valid options and its descriptions.
            valid_options (List[int]): List of integers with the possible options.
            show_title (bool, optional): Defaults to True.
            show_options (bool, optional): Defaults to True.
        
        Returns:
            int: Option inputted by the user.
        """
        if show_title:
            print(title + '\n')
        if show_options:
            print(options + '\n')

        option_str = input("Option: ")
        option = None
        if option_str.strip() not in [str(i) for i in valid_options]:
            ef = exceptions.InvalidEntryError("Invalid entry. Expected any of: " + str(valid_options) \
                 + " and got: " + option_str, basename(__file__))
            option = self.get_menu_option(title, options, valid_options, False, False)
            del ef
        else:
            option = int(option_str)

        return option

    def get_list_of_tuples(self, input_name: str, n: int, type_value: str = "float", type_values: List[str] = None, unpack_n: int = 2) -> List[Tuple[Union[float, int]]]:
        """ Gets a list of tuples inputted by the user. Supported type values are: float, int and str.
        
        Args:
            input_name (str): Name of the coordinate or message to be shown before the user inputs a value.
            n (int): Number of expected entries.
            type_value (str, optional): Type value of all elements. Defaults to "float". If it is None, that
                                        means that not all elements have the same type value. Therefore,
                                        type_values is used.
            type_values (List[str], optional): If type_value is None, then type_values must not be None.
                                               This a list of strs where each i-th element corresponds to
                                               the type value of the i-th element to unpack, where 
                                               0 <= i < unpack_n
            unpack_n (int, optional): Number of elements to unpack. Defaults to 2.
        
        Returns:
            List[Tuple[Union[float, int]]]: [description]
        """
        l = list()
        # Gets each x, y tuple and appends it to ss.
        for i in range(n):
            exception_occurred = True
            while exception_occurred: # Continues looping as long as there is an invalid entry.
                str_x_y = input('\t' + input_name + " " + str(i+1) + ": ")
                try:
                    raw_list = str_x_y.split(", ")
                    if len(raw_list) != unpack_n: # The number of values to unpack must be unpack_n
                        error_message = "\tThe number of values separated by a comma must be " + str(unpack_n)
                        print(error_message + ".")
                        e = exceptions.InvalidEntryError(error_message, self.file__)
                        del e
                    else:
                        if type_value is not None:
                            try: # x and y must be float or int.
                                if type_value == "float":
                                    t = tuple(float(x) for x in raw_list)
                                elif type_value == "int":
                                    t = tuple(int(x) for x in raw_list)
                                else: # type_value is "str".
                                    t = tuple(raw_list)
                                l.append(tuple(t))
                                exception_occurred = False
                            except:
                                error_message = "\tInvalid entry. Expected: " + type_value
                                print(error_message + ".")
                                e = exceptions.InvalidEntryError(error_message + " and got: " + raw_list, self.file__)
                                exception_occurred = True
                                del e
                        else:
                            t = list()
                            for i in range(unpack_n):
                                try:
                                    if type_values[i] == "float":
                                        current_value = float(raw_list[i])
                                    elif type_value[i] == "int":
                                        current_value = int(raw_list[i])
                                    else: # type_value[i] is str.
                                        current_value = raw_list[i]
                                    t.append(current_value)
                                    exception_occurred = False
                                except:
                                    error_message = "Invalid entry. Expected: " + type_value[i] + " and got " + raw_list[i] + \
                                        " in position " + str(i) 
                                    print(error_message + ".")
                                    e = exceptions.InvalidEntryError(error_message, self.file__)
                                    exception_occurred = True
                                    del e
                            l.append(tuple(t))
                except Exception as e:
                    if e.__cause__ is not None:
                        ef = exceptions.Bug("An unexpected error ocurred. Original message: " + e.__cause__, self.file__)
                    else:
                        ef = exceptions.Bug("An unexpected error ocurred.", self.file__)
                    del ef
        return l

    def get_str_input(self, msg: str, valid_inputs: list, default: str = None) -> str:
        complete_msg = msg + " (" + str(valid_inputs)[1:-1]

        if default is not None:
            complete_msg += ", Default: '" + default + "'"
        
        complete_msg += "): "

        raw_str = input(complete_msg)

        if raw_str.strip() == "" and default is not None:
            return default

        if raw_str.strip().lower() not in valid_inputs:
            error_message = "Invalid entry. Expected any of: " + str(valid_inputs) + " and got: " + raw_str
            ef = exceptions.InvalidEntryError(error_message, basename(__file__))
            print(error_message + ".")
            del ef
            raw_str = self.get_str_input(msg, valid_inputs)

        return raw_str.strip().lower()

    def get_list(self, msg: str, type_value: str = 'str') -> list:
        raw_str = input(msg + ": ")
        raw_list = raw_str.split(" ")
        l = list()

        if type_value == "str" or type_value == "mixed":
            l = raw_list

        try:
            if type_value == "float":
                l = [float(char) for char in raw_list]
            elif type_value == "int":
                l = [int(char) for char in raw_list]
        except:
            error_message = "\tInvalid entry. Expected: " + type_value
            print(error_message + ".")
            e = exceptions.InvalidEntryError(error_message + " and got: " + str(raw_list), self.file__)
            l = self.get_list(msg, type_value)
            del e

        return l