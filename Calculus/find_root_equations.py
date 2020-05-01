# -*- coding: utf-8 -*-
"""
Finds the roots of a certain function with Newton's, bisection or secant method.

Created on December 13, 2019.

@author: Camilo Martínez
"""
from math import *

from ExceptionHandling import exceptions
from random import randint


def find_root_newton(argument: str, start_point: float, tolerance: float, max_iterations: int) -> float:
    """	Finds the root a function using Newton's method.

        Parameters
        ----------
        argument : str
            Argument as a function of x.

        start_point : float
            Initial guess of the root. Starting point to look for roots.

        tolerance : float
            Indicates how accurate the root must be.

        max_iterations : int
            Number of iterations for each of the methods of finding the root.

        Returns
        -------
        x : float
            Root of the function.

    """
    dx = 0.00000001
    x = start_point
    iterations = 1

    # Newton's method.
    while iterations < max_iterations:
        # Derivative of the function in x.
        df = (f(x+dx, argument) - f(x, argument))/dx
        x1 = x - f(x, argument)/df
        t = abs(x1 - x)
        if t < tolerance:
            break
        x = x1
        iterations += 1
    return x


def f(x: float, argument: str) -> float:
    """ Evaluates the function in x.

        Parameters
        ----------
        x : float
            Value of x where the function must be evaluated.

        argument : str
            Argument of the function.

        Returns
        -------
        f : float
            f(x)
    """

    f = float(eval(argument))
    return f


def obtain_argument() -> str:
    """ Obtains the argument of the function to evaluate.

        Returns
        -------
        argument : str
            Argument of the function.
    """
    argument = ""
    testNumber = randint(0, 1000)
    while True:
        str_value = input("f(x) = ")
        try:
            try:
                foo = f(testNumber, str_value)
                argument = str_value
                break
            except:
                e = exceptions.InvalidEntryError("Invalid entry: " + str_value)
                raise e
        except:
            print("Invalid entry: " + str_value)

    return argument


def obtain_start_point() -> float:
    """ Obtains the starting point for finding the root.

        Returns
        -------
        start_point : float
            Starting point for finding the root.
    """
    start_point = 0.1
    while True:
        str_value = input("Start point (default: 0.1) = ")
        if str_value == "":
            break
        else:
            try:
                try:
                    start_point = float(str_value)
                    break
                except:
                    e = exceptions.InvalidEntryError(
                        "Invalid entry: " + str_value)
                    raise e
            except:
                print("Invalid entry: " + str_value)

    return start_point


def obtain_tolerance() -> float:
    """ Obtains the required tolerance for finding the root.

    Returns
    -------
    tolerance : float
            Required tolerance for finding the root.
"""
    tolerance = 0.00001
    while True:
        str_value = input("Tolerance (default: 0.00001) = ")
        if str_value == "":
            break
        else:
            try:
                try:
                    tolerance = float(str_value)
                    break
                except:
                    e = exceptions.InvalidEntryError(
                        "Invalid entry: " + str_value)
                    raise e
            except:
                print("Invalid entry: " + str_value)
    return tolerance


def obtain_max_iterations() -> int:
    """ Obtains the number of desired iterations to run.

        Returns
        -------
        max_iterations : float
            Number of max. iterations the program has to execute.
    """
    max_iterations = 100000
    while True:
        str_value = input("Number of iterations (default: 100000) = ")
        if str_value == "":
            break
        else:
            try:
                try:
                    max_iterations = float(str_value)
                    break
                except:
                    e = exceptions.InvalidEntryError(
                        "Invalid entry: " + str_value)
                    raise e
            except:
                print("Invalid entry: " + str_value)

    return max_iterations


def main() -> None:
    """ Main method.

        Finds the roots of a certain function with Newton's, bisection or secant method.
    """
    method = "N"
    while True:
        str_value = input(
            "Method [N: Newton (default), S: Secant, B: Bisection]: ")
        if str_value == "":
            break
        if str_value != "N" and str_value != "S" and str_value != "B":
            try:
                e = exceptions.InvalidEntryError("Invalid entry: " + str_value)
                raise e
            except:
                print("Invalid entry: " + str_value)
        else:
            method = str_value
            break

    argument = obtain_argument()
    start = obtain_start_point()
    error = obtain_tolerance()
    max_iterations = obtain_max_iterations()

    print("")
    try:
        if method == "N":
            root = find_root_newton(argument, start, error, max_iterations)
        print("--> The closest root to " + str(start) + " is = " + str(root))
    except:
        print("Something went wrong.")
        print("Either the function is not continous or it doesn't have a root near the start point.")
