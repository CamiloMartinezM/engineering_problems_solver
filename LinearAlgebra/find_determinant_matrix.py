# -*- coding: utf-8 -*-
"""
Created on December 14, 2019.

@author: Camilo Martínez
"""
from LinearAlgebra import obtain_square_matrix


def det(matrix: list, mul: float) -> float:
    """ Recursive function to find the determinant of the given matrix.

        Parameters
        ----------
        matrix : list
            The matrix in the form of a list of lists.

        mul : float
            Cofactor value.

        Returns
        -------
            total : float
                Determinant of matrix.
        """
    width = len(matrix)
    if width == 1:
        return mul * matrix[0][0]
    else:
        sign = -1
        total = 0
        for i in range(width):
            m = []
            for j in range(1, width):
                buff = []
                for k in range(width):
                    if k != i:
                        buff.append(matrix[j][k])
                m.append(buff)
            sign *= -1
            total += mul * det(m, sign * matrix[0][i])
        return total


def main():
    """ Main method. """
    matrix = obtain_square_matrix.main()
    print("")

    # In case an error occured obtaining the matrix.
    if matrix is not None:
        print("The determinant is = " + str(det(matrix, 1)))
