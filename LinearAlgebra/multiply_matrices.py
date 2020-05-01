#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
	Multiplies 2 matrices given by the user.
'''
import obtainUnsquareMatrix
import printMatrix
import writeVariable
from variableClass import Variable

def multiply(X, Y):
	""" Multiplies the given two matrices """
	result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
	return result

def main():
	""" Main method """
	print ("First matrix:")
	print ("")
	matrixA = obtainUnsquareMatrix.main()

	print ("")
	print ("Second matrix:")
	print ("")
	matrixB = obtainUnsquareMatrix.main()

	print ("")
	# Condition for matrix multiplication.
	if len( matrixA[0] ) == len( matrixB ):
		print ("The result is: ")
		result = multiply(matrixA, matrixB)
		printMatrix.main(result)
		print ("")

		# Algorithm that stores the result to a variable.
		answer = raw_input("Save to a variable? [y/n] ")
		if answer == "y":
			# Loop that ensures the entries are correct.
			while True:
				name = raw_input("Name of the variable (do not include whitespaces!): ")
				if " " not in name:
					break
				else:
					print("Do not include whitespaces!")

			newVariable = Variable( result, str(name), "matrix" )
			writeVariable.main( newVariable )
	else:
		print("Remember that the number of columns of the first matrix must be equal to the number of rows of the second one")
