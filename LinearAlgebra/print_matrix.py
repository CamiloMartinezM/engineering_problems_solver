#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
	Prints a matrix in a friendly manner.
'''
def main(matrix):
	maxNumberDigits = 0
	i = 0

	# Obtains the max number of digits inside the matrix.
	for row in matrix:
		while i < len(row):
			negativeCorrection = 0

			# Negative correction in case the iterated number is negative.
			if row[i] < 0:
				correccionNgativa = 1

			# Número de digits del valor iterado.
			digits = len(str(abs(row[i] + negativeCorrection)))

			# Assigns the maximum number of digits.
			if digits > maxNumberDigits:
				maxNumberDigits = digits

			i += 1

			print ("")

	# Prints the matrix.
	for row in matrix:
		print ('%s' % (' '.join('%0*s' % (maxNumberDigits, i) for i in row)))
