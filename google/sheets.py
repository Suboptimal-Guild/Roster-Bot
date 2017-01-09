from __future__ import print_function
import httplib2
import os
import json
from texttable import Texttable

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

# Spreadsheet IDs
ROSTER_SHEET = '1j5kBuTppGMIp17NBvLPmHV7b2_GSuc2JRT9JhKxLDas'
HARAMBOT_TEST_SHEET = '1K0V19lxMsIC7TzLTJ8AY8s7vjlIljpmK_5MuO2LopSI'

# Spreadsheet shit
DISCOVERY_URL = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_roster():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=DISCOVERY_URL)

    rangeName = 'Roster!G3:K'
    result = service.spreadsheets().values().get(
    spreadsheetId=ROSTER_SHEET, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found in sheet.')
    else:
        a = []
        for row in values:
            a.append((row[0], row[1], row[2], row[3], row[4]))
        return a
