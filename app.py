import base64
import os
from urllib.parse import parse_qs, urlparse
from flask import Flask, Request, json, jsonify, request
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import requests

app = Flask(__name__)

##google Calendar

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

##Gmail
# Cargar el token para acceder a Gmail API
def get_gmail_service():
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)

@app.route("/gmail-webhook", methods=["POST"])
def gmail_webhook():
    data = request.get_json()
    print("📦 Payload recibido:")
    print(json.dumps(data, indent=2))

    pubsub_msg = data.get("message", {})
    
    # Decodificar el campo 'data' que viene en base64
    encoded_data = pubsub_msg.get("data", "")
    decoded_bytes = base64.b64decode(encoded_data)
    decoded_data = json.loads(decoded_bytes)

    email = decoded_data.get("emailAddress")
    history_id = str(decoded_data.get("historyId"))  # importante convertir a str

    print(f"\n📨 Notificación de Gmail para: {email}")
    print(f"🔁 History ID recibido: {history_id}")

    service = get_gmail_service()

    try:
        response = service.users().history().list(
            userId='me',
            startHistoryId=history_id,
            historyTypes=['messageAdded']
        ).execute()

        print("🧾 Respuesta de history.list:")
        print(json.dumps(response, indent=2))


        history = response.get("history", [])
        for record in history:
            for msg in record.get("messagesAdded", []):
                msg_id = msg["message"]["id"]
                full_msg = service.users().messages().get(userId='me', id=msg_id).execute()

                headers = full_msg.get("payload", {}).get("headers", [])
                subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(Sin asunto)")
                sender = next((h["value"] for h in headers if h["name"] == "From"), "(Sin remitente)")

                print(f"📧 Nuevo mensaje:")
                print(f"    ➤ De: {sender}")
                print(f"    ➤ Asunto: {subject}")

    except Exception as e:
        print(f"❌ Error al consultar Gmail API: {e}")

    return "OK", 200


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

@app.route('/webhook-drive', methods=['POST'])
def webhook():
    print(" ¡Cambio detectado en Google Drive!")
    print("Encabezados:", dict(request.headers))
    print("***********************\n")
    
    resource_uri = request.headers.get('X-Goog-Resource-Uri')
    page_token = None
    token_path= 'last_token.txt'
    if resource_uri:
        print("There is resouci+iru")
        query = urlparse(resource_uri).query
        params = parse_qs(query)
        page_token = params.get('pageToken', [None])[0]
    

    if os.path.exists(token_path):
        print("encontramos el nuevo token para el cambio")
        with open(token_path, 'r') as f:
            page_token = f.read().strip()
        print("page_token",page_token)
    
    if not page_token:
        print(" No se encontró pageToken en la notificación.")
        return '', 200
    
    try:
        creds = load_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        response = service.changes().list(pageToken=page_token, spaces='drive').execute()
        
        for change in response.get('changes', []):
            file = change.get('file')
            removed = change.get('removed', False)
            change_type = change.get('changeType', 'unknown')
            file_id = None
            file_name = None

            if removed:
                # Archivo eliminado
                file_id = change.get('fileId', 'Desconocido')
                print(f" Archivo eliminado: ID={file_id}")
            elif file:
                # Archivo creado o modificado
                file_id = file.get('id')
                file_name = file.get('name')
                print(f" Archivo cambiado: {file_name} (ID: {file_id})")
                
                # Ahora podemos obtener detalles adicionales del archivo
                try:
                   file_detail = service.files().get(fileId=file_id, fields="id, name, mimeType, modifiedTime, owners, trashed").execute()
                   print(" Detalles del archivo:")
                   print(f"  Tipo MIME: {file_detail.get('mimeType')}")
                   print(f"  Modificado: {file_detail.get('modifiedTime')}")
                   print(f"  Propietarios: {[owner.get('emailAddress') for owner in file_detail.get('owners', [])]}")
                   print(f"  Papelera: {file_detail.get('trashed')}")
                except Exception as e:
                   print(f"  No se pudo obtener detalles: {e}")
            else:
                print(" Cambio sin archivo asociado:", change)
            print("------------\n")
        
        if 'newStartPageToken' in response:
            new_token = response['newStartPageToken']
            with open(token_path, 'w') as f:
                f.write(new_token)
            print(" Nuevo startPageToken:", response['newStartPageToken'])
        
    except Exception as e:
        print(" Error al consultar cambios:", e)
    
    return '', 200

##DropBox

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

#Slack with Bot
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


#webhook ClickUp 
@app.route('/webhook-clickup', methods=['POST'])
def clickup_webhook():
    data = request.json
    print("Webhook recibido:")
    print(data)
    return jsonify({'status': 'received'}), 200

#webhook asana
@app.route('/webhook-asana', methods=['POST'])
def asana_webhook():
    # Verificación inicial del webhook
    if 'X-Hook-Secret' in request.headers:
        secret = request.headers['X-Hook-Secret']
        print("Verificación recibida, respondiendo con X-Hook-Secret")
        return '', 200, {'X-Hook-Secret': secret}

    # Manejo de eventos reales
    payload = request.get_json()
    print("Evento recibido:")
    print(payload)

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)