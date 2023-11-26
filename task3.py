class Task3:
    def __init__(self):
        print("Init task 3")
        return

    def Task3_Run(self):
        print("Task 3 is activated!!!!")
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
from task2 import max_index
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1SOAXdeqHgPm929PPHKhlMgmvCxwz0j5S2JD4jH68oqY"
RANGE_NAME = "Sheet 1 Data!A1:E"
def get_status(student_name, student_id):
    # Your logic to determine the status based on student name and ID
    # For demonstration purposes, let's randomly assign "Yes" or "No" for each student name
    global studentstatus
    studentstatus = None
    if max_index == 0:
        studentstatus = 'YES'
    elif max_index == 1:
        studentstatus = 'NO'
    return studentstatus

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        for row in range(2, 7):  # Assuming you have data in rows B2 to B6
            range_name_student_name = f"Sheet 1!B{row}"
            range_name_student_id = f"Sheet 1!A{row}"
            print(f"Fetching data from range: {range_name_student_name}")
            student_name_values = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name_student_name).execute().get("values")
            student_id_values = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name_student_id).execute().get("values")

            if student_name_values and student_name_values[0] and student_id_values and student_id_values[0]:
                student_name = student_name_values[0][0]
                student_id = student_id_values[0][0]

                # Your logic to determine the status based on student name and ID
                status = get_status(student_name, student_id)

                print(f"Student Name: {student_name}, Student ID: {student_id}, Status: {status}")

                # Update the status in column D
                sheets.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"Sheet 1!D{row}",
                    valueInputOption="USER_ENTERED",
                    body={"values": [[status]]}
                ).execute()

            else:
                print(f"No data found for Student in row {row}")

    except HttpError as error:
        print(error)
if __name__ == "__main__":
    main()
