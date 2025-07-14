import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def load_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No se encontraron credenciales válidas. Ejecuta authorize.py primero.")
    return creds

creds = load_credentials()
service = build('drive', 'v3', credentials=creds)

start_page_token = service.changes().getStartPageToken().execute()['startPageToken']
print("🔖 Usando startPageToken:", start_page_token)

channel = {
    "id": "mi-unico-id-canal-6234569",
    "type": "web_hook",
    "address": "https://3d52-2001-1388-4a01-972a-dd29-1613-9604-b301.ngrok-free.app/webhook"
}
response = service.changes().watch(body=channel, pageToken=start_page_token).execute()

with open('last_token.txt', 'w') as f:
    f.write(start_page_token)
print("Suscripción activa.")
print(response)