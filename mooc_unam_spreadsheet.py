from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SECRET_FILE = "E:/Proyectos/MOOC_UNAM/data_learning_analytics/credenciales/credentials.json"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def validador(id_hdc, rango_hdc):
    credenciales = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credenciales = pickle.load(token)
    if not credenciales or not credenciales.valid:
        if credenciales and credenciales.expired and credenciales.refresh_token:
            credenciales.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SECRET_FILE, SCOPES
            )
            credenciales = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credenciales, token)

    service = build('sheets', 'v4', credentials=credenciales)

    hojadecalculo = service.spreadsheets()
    resultado = hojadecalculo.values().get(
        spreadsheetId=id_hdc, range=rango_hdc).execute()
    return resultado.get('values', [])
