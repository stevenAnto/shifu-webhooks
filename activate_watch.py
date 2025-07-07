# activate_watch.py
import pickle
from googleapiclient.discovery import build

def main():
    with open('token.pickle', 'rb') as token_file:
        creds = pickle.load(token_file)

    service = build('calendar', 'v3', credentials=creds)

    body = {
        'id': 'cal-watch-002',  # puedes usar uuid4 si quieres algo único
        'type': 'web_hook',
        'address': 'https://4079-2001-1388-4a01-1db9-bc1e-8928-f072-ae21.ngrok-free.app/webhook-calendar',
        'params': {
            'ttl': '86400'  # 1 día
        }
    }

    response = service.events().watch(calendarId='primary', body=body).execute()
    print("✅ Webhook activado:")
    print(response)
    calendar_list = service.calendarList().list().execute()
    for cal in calendar_list['items']:
        print(f"Calendario: {cal['summary']}, ID: {cal['id']}, Primary: {cal.get('primary', False)}")


if __name__ == '__main__':
    main()
