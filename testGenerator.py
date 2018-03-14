"""
Code to generate random test sets for the solution to use.
"""
import random

hourLimit = 10
foodTypes = 112
exerTypes = 6

for i in range(0, 10):
	curStr = ""
	numIndex = 0

	if random.randint(0,3) < 3:
		curStr += "f,"
		numIndex = foodTypes
	else:
		curStr += "e,"
		numIndex = exerTypes

	curStr += str(random.randint(1,numIndex)) + ","
	curStr += str(random.randint(0,60 * hourLimit))
	print curStr

	