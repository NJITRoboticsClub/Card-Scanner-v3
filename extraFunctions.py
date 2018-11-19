import datetime

def stripCard(inputString):
	'''Strips excess data from byte-string'''
	ID = str(inputString)[16:-6]
	print("Processing ID: "+ID)
	return ID

def fetchCurrentDateTime():
	fullString = str(datetime.datetime.now())
	date = datetime.datetime.now().strftime('%m/%d/%Y')#Formats date
	time = datetime.datetime.now().strftime('%I:%M:%S %p')#Formats time
	return [date,time]

def register(idNum):
	print(idNum+"Not found in list, add data manually until this is automated")

def findLastRow(idNumList,targetID):
	lastIndex = 1 #default to the header, for the new entry condition
	for index in range(len(idNumList)):
		if targetID == idNumList[index]:
			lastIndex = index
	return lastIndex+1# sheet rows aren't 0-indexed
