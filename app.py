from flask import Flask, request
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build

app = Flask(__name__)

def get_service():
    with open('token.pickle', 'rb') as f:
        creds = pickle.load(f)
    return build('calendar', 'v3', credentials=creds)

last_check = datetime.utcnow()

@app.route('/webhook-calendar', methods=['POST'])
def webhook_calendar():
    global last_check
    now = datetime.utcnow()
    service = get_service()

    events_result = service.events().list(
        calendarId='primary',
        updatedMin=last_check.isoformat() + 'Z',
        singleEvents=True,
        orderBy='updated'
    ).execute()

    events = events_result.get('items', [])
    print(f"\nNotificación recibida: {len(events)} evento(s) actualizado(s) desde {last_check}")
    for event in events:
        print(f"  - {event.get('summary')} (ID: {event.get('id')})")

    last_check = now
    return '', 200

@app.route('/webhook-dropbox', methods=['GET', 'POST'])
def dropbox_webhook():
    if request.method == 'GET':
        # Verificación del webhook (challenge)
        challenge = request.args.get('challenge')
        return challenge, 200
    elif request.method == 'POST':
        # Notificación de cambios
        data = request.get_json()
        print(" Cambio recibido en Dropbox")
        print("Usuarios afectados:", data.get('list_folder', {}).get('accounts'))
        return '', 200


if __name__ == '__main__':
    app.run(port=5000)