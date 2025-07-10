from flask import Flask, jsonify, request
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import requests

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
#endpoint para slack 
# Pon aquí tu Bot User OAuth Token (xoxb-...)
SLACK_BOT_TOKEN = "poner aqui tu token"

SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"

@app.route('/slack-webhook', methods=['POST'])
def slack_webhook():
    data = request.get_json()

    # Slack verifica la URL con un challenge
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data['challenge']})

    # Evento recibido
    if data.get('type') == 'event_callback':
        event = data['event']
        print("Nuevo evento de Slack:", event)

        # Solo responder si es mensaje y NO es mensaje de bot (para evitar loops)
        if event.get('type') == 'message' and not event.get('bot_id'):
            user = event.get('user')
            text = event.get('text')
            channel = event.get('channel')

            # Mensaje para responder
            reply_text = f"Hola <@{user}>! Recibí tu mensaje: {text}"

            # Enviar mensaje a Slack usando chat.postMessage
            headers = {
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "channel": channel,
                "text": reply_text
            }

            response = requests.post(SLACK_POST_MESSAGE_URL, headers=headers, json=payload)
            print("Respuesta de Slack API:", response.json())

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)