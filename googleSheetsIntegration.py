import gspread
from oauth2client.service_account import ServiceAccountCredentials
import extraFunctions
#import generateNewAttendanceSheet

def signIn(idList,ID,MemberList,Attendance):
	idList = MemberList.col_values(2)[1:]
	memberRow = extraFunctions.findLastRow(idList,ID)+1
	targetInfo = MemberList.row_values(memberRow)#find row
	targetName = targetInfo[2]
	attendenceIDList = Attendance.col_values(1)#Column of ID Numbers
	lastrow = extraFunctions.findLastRow(attendenceIDList,ID)
	lastEntry = Attendance.row_values(lastrow)
	if len(lastEntry) == 4:
		lastEntry.append("")
	if lastEntry[4] == "Time-Out" or lastEntry[4] != "":#If there is no entry or the last entry has signed out,
		#print("signing in...")
		date_time = extraFunctions.fetchCurrentDateTime()
		date = date_time[0]
		time = date_time[1]
		entryCount = Attendance.cell(1,10).value
		targetRow = int(entryCount)+2 #skip header and final entry
		Attendance.update_cell(targetRow,1,ID)
		Attendance.update_cell(targetRow,2,targetName)#TODO find name
		Attendance.update_cell(targetRow,3,date)
		Attendance.update_cell(targetRow,4,time)
		print("Signed in "+targetName+" at " +time+"\n")
	else:
		date_time = extraFunctions.fetchCurrentDateTime()
		time = date_time[1]
		#print("Signing out...")
		Attendance.update_cell(lastrow,5,time)
		print("Signed out "+targetName+" at " +time+"\n")





def enterSwipe(ID):
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('my-secret.json', scope)
	authorization = gspread.authorize(creds)

	# Find a workbook by name and open the sheets
	# Make sure you use the right name here.
	#fileName = generateNewAttendanceSheet.findSemester()
	fileName = "Fall 2018 Attendance"
	#fileName = "Copy of Fall 2018 Attendance"
	client = None
	client = authorization.open(fileName)
	MemberListClient = authorization.open("Full MemberList")

	#Open individual Sheets
	MemberList = client.worksheet("MemberList")
	Attendance = client.worksheet("Attendance")
	MasterMemberList = MemberListClient.worksheet("MasterMemberList")
	#Step 1: count members
	memberCount = MemberList.cell(1, 12).value #Checks value of L2, which is pre-calculated
	idList = MemberList.col_values(2)[1:]

	if ID not in idList:#Not found locally in idList
		fullIDList = MasterMemberList.col_values(2)
		#print(fullIDList)
		if ID not in fullIDList:#not found globally in fullIDList
			print("Your information was not found...")
			print("ID is "+ID)
			targetName = input("Please enter your name: ")
			targetUCID = input("Please enter your UCID (it's in your email): ")
			newRow = len(idList)+1
			print(MemberList.row_values(newRow))
			#Update Local memberlist
			MemberList.update_cell(newRow,2,ID)
			MemberList.update_cell(newRow,3,targetName)
			MemberList.update_cell(newRow,4,"Member")
			MemberList.update_cell(newRow,5,targetUCID)
			print("Local entry created for "+targetName)

			#update Global Memberlist
			newMasterRow = len(fullIDList)+1
			MasterMemberList.update_cell(newMasterRow,2,ID)
			MasterMemberList.update_cell(newMasterRow,3,targetName)
			MasterMemberList.update_cell(newMasterRow,4,"Member")
			MasterMemberList.update_cell(newMasterRow,5,targetUCID)
			print("Global entry created.")
			signIn(idList,ID,MemberList,Attendance)

		else:#found globally
			#Get info from MasterList
			masterMemberRow = extraFunctions.findLastRow(fullIDList,ID)#
			#print("Moving Entry..."+str(masterMemberRow))
			memberInfo = MasterMemberList.row_values(masterMemberRow)
			print(memberInfo)
			#print(memberInfo)
			targetName = memberInfo[2]
			print("Name:"+targetName)
			targetUCID = memberInfo[4]
			targetPosition = memberInfo[3]

			#Now place in local memberlist
			newRow = len(idList)+2
			MemberList.update_cell(newRow,2,ID)
			MemberList.update_cell(newRow,3,targetName)
			MemberList.update_cell(newRow,4,targetPosition)
			MemberList.update_cell(newRow,5,targetUCID)
			print("Local entry created for "+targetName)
			signIn(idList,ID,MemberList,Attendance)# idList is wrong

	else:#found locally
		signIn(idList,ID,MemberList,Attendance)

def whosHere(): #Needs to be finished
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('my-secret.json', scope)
	authorization = gspread.authorize(creds)

	# Find a workbook by name and open the sheets
	# Make sure you use the right name here.
	#fileName = generateNewAttendanceSheet.findSemester()
	fileName = "Fall 2018 Attendance"
	#fileName = "Copy of Fall 2018 Attendance"
	client = None
	client = authorization.open(fileName)
	
	#Open individual Sheet
	Attendance = client.worksheet("Attendance")
	
