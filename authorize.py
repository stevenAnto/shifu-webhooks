import os.path
import pickle
from datetime import datetime
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_734676694624-7q680lm0d9mhivgoohr4ebo5873undgl.apps.googleusercontent.com.json',
                SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'  # Tiempo actual UTC
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    print("✅ Autenticación exitosa. Próximos eventos:")
    if not events:
        print("No hay eventos próximos.")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"  - {event.get('summary', '(Sin título)')} (Inicio: {start})")

if __name__ == '__main__':
    main()

