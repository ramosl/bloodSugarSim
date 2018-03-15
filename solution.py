import csv

import matplotlib.pyplot as plt

#Time will do in minutes
#Currently receive food by ID number


"""
Questions to ask:
Am i allowed to fix input the way I did, or how much flexitiblity am i allowed
- Currently do buy index and by exact name of food

# GRAPH FOR GLYCATION

"""

# Starting constants based on the specification
STARTING_BLOOD_SUGAR = 80
GLYCATION_LEVEL = 150

#Method to extract food/exercise info from csv files
def getContents(filename):
	csvfile = open(filename, "rb")
	datareader = csv.reader(csvfile)

	contentList = {}
	for row in datareader:
		for col in range(0, 2):
			if row[col].isdigit():
				contentList[int(row[col])] = int(row[2])
			else:
				contentList[row[col]] = int(row[2])
	return contentList

#Method to extract test set info from csv files
def getTestSet(filename):
	csvfile = open(filename, "rb")
	datareader = csv.reader(csvfile)
	contentList = []
	for row in datareader:
		newRow = []
		for elem in row:
			if elem.isdigit():
				newRow.append(int(elem))
			else:
				newRow.append(elem)
		contentList.append(newRow)

	return contentList

			
"""
Method to run the simulation. Accepts a list of properly formatted inputs,
including the item's index/name and whether it is a food or exercise, and
figures out how to plot the points in a blood sugar simulation graph and
plots it. Also prints out the final value of glycation.
"""
def bloodSugarSim(inputList):
	exerList = getContents("Exercise.csv")
	foodList = getContents("FoodDB.csv")

	#Sort the input list based on the time inputted.
	inputList = sorted(inputList,key=lambda x: x[2])
	print inputList

	#Dictionary of times in the graph
	timesList = {0:0}

	"""
	First created a dictionary of all the times that would create kink points, 
	when the slope would change in the graph. Contains when eating/exercising
	would start changing a person's blood sugar and when it would stop.
	"""
	for elem in inputList:
		timesList[elem[2]] = 0.0
		if elem[0] == 'f': timesList[elem[2] + 120] = 0.0
		else: end = timesList[elem[2] + 60] = 0.0

	# timesList.sort()

	"""
	Using the dictionary of times that was created previously, now calculate the
	corresponding slope in each of those sections.
	"""
	for index, elem in enumerate(inputList):
		timeMod = 60
		if elem[0] == 'f': timeMod = 120

		for timeElem in timesList:
			if timeElem >= elem[2] and timeElem < elem[2] + timeMod:
				if elem[0] == 'f': 
					timesList[timeElem] += (foodList[elem[1]] * 1.0) / 120
				else: 
					timesList[timeElem] -= (exerList[elem[1]] * 1.0) / 60

	#Create a list that has all keys sorted to traverse the timesList in chronological order.
	sortedKeys = sorted(timesList.keys())

	#Final set of points to output to graph
	pointList = []
	glyPointList = [(0,0)]

	bloodSugar = STARTING_BLOOD_SUGAR
	glycation = False
	glyCount = 0

	#Loop through all elements in the list of times.
	for index, curTime in enumerate(sortedKeys):
		normalizationTime = -1

		if index != 0 and timesList[sortedKeys[index - 1]] != 0:
			bloodSugar += (curTime - sortedKeys[index - 1]) * timesList[sortedKeys[index - 1]]
		elif timesList[sortedKeys[index - 1]] == 0:
			if bloodSugar > STARTING_BLOOD_SUGAR:
				"""
				If nothing is happening, then the person begins normalizing back to starting blood
				sugar. Thus, this would be done by creating another point in the output later on.
				"""
				if bloodSugar - STARTING_BLOOD_SUGAR < curTime - sortedKeys[index - 1]:
					normalizationTime = sortedKeys[index - 1] + bloodSugar - STARTING_BLOOD_SUGAR
					pointList.append((normalizationTime, STARTING_BLOOD_SUGAR))
					
				bloodSugar += (curTime - sortedKeys[index - 1]) * -1
				if bloodSugar < STARTING_BLOOD_SUGAR:
					bloodSugar = STARTING_BLOOD_SUGAR

		"""
		To track glycation, whenever the blood sugar level would go above 150, the program would
		then find the intersect of that line with the current segment. It would then add that amount
		to the total glycation count.
		"""
		if not glycation and bloodSugar >= GLYCATION_LEVEL:
			

			glycation = True
			yInt = bloodSugar - curTime * timesList[sortedKeys[index - 1]]
			glyStart = ((GLYCATION_LEVEL - yInt) * 1.0) / timesList[sortedKeys[index - 1]]
			
			glyPointList.append((glyStart, glyCount))
			glyCount += curTime - glyStart
			glyPointList.append((curTime, glyCount))

		elif glycation and bloodSugar < GLYCATION_LEVEL:
			glycation = False
			yInt, glyEnd = 0, 0

			if timesList[sortedKeys[index - 1]] == 0:
				if normalizationTime != -1:
					yInt = bloodSugar - normalizationTime * -1
					glyEnd = ((GLYCATION_LEVEL - yInt) * 1.0) / -1
				else:
					yInt = bloodSugar - curTime * -1
					glyEnd = ((GLYCATION_LEVEL - yInt) * 1.0) / -1
			else:
				yInt = bloodSugar - curTime * timesList[sortedKeys[index - 1]]
				glyEnd = ((GLYCATION_LEVEL - yInt) * 1.0) / timesList[sortedKeys[index - 1]]

			

			# glyPointList.append((glyEnd, glyCount))

			glyPointList.append((sortedKeys[index - 1], glyCount))
			glyCount += glyEnd - sortedKeys[index - 1]
			glyPointList.append((glyEnd, glyCount))

		elif glycation == True and bloodSugar > GLYCATION_LEVEL:
			# glyCount += curTime - sortedKeys[index - 1]
			# glyPointList.append((curTime, glyCount))

			glyPointList.append((sortedKeys[index - 1], glyCount))
			glyCount += curTime - sortedKeys[index - 1]
			glyPointList.append((curTime, glyCount))

		#Add the point to the list of points for the graph
		pointList.append((curTime, bloodSugar))

	#Add one final point so that a person's blood level normalizes to the starting level
	# print glycation
	# print bloodSugar
	normalizationTime = sortedKeys[len(sortedKeys) - 1] + bloodSugar - STARTING_BLOOD_SUGAR
	if bloodSugar > STARTING_BLOOD_SUGAR:
		pointList.append((normalizationTime, STARTING_BLOOD_SUGAR))
		bloodSugar = STARTING_BLOOD_SUGAR
	if glycation and bloodSugar < GLYCATION_LEVEL:
		yInt, glyEnd = 0, 0

		curTime = sortedKeys[len(sortedKeys) - 1]

		yInt = bloodSugar - normalizationTime * -1
		glyEnd = ((GLYCATION_LEVEL - yInt) * 1.0) / -1

		glyPointList.append((curTime, glyCount))
		glyCount += glyEnd - curTime
		glyPointList.append((glyEnd, glyCount))
	glyPointList.append((normalizationTime, glyCount))



	print "Glycation level is", glyCount


	#Plotting the graph using pyplot
	xAxis = []
	yAxis = []
	for elem in pointList:
		xAxis.append(elem[0])
		yAxis.append(elem[1])

	plt.plot(xAxis, yAxis)
	plt.xlabel('Time (Minutes)')
	plt.ylabel('Blood Sugar Level')
	plt.title("Change in Blood Sugar over Time")
	plt.show()

	xAxis2 = []
	yAxis2 = []
	for elem in glyPointList:
		xAxis2.append(elem[0])
		yAxis2.append(elem[1])

	plt.plot(xAxis2, yAxis2)
	plt.xlabel('Time (Minutes)')
	plt.ylabel('Glycation Level')
	plt.title("Change in Glycation over Time")
	plt.show()



#Code to run the Blood Sugar Simulator
testSet = getTestSet("test2.csv")
bloodSugarSim(testSet)
