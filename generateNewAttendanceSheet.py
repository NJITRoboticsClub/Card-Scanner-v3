from apiclient import errors
import extraFunctions
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pprint import pprint
from googleapiclient import discovery
# ...

def copy_file(service, origin_file_id, copy_title):
  """Copy an existing file.

  Args:
    service: Drive API service instance.
    origin_file_id: ID of the origin file to copy.
    copy_title: Title of the copy.

  Returns:
    The copied file if successful, None otherwise.
  """
  copied_file = {'title': copy_title}
  try:
    return service.files().copy(
        fileId=origin_file_id, body=copied_file).execute()
  except (errors.HttpError, error):
    print('An error occurred: %s' % error)
  return None

def findSemester():
  dateTime = extraFunctions.fetchCurrentDateTime()
  month = int(dateTime[0][:2])
  year = dateTime[0][-4:]
  JUNE = 5
  season = ""
  if month < JUNE:
    season = "Spring"
  else:
    season = "Fall"
  return season+" "+year+" Attendance Sheet"


def createNewAttendanceSheet(title):
  #Security
  scope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name('my-secret.json', scope)
  gc = gspread.authorize(credentials)
  service = discovery.build('sheets', 'v4', credentials=credentials)
  #Create A New File
  spreadsheet_body = {
    "properties": {
      "title": title
    }
  }
  request = service.spreadsheets().create(body=spreadsheet_body)
  response = request.execute()

  #Changing permissions for the user (from the credentials.json) and then the real user (me)
  gc.insert_permission(response['spreadsheetId'], 'project@plated-mantra-216318.iam.gserviceaccount.com', perm_type='user', role='owner')
  gc.insert_permission(response['spreadsheetId'], 'robotato106@gmail.com', perm_type='user', role='owner')
  # ID of template
  template_id = '1coZ2b6VwWxbXrg0XHzpcHuVVH0ximyQUs_Si9EE8vcE'  
  #sheet = gc.open_by_key(response['spreadsheet_id']).Sheet1
  # The ID of the sheet to copy. Everybody has access!!!
  sheet_id = 0  
  #Copy Sheet
  copy_sheet_to_another_spreadsheet_request_body = {"destinationSpreadsheetId": ""}
  request = service.spreadsheets().sheets().copyTo(spreadsheetId=template_id, sheetId=sheet_id, body=copy_sheet_to_another_spreadsheet_request_body)
  response = request.execute()
  gspread.Client(authorization).create(title)

createNewAttendanceSheet("Fall 2018 Attendance Sheet")
