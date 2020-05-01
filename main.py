# -*- coding: utf-8 -*-
"""
Created on December 13, 2019.

@author: Camilo Martínez
"""

import json
from ExceptionHandling import exceptions
from importlib import import_module
from os import name, system

import introduction

# True if the title of the log file has already been written.
TITLE_EXISTS = False

# Name of the JSON file which contains all the available options.
JSON_OPTIONS_FILE = "options.json"


def clear() -> None:
    """ Clears the console.
    """
    if name == 'nt':
        _ = system('cls')  # For windows.
    else:
        _ = system('clear')  # For mac and linux (here, os.name is 'posix').


def load_options() -> dict:
    """ Loads the options from a JSON file.

        The options are loaded into a dictionary thanks to the json module.
        Each option is a string, which is a key of the dictionary, and each
        key contains the following attributes:

        id : string
            An id to identify every function/option inside the key.
        name : string
            The user-friendly name of the function/option.
        function : string
            The name of the actual function, which can be a .cpp or .py name
            of file.
    
    Returns:
        dict: Contains the available options in dictionary format.
    """
    with open(JSON_OPTIONS_FILE) as f:
        data = json.load(f)

    return data


def main():
    """ Executes the app.

        Shows the available options the user has access to.
        The available options are loaded from a JSON file.
    """

    while True:
        clear()

        data = load_options()

        area, name, function = introduction.main(data['options'])

        clear()

        introduction.create_title(area + " -> " + name)

        import_module(area + '.' + function).main()

        print("")
        input("Press any key to continue...")
        clear()
    

print("")

if __name__ == "__main__":
    main()
