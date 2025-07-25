import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Reemplaza con el ID de tu proyecto y nombre del topic creado
PROJECT_ID = "webhookgmail-464813"
TOPIC_NAME = f"projects/{PROJECT_ID}/topics/gmail-notify"

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_734676694624-7q680lm0d9mhivgoohr4ebo5873undgl.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def activate_watch(service):
    request = {
        "labelIds": ["INBOX"],
        "topicName": TOPIC_NAME
    }
    response = service.users().watch(userId='me', body=request).execute()
    print("🔔 Gmail watch activated:")
    print(response)

if __name__ == "__main__":
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    activate_watch(service)