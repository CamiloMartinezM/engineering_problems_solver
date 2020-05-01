# -*- coding: utf-8 -*-
"""
Created on December 14, 2019.

@author: Camilo Martínez
"""
from ExceptionHandling import exceptions


def main() -> list:
    """ Main method.

        Obtains a matrix given by the user.

        Returns
        -------
            matrix : list
                Matrix input by the user in the form of a list of lists.
    """
    # try-except in case an entered value is invalid.
    exception_ocurred = True
    while exception_ocurred:
        try:
            n = int(input("Dimension (example: 2 -> Gives a 2x2 matrix) = "))
            exception_ocurred = False
        except:
            print("Invalid entry!")

    print("")
    print("Matrix " + str(n) + "x" + str(n) + ":")

    # Loop that creates the rows of the matrix as a list.
    i = 0
    matrix = []

    while i < n:
        try:
            try:
                str_presentRow = []

                str_row = input("-> Row #" + str(i + 1) + ": ")

                str_presentRow = str_row.split(" ")

                presentRow = [float(x) for x in str_presentRow]
            except:
                e = exceptions.InvalidEntryError("Invalid entry: " + str_row, )
                raise e

            if len(presentRow) == n:
                matrix.append(presentRow)
                i += 1
            else:
                e = exceptions.InvalidEntryError(
                    "The number of given values is different from the matrix dimension.")
                raise e
        except exceptions.InvalidEntryError as e:
            print(e.message)

    return matrix
