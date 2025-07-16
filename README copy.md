# 🔔 Webhooks con Flask: Google Calendar, Gmail, Google Drive, Dropbox, Slack, ClickUp y Asana

Este proyecto implementa **webhooks en Flask** para escuchar cambios en:

- 📅 Google Calendar  
- 📥 Gmail  
- 📂 Google Drive  
- 📁 Dropbox  
- 💬 Slack (solo para el workspace donde la app ha sido creada)  
- ✅ ClickUp (eventos en tareas)  
- 📋 **Asana** (eventos en proyectos)

Utiliza OAuth 2.0 para autenticación (para Google APIs) y tokens de acceso para Dropbox, Slack, ClickUp y Asana.  
Los cambios se notifican en tiempo real a tu servidor Flask usando la funcionalidad de webhooks de cada plataforma.

---

## 📁 Estructura del proyecto

```bash
.
├── activate_watch_drive.py
├── activate_watch_gmail.py
├── activate_watch_google_calendar.py
├── ambiente/                        # Entorno virtual
├── app.py                         # Servidor Flask: maneja todos los webhooks
├── asana/
│   └── create_webhook.py          # Script para crear webhook en Asana
├── authorize_google_calendar.py
├── authorize_google_drive.py
├── authorize_google_gmail.py
├── calculoExpiration.py
├── client_secret_*.json           # Credenciales OAuth (NO subir)
├── README.md
├── registro_webhook_clickup.py
├── requirements.txt
└── token.pickle                   # Token de acceso Google (NO subir)
```

---

## ⚙️ Configuración General

### 1. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv ambiente
source ambiente/bin/activate
pip install -r requirements.txt
```

### 2. Agregar credenciales

En todos los scripts `authorize_*.py`, asegúrate de tener el archivo de credenciales OAuth descargado desde Google Cloud Console y nombrado como `client_secret_*.json`.

Ese archivo debe ser pasado a:

```python
InstalledAppFlow.from_client_secrets_file('client_secret_*.json', SCOPES)
```

> ⚠️ **No subas este archivo a GitHub.**

### 3. Establecer URLs públicas

En los scripts `activate_watch_*.py`, asegúrate de:

- Exponer tu servidor Flask con ngrok:

```bash
ngrok http 5000
```

- Copiar la URL pública (por ejemplo `https://xxxx.ngrok-free.app`) y colocarla como dirección del webhook en el cuerpo del `watch()` o en los scripts específicos.

---

## 📋 Webhook Asana

### Pasos para crear el webhook:

1. Obtén tu **token personal** (PAT) en:  
   [https://app.asana.com/0/developer-console](https://app.asana.com/0/developer-console)

2. Obtén el **Workspace ID** y el **Project ID** usando la API de Asana o sus herramientas.

3. Exponer tu servidor Flask local con ngrok:

```bash
ngrok http 5000
```

4. Edita `asana/create_webhook.py`, reemplaza:

```python
ASANA_TOKEN = "tu_token_personal"
PROJECT_ID = "tu_project_id"
WEBHOOK_URL = "https://tu-ngrok-url.ngrok.io/webhook-asana"
```

5. Ejecuta el script para registrar el webhook:

```bash
python asana/create_webhook.py
```

6. Asegúrate de tener en `app.py` o un archivo separado el endpoint `/webhook-asana` para recibir y validar los eventos.

---

## 🚀 Endpoints disponibles

| Plataforma       | Endpoint             | Descripción                                         |
|------------------|----------------------|----------------------------------------------------|
| Google Calendar  | `/webhook-calendar`  | Recibe eventos creados o modificados               |
| Gmail            | `/webhook-gmail`     | Recibe notificaciones vía Pub/Sub                   |
| Google Drive     | `/webhook-drive`     | Recibe notificaciones por cambios en archivos      |
| Dropbox          | `/webhook-dropbox`   | Recibe notificaciones por cambios de archivos      |
| Slack            | `/slack-webhook`     | Recibe eventos y mensajes de Slack                  |
| ClickUp          | `/webhook-clickup`   | Recibe eventos de tareas (creación, edición, etc.) |
| Asana            | `/webhook-asana`     | Recibe eventos de proyectos y tareas en Asana      |
| Monday            | `/webhook-monday`     | Recibe eventos a los que el usuario se ha suscrito desde su workspace |

---

## 🎥 Video Tutoriales

### ▶️ Google Calendar Webhook  
[![Google Calendar Webhook](https://img.youtube.com/vi/kVy_RRfCHXQ/0.jpg)](https://youtu.be/kVy_RRfCHXQ)  
🔗 [Ver en YouTube](https://youtu.be/kVy_RRfCHXQ)

### ▶️ Gmail Webhook  
[![Gmail Webhook](https://img.youtube.com/vi/rGWagmPi_ek/0.jpg)](https://youtu.be/rGWagmPi_ek)  
🔗 [Ver en YouTube](https://youtu.be/rGWagmPi_ek)

### ▶️ Google Drive Webhook  
[![Google Drive Webhook](https://img.youtube.com/vi/vaf4G8jagUo/0.jpg)](https://youtu.be/vaf4G8jagUo)  
🔗 [Ver en YouTube](https://youtu.be/vaf4G8jagUo)

### ▶️ Dropbox Webhook Paso a Paso  
[![Dropbox Webhook](https://img.youtube.com/vi/uzKjRO4pOfc/0.jpg)](https://youtu.be/uzKjRO4pOfc)  
🔗 [Ver en YouTube](https://youtu.be/uzKjRO4pOfc)

### ▶️ Slack Webhook Introducción y Configuración  
[![Slack Webhook](https://img.youtube.com/vi/-V7rQy6kGSQ/0.jpg)](https://youtu.be/-V7rQy6kGSQ)  
🔗 [Ver en YouTube](https://youtu.be/-V7rQy6kGSQ)

### ▶️ ClickUp Webhook  
[![ClickUp Webhook](https://img.youtube.com/vi/NLrBBENwhRw/0.jpg)](https://youtu.be/NLrBBENwhRw)  
🔗 [Ver en YouTube](https://youtu.be/NLrBBENwhRw)

### ▶️ **Asana Webhook**  
[![Asana Webhook](https://img.youtube.com/vi/29fHsNAd1fQ/0.jpg)](https://youtu.be/29fHsNAd1fQ)  
🔗 [Ver en YouTube](https://youtu.be/29fHsNAd1fQ)

---

## 🔒 Seguridad

No subas archivos sensibles a Git:

- `client_secret_*.json`
- `token.pickle`
- `ambiente/` (entorno virtual)

Configura tu `.gitignore` así:

```gitignore
client_secret_*.json
token.pickle
ambiente/
__pycache__/
*.pyc
```

---

## 🪪 Licencia

MIT License © 2025
