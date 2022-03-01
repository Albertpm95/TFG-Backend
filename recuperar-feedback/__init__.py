from __future__ import print_function
from http.client import HTTPResponse

from constants import SCOPES, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME

from flask import Flask
from flask_cors import CORS, cross_origin

import azure.functions as func
import json
import os.path

import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
@app.route("/recuperar-feedback")
def main(req: func.HttpRequest) -> func.HttpResponse:

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'recuperar-feedback/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return func.HttpResponse("No hay datos recientes de feedback.")

        del values[0]
        b = []

        for row in values:
            del row[5]

            registered_date = datetime.datetime.strptime(
                row[4], '%d/%m/%Y %H:%M:%S')
            registered_date = registered_date + datetime.timedelta(hours=1)
            now = datetime.datetime.now()

            difference = now - registered_date

            if (difference.total_seconds() <= 12600):
                fila = {'ubicacion': row[0],
                        'luminico': row[1], 'termico': row[2], 'acustico': row[3]}
                b.append(fila)

        return func.HttpResponse(
            json.dumps(b)
        )

    except HttpError as err:
        return func.HttpResponse("No se han podido procesar los datos")
