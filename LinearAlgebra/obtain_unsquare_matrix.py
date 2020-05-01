#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
	Obtains a not-square matrix given by the user and stores it in a list of lists.
'''

def obtainDimension():
	""" Obtains the dimension of the matrix """
	try:
		str_dimension = raw_input("Dimension (example: 3x4): ")
		dimension = [int(x) for x in str_dimension.split("x")]
		print ("")
	except:
		print ("Invalid entry!")

	return dimension

def main():
	""" Main method """
	rows, columns = obtainDimension()

	print ("Matrix " + str(rows) + "x" + str(columns) + ":")

	i = 0
	matrix = []
	# Loop that iterates the matrix by rows.
	while i < rows:
		str_Fila = raw_input("-> Row #" + str(i + 1) + ": ")

		# In case the dimension is not being respected.
		if columns != len(str_Fila.split(" ")):
			print ("The number of given values is not equal to the number of columns!")
		else:
			fila = [float(x) for x in str_Fila.split(" ")]
			matrix.append(fila)
			i += 1

	return matrix
