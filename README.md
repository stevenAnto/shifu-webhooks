
# 🔔 Webhooks con Flask: Google Calendar, Gmail, Dropbox, Slack y ClickUp

Este proyecto implementa **cinco webhooks en Flask** para escuchar cambios en:

- 📅 Google Calendar  
- 📥 Gmail (no agregado aún)  
- 📁 Dropbox  
- 💬 Slack (solo para el workspace donde la app ha sido creada)  
- ✅ ClickUp (eventos en tareas)

Utiliza OAuth 2.0 para autenticación (para Google APIs) y tokens de acceso para Dropbox, Slack y ClickUp.  
Los cambios se notifican en tiempo real a tu servidor Flask usando la funcionalidad de webhooks de cada plataforma.

---

## 📁 Estructura del proyecto

```bash
.
├── app.py                      # Servidor Flask: maneja todos los webhooks
├── activate_watch.py           # Activa webhook de Google Calendar
├── authorize.py                # Autenticación OAuth para Google Calendar y Gmail
├── calculoExpiration.py        # Calcula expiración del webhook de Calendar
├── registro_webhook_clickup.py # Registro del webhook de ClickUp
├── utils.py                    # Funciones auxiliares
├── requirements.txt            # Dependencias
├── ambiente/                   # Entorno virtual
├── client_secret_*.json        # Credenciales OAuth (NO subir)
├── token.pickle                # Token de acceso Google (NO subir)
```

---

## ⚙️ Configuración General

### 1. Crear entorno virtual e instalar dependencias

```bash
python3 -m venv ambiente
source ambiente/bin/activate
pip install -r requirements.txt
```

---

## 📅 Google Calendar Webhook

### 🔧 Configuración

1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/).
2. Habilita la **API de Google Calendar**.
3. Descarga el archivo `client_secret_*.json`.
4. Ejecuta `authorize.py` para autenticarte:

```bash
python authorize.py
```

5. Ejecuta `activate_watch.py` para activar el webhook:

```bash
python activate_watch.py
```

6. Levanta tu servidor Flask:

```bash
python app.py
```

7. Expón tu endpoint con ngrok:

```bash
ngrok http 5000
```

> Notificaciones llegarán a `/webhook-calendar` cuando se creen o modifiquen eventos.

---

## 📥 Gmail Webhook

Este webhook escucha cambios en el buzón Gmail usando Pub/Sub.

### Pasos

1. Habilita la **Gmail API** en Google Cloud.
2. Configura Pub/Sub y una suscripción push hacia `/webhook-gmail`.
3. Usa `authorize.py` para autorizar acceso.
4. Modifica `app.py` para manejar el POST en `/webhook-gmail`.

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
- Solo recibe eventos del workspace donde la app está instalada (no es global).

---

## ✅ ClickUp Webhook

Este webhook escucha eventos en tareas de un espacio de ClickUp.

### Pasos

1. Obtén tu `team_id` y `space_id` usando la API de ClickUp (o un script como apoyo).
2. Levanta tu servidor Flask:

```bash
python app.py
```

3. Expón tu endpoint con ngrok:

```bash
ngrok http 5000
```

4. Edita el archivo `registro_webhook_clickup.py` y reemplaza `PUBLIC_URL` con la URL pública de ngrok.

5. Ejecuta el registro del webhook:

```bash
python registro_webhook_clickup.py
```

> ClickUp enviará eventos como `taskCreated`, `taskUpdated`, `taskDeleted` a `/webhook-clickup`.

---

## 🎥 Video Tutoriales

### ▶️ Google Calendar Webhook
[![Google Calendar Webhook](https://img.youtube.com/vi/kVy_RRfCHXQ/0.jpg)](https://youtu.be/kVy_RRfCHXQ)  
🔗 [Ver en YouTube](https://youtu.be/kVy_RRfCHXQ)

### ▶️ Dropbox Webhook Paso a Paso
[![Dropbox Webhook](https://img.youtube.com/vi/uzKjRO4pOfc/0.jpg)](https://youtu.be/uzKjRO4pOfc)  
🔗 [Ver en YouTube](https://youtu.be/uzKjRO4pOfc)

### ▶️ Slack Webhook Introducción y Configuración
[![Slack Webhook](https://img.youtube.com/vi/-V7rQy6kGSQ/0.jpg)](https://youtu.be/-V7rQy6kGSQ)  
🔗 [Ver en YouTube](https://youtu.be/-V7rQy6kGSQ)

### ▶️ ClickUp Webhook
[![ClickUp Webhook](https://img.youtube.com/vi/NLrBBENwhRw/0.jpg)](https://youtu.be/NLrBBENwhRw)  
🔗 [Ver en YouTube](https://youtu.be/NLrBBENwhRw)

---

## 🚀 Endpoints disponibles

| Plataforma       | Endpoint             | Descripción                                         |
|------------------|----------------------|-----------------------------------------------------|
| Google Calendar  | `/webhook-calendar`  | Recibe eventos creados o modificados               |
| Gmail            | `/webhook-gmail`     | Recibe notificaciones vía Pub/Sub                  |
| Dropbox          | `/webhook-dropbox`   | Recibe notificaciones por cambios de archivos      |
| Slack            | `/slack-webhook`     | Recibe eventos y mensajes de Slack                 |
| ClickUp          | `/webhook-clickup`   | Recibe eventos de tareas (creación, edición, etc.) |

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
