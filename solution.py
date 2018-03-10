import csv

#Time will do in minutes
#Currently receive food by ID number

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
			print newRow
			contentList.append(newRow)
		else:
			if row[col].isdigit():
				contentList.append(int(row[col]))
			else:
				contentList.append(row[col])

	return contentList

			

def bloodSugarSim(inputList):
	#sort inputList by time
	print inputList
	print sorted(inputList,key=lambda x: x[2])

	#Start with Blood Sugar

	for elem in inputList:
		if elem[0] == 'f':
			print "test"





exerList = getContents("Exercise.csv", 2)
foodList = getContents("FoodDB.csv", 2)
testSet = getContents("test.csv", -1)

bloodSugarSim(testSet)



# print exerList
# print foodList
