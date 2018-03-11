import csv

import matplotlib.pyplot as plt

#Time will do in minutes
#Currently receive food by ID number

#food does not currently match index as there are holes in the document provided

#Get contents from files. Currently just uses the index of food
#rather than name.
def getContents(filename, col):
	csvfile = open(filename, "rb")
	datareader = csv.reader(csvfile)
	contentList = []
	for row in datareader:
		if col == -1:
			newRow = []
			for elem in row:
				if elem.isdigit():
					newRow.append(int(elem))
				else:
					newRow.append(elem)
			# print newRow
			contentList.append(newRow)
		else:
			if row[col].isdigit():
				contentList.append(int(row[col]))
			else:
				contentList.append(row[col])

	return contentList

			

def bloodSugarSim(inputList):
	#sort inputList by time
	# print inputList
	exerList = getContents("Exercise.csv", 2)
	foodList = getContents("FoodDB.csv", 2)

	# print exerList

	# print len(foodList)
	# print foodList

	inputList = sorted(inputList,key=lambda x: x[2])
	# print inputList

	#Start with Blood Sugar

	timesList = {0:0}

	for elem in inputList:
		timesList[elem[2]] = 0.0
		if elem[0] == 'f': timesList[elem[2] + 120] = 0.0 #timesList.append(elem[2] + 120)
		else: end = timesList[elem[2] + 60] = 0.0

	# timesList.sort()

	for index, elem in enumerate(inputList):
		timeMod = 60
		if elem[0] == 'f': timeMod = 120

		for timeElem in timesList:
			if timeElem >= elem[2] and timeElem < elem[2] + timeMod:
				if elem[0] == 'f': 
					# print elem[1]
					timesList[timeElem] += (foodList[elem[1]] * 1.0) / 120
					if timeElem == 16:
						print (foodList[elem[1]] * 1.0) / 120
				else: 
					timesList[timeElem] -= (exerList[elem[1]] * 1.0) / 60
					if timeElem == 16:
						print elem[1]
						print exerList[elem[1]]
						print (exerList[elem[1]] * 1.0) / 60

		# end = 0
	# print timesList
		# if elem[0] == 'f': end = elem[2] + 120
		# else: end = elem[2] + 60

	pointList = []

	sortedKeys = sorted(timesList.keys())#.sort() #List of all the times
	# print sortedKeys
	# sortedKeys = sorted(sortedKeys)
	# print sortedKeys

	# print timesList

	bloodSugar = 80.0
	glycation = False
	glyCount = 0

	#Always trying to calculate where the point is in curTime
	for index, curTime in enumerate(sortedKeys):
		normalizationTime = -1

		if index != 0 and timesList[sortedKeys[index - 1]] != 0:
			bloodSugar += (curTime - sortedKeys[index - 1]) * timesList[sortedKeys[index - 1]]
		elif timesList[sortedKeys[index - 1]] == 0:
			if bloodSugar > 80:
				if bloodSugar - 80 < curTime - sortedKeys[index - 1]:
					normalizationTime = sortedKeys[index - 1] + bloodSugar - 80
					pointList.append((normalizationTime, 80))
					

				bloodSugar += (curTime - sortedKeys[index - 1]) * -1
				if bloodSugar < 80:
					bloodSugar = 80



		if not glycation and bloodSugar >= 150:
			glycation = True
			b = bloodSugar - curTime * timesList[sortedKeys[index - 1]]
			glyStart = (150.0 - b) / timesList[sortedKeys[index - 1]]

			glyCount += curTime - glyStart

			# print "start time = ", sortedKeys[index - 1]
			# print "glystrt = ", glyStart
			# print "Cur glycount", glyCount
		elif glycation and bloodSugar < 150:
			glycation = False

			b = 0
			glyEnd = 0

			# b = bloodSugar - curTime * timesList[sortedKeys[index - 1]]
			if timesList[sortedKeys[index - 1]] == 0:
				if normalizationTime != -1:
					b = bloodSugar - normalizationTime * -1
					glyEnd = (150.0 - b) / -1
				else:
					b = bloodSugar - curTime * -1
					glyEnd = (150.0 - b) / -1
			else:
				b = bloodSugar - curTime * timesList[sortedKeys[index - 1]]
				glyEnd = (150.0 - b) / timesList[sortedKeys[index - 1]]

			# print "cur blood", bloodSugar
			# print "time", curTime
			# print "last time = ", sortedKeys[index - 1]
			# print "glyend = ", glyEnd 
			

			glyCount += glyEnd - sortedKeys[index - 1]
			# print "Cur glycount", glyCount
		elif glycation == True and bloodSugar > 150:
			glyCount += curTime - sortedKeys[index - 1]
			# print "Cur glycount", glyCount


		pointList.append((curTime, bloodSugar))

		# print curTime, timesList[index]
	# print pointList
	print "Glycation is", glyCount

	xAxis = []
	yAxis = []
	for elem in pointList:
		xAxis.append(elem[0])
		yAxis.append(elem[1])

	# print xAxis
	# print yAxis

	plt.plot(xAxis, yAxis)
	plt.xlabel('Time (Minutes)')
	plt.ylabel('Blood Sugar Level')
	plt.title("Change in Blood Sugar over Time")
	plt.show()

testSet = getContents("test4.csv", -1)

bloodSugarSim(testSet)



# print exerList
# print foodList
