# -*- coding: utf-8 -*-
"""
Created on December 13, 2019.

@author: Camilo Martínez
"""
from ExceptionHandling import ParentException

class OptionNotFoundError(ParentException.ParentException):
    """ Raised when the user inputs an inexistent/unavailable option.

        When the exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None) -> None:
        super().__init__(message, filename, 0)


class FunctionNotFoundError(ParentException.ParentException):
    """ Raised when the program has a problem finding the function.

        When the exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None) -> None:
        super().__init__(message, filename, 1)

class InvalidEntryError(ParentException.ParentException):
    """ Raised when the program has a problem with an entry, i.e,
        expected: float, but was str.

        When the exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None) -> None:
        super().__init__(message, filename, 2)

class InvalidFileExtensionError(ParentException.ParentException):
    """ Raised when an unexpected error occurrs, associated with
        calls to python functions.

        When the exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None) -> None:
        super().__init__(message, filename, 3)

class InvalidFileFormatError(ParentException.ParentException):
    """ Raised when an unexpected error occurrs, associated with
        calls to python functions.

        When the exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None) -> None:
        super().__init__(message, filename, 4)

class Bug(ParentException.ParentException):
    """ Raised when an unexpected error occurrs, associated with
        calls to python functions.

        When the exception is raised, the error message gets
        stored inside a log file, which contains all errors.
    """

    def __init__(self, message: str, filename: str = None) -> None:
        super().__init__(message, filename, 000)
