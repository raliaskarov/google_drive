from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle


# ID for google sheets to access
workbook_id = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
path_to_secrets = "path/to/yourcredentials.json"
sheet_name = 'name_of_your_sheet'

def read_google_sheets(workbook_id, sheet_name, path_to_secrets):
    # If modifying these SCOPES, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_secrets, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    # Replace 'SPREADSHEET_ID' with your specific Spreadsheet ID
    result = sheet.values().get(spreadsheetId = workbook_id,
                                range=sheet_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        df = pd.DataFrame(values[1:], columns=values[0])
    
    return df

read_google_sheets(workbook_id, sheet_name, path_to_secrets)
