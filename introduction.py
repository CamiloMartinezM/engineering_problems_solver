# -*- coding: utf-8 -*-
"""
Created on December 13, 2019.

@author: Camilo Martínez
"""

from ExceptionHandling import exceptions
from typing import Tuple
import give_console_width

# Console width of the current/active console.
CONSOLE_WIDTH = give_console_width.main()

# Dictionary of available options in the following format:
# {"[Real_ID]": {"Area": key,
#                "Name": option['name'],
#                "Function": option['function']}
# Where Real_ID takes into account the number of the
# upper level where the nested option is.
AVAILABLE_OPTIONS = dict()


def create_title(title: str) -> None:
    """ Creates a proper title.
    
    Args:
        title (str): Title of the program.
    """
    print("~" * CONSOLE_WIDTH)
    print(" " * int(str((CONSOLE_WIDTH - len(title))//2)) +
          title + " " * int(str((CONSOLE_WIDTH - len(title))//2)))
    print("~" * CONSOLE_WIDTH)
    print("")


def show_option(cont: int, id_: int, name: str) -> None:
    """ Show the option in an user-friendly way.
    
    Args:
        cont (int): Number of the upper menu, i.e, area of the option.
        Example: Calculus, Linear Algebra.description]
        id_ (int): Number of the lower menu, i.e, specific function.
        name (str): Name of the function.
    """
    print("\t" + str(cont + id_) + ". " + name + ".")


def take_option() -> str:
    """ Algorithm that takes the option of the user.
    
    Returns:
        str: The selected option.
    """
    option = input("Option: ")
    return option


def look_up_option(option: float) -> Tuple[str, str, str]:
    """ Looks up the option given by parameter.

        This method looks for the option given by parameter inside
        the list of available options.    
    
    Args:
        option (float): Option the user asked for.
    
    Raises:
        e (OptionNotFoundError): This method raises this error when the option was not found,
        i.e, it is not one of the available options.
    
    Returns:
        Tuple[str, str, str]: Tuple of 3 strs, which are:
            Area : str
                Area of the picked option.
            Name : str
                Name of the option.
            Function : str
                Actual name of the function, which gets called to
                execute what the user wants. 
    """
    if str(option) in AVAILABLE_OPTIONS.keys():
        return (AVAILABLE_OPTIONS[str(option)]['Area'],
                AVAILABLE_OPTIONS[str(option)]['Name'],
                AVAILABLE_OPTIONS[str(option)]['Function'])
    else:
        e = exceptions.OptionNotFoundError(
            "Picked option " + str(option) + " not found.")
        raise e


def main(options: dict) -> None:
    """ Shows the available options of the program.
    
    Args:
        options (dict): Available options to show the user. Options must be
        in the following dictionary format:

        {
            "[name of area 1]": [
                {
                    "id": _, 
                    "name": _, 
                    "function": _
                },
                {
                    ...
                }
            ],
            "[name of area 2]": [
                {
                    ...
                }
            ], 
            ...
        }
    """
    title = "University tools and solvers, by Camilo Martínez"

    create_title(title)

    cont = 1
    for key in options.keys():
        print(str(cont) + ". " + key + ".")
        for option in options[key]:
            show_option(cont, option['id'], option['name'])
            AVAILABLE_OPTIONS[str(cont + option['id'])] = {"Area": key,
                                                           "Name": option['name'],
                                                           "Function": option['function']}

        cont += 1
        
    print("Q. Quit.")
    print("")
    print("~" * CONSOLE_WIDTH)

    while True:
        picked_option = take_option().lower()
        
        if picked_option in ['quit', 'q']: # Exits the program.
            import sys
            print("\nBye! Glad I could be of service.\n")
            sys.exit(0)
        
        try:
            area, name, function = look_up_option(picked_option)
            return area, name, function
        except exceptions.OptionNotFoundError:
            print("[*] That option does not exist. Please, try again.")
            print("")
