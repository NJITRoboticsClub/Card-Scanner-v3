import serial
import io
import extraFunctions
import googleSheetsIntegration
import GUI_testing
import time

global ser
try:
	ser = serial.Serial('COM1') #Opens Serial Port "COM1"
	print("Robotics Sign-in System:")
	print("Simply close the terminal window to close.")
	print("Swipe card to sign-in or out" + "\n")
	while(True):
		print("Please swipe:")
		cardID = extraFunctions.stripCard(ser.readline())
		googleSheetsIntegration.enterSwipe(cardID)
except serial.serialutil.SerialException:
	print("Scanner is currently being used by another program...")
	print("Only start by running newScannerApp.py, don't use a compiler.")
	time.sleep(5)#5 Seconds
