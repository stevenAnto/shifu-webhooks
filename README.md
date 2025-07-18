# 🔔 Webhooks con Flask: Google Calendar, Gmail, Google Drive, Dropbox, Slack y ClickUp

Este proyecto implementa **seis webhooks en Flask** para escuchar cambios en:

- 📅 Google Calendar  
- 📥 Gmail  
- 📂 Google Drive  
- 📁 Dropbox  
- 💬 Slack (solo para el workspace donde la app ha sido creada)  
- ✅ ClickUp (eventos en tareas)
- 📋 **Asana** (eventos en proyectos)
- ✅ Notion (eventos en pages and databases de un workspace determinado)


Utiliza OAuth 2.0 para autenticación (para Google APIs) y tokens de acceso para Dropbox, Slack y ClickUp.  
Los cambios se notifican en tiempo real a tu servidor Flask usando la funcionalidad de webhooks de cada plataforma.

---

## 📁 Estructura del proyecto

```bashgg
.
├── app.py                         # Servidor Flask: maneja todos los webhooks
├── activate_watch_google_calendar.py  # Activa webhook de Google Calendar
├── activate_watch_gmail.py        # Activa webhook de Gmail (Pub/Sub)
├── activate_watch_drive.py        # Activa webhook de Google Drive
├── authorize_google_calendar.py   # Autenticación para Google Calendar
├── authorize_google_gmail.py      # Autenticación para Gmail
├── authorize_google_drive.py      # Autenticación para Google Drive
├── calculoExpiration.py           # Calcula expiración del webhook de Calendar
├── registro_webhook_clickup.py    # Registro del webhook de ClickUp
├── requirements.txt               # Dependencias
├── ambiente/                      # Entorno virtual
├── client_secret_*.json           # Credenciales OAuth (NO subir)
├── token.pickle                   # Token de acceso Google (NO subir)
├── asana/
│   └── create_webhook.py          # Script para crear webhook en Asana
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

En los scripts `activate_watch_google_calendar.py`, `activate_watch_drive.py`, etc., asegúrate de:

- Exponer tu servidor Flask con ngrok:

```bash
ngrok http 5000
```

- Copiar la URL pública (por ejemplo `https://xxxx.ngrok-free.app`) y colocarla como dirección del webhook en el cuerpo del `watch()` (puede requerir editar el script si aún no lo implementaste).

### 4. Caso especial: Gmail con Pub/Sub

En `activate_watch_gmail.py`, no defines la URL de tu webhook directamente. Gmail envía notificaciones al **tópico Pub/Sub** (`gmail-notify`), y tú debes:

- Ir a Google Cloud Console
- Buscar ese tópico (`gmail-notify`)
- Crear una **suscripción Push** con destino:

```
https://<tu-ngrok>.ngrok-free.app/webhook-gmail
```

> Gmail → Pub/Sub → Suscripción Push → Tu servidor Flask

---

## 📅 Google Calendar Webhook

### 🔧 Configuración

1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/).
2. Habilita la **API de Google Calendar**.
3. Descarga el archivo `client_secret_*.json`.
4. Ejecuta `authorize_google_calendar.py` para autenticarte:

```bash
python authorize_google_calendar.py
```

5. Ejecuta `activate_watch_google_calendar.py` para activar el webhook (edita la URL pública si es necesario):

```bash
python activate_watch_google_calendar.py
```

6. Levanta tu servidor Flask:

```bash
python app.py
```

7. Expón tu endpoint con ngrok:

```bash
ngrok http 5000
```

> Notificaciones llegarán a `/webhook-calendar`.

---

## 📥 Gmail Webhook

Este webhook escucha cambios en el buzón Gmail usando **Google Pub/Sub**.

### Pasos

1. Habilita la **Gmail API** y Pub/Sub en Google Cloud.
2. Ejecuta la autenticación:

```bash
python authorize_google_gmail.py
```

3. Ejecuta el script:

```bash
python activate_watch_gmail.py
```

4. Luego, en Google Cloud Console, ve a Pub/Sub > Tópicos > `gmail-notify` y crea una **suscripción Push** que apunte a tu endpoint:

```
https://<tu-ngrok>.ngrok-free.app/webhook-gmail
```

> Las notificaciones llegarán a `/webhook-gmail`.

---

## 📂 Google Drive Webhook

Este webhook escucha cambios en archivos de Google Drive.

### Pasos

1. Habilita la **Google Drive API** en Google Cloud.
2. Ejecuta la autenticación:

```bash
python authorize_google_drive.py
```

3. Crea el webhook (asegúrate de establecer la URL pública):

```bash
python activate_watch_drive.py
```

> Las notificaciones llegarán a `/webhook-drive`.

---

## 📁 Dropbox Webhook

Este webhook recibe cambios de cuentas vinculadas a tu app en Dropbox.

### Pasos

1. Ve a [Dropbox Developers](https://www.dropbox.com/developers/apps).
2. Crea una app y activa los siguientes permisos:
   - `files.metadata.read`
   - `files.content.read` (opcional)
3. Agrega la URL del webhook en la sección **Webhook URI** (`https://XXXX.ngrok-free.app/webhook-dropbox`).
4. Genera un token de acceso desde el dashboard y guárdalo.
5. Haz cambios en tu cuenta Dropbox y observa que lleguen a `/webhook-dropbox`.

> El webhook notificará cambios, pero no incluye detalles. Usa la API Dropbox con tu token para consultar qué cambió.

---

## 💬 Slack Webhook

Este webhook recibe eventos en tiempo real de Slack **solo para el workspace donde la app ha sido creada e instalada**.

### ¿Qué hace?

- Escucha eventos como mensajes en canales públicos o reacciones añadidas.
- Recibe notificaciones vía HTTP POST en tu servidor Flask.
- Permite a tu bot responder automáticamente mensajes usando el token de bot.

---

## ✅ ClickUp Webhook

Este webhook escucha eventos en tareas de un espacio de ClickUp.

### Pasos

1. Obtén tu `team_id` y `space_id` usando la API de ClickUp.
2. Levanta tu servidor Flask:

```bash
python app.py
```

3. Expón tu endpoint con ngrok:

```bash
ngrok http 5000
```

4. Edita el archivo `registro_webhook_clickup.py` y reemplaza:
   - `PUBLIC_URL` con la URL pública generada por ngrok.
   - `TEAM_ID` y `SPACE_ID` con los valores obtenidos de la API de ClickUp.

5. Ejecuta el registro del webhook:

```bash
python registro_webhook_clickup.py
```

> ClickUp enviará eventos como `taskCreated`, `taskUpdated`, `taskDeleted` a `/webhook-clickup`.

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
## 📋 Webhook Monday

### Pasos para crear el webhook:


3. exponer tu servidor flask local con ngrok:

- el endpoint es  /webhook-monday

- Funciona solo cuando el usuario registra la url publica en su workspace manualmente. Es decir, el usuario debe crearse un espacio 
 y registrar la url publica para recibir notificaciones


```bash
ngrok http 5000
```
## 📋 Webhook Notion

### Pasos para crear el webhook:
0. Levantar el endpoint en una url publica

1. Cerar una integracion en su espacio de trabajo.

2. En settings de dicha integracion, poner la url para su suscripcion(enviara un token)

3. Verify  con el token para que comience escuchar

4. En setting de la integracion agregar Acces (paginas y bases de datos de los cuales se quiere escuchar)



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

### ▶️ **Monday Webhook**  
[![Asana Webhook](https://img.youtube.com/vi/29fHsNAd1fQ/0.jpg)](https://youtu.be/igcrTDy7xtI)  
🔗 [Ver en YouTube](https://youtu.be/igcrTDy7xtI)

### ▶️ **Monday Webhook**  
[![Asana Webhook](https://img.youtube.com/vi/29fHsNAd1fQ/0.jpg)](https://youtu.be/_wRslFjjnIE)  
🔗 [Ver en YouTube](https://youtu.be/_wRslFjjnIE)


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
| Notion            | `/webhook-notion`     | Recibe eventos de paginas y Base dedatos accesados por la integracion|


---

## 🔒 Seguridad

Asegúrate de no subir archivos sensibles a Git:

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
