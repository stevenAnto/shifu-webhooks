# Google Calendar Webhook con Flask

Este proyecto implementa un webhook para Google Calendar usando Flask en Python.  
Permite recibir notificaciones en tiempo real cuando hay cambios en el calendario, usando la API de Google Calendar y OAuth 2.0 para autenticación.

---

## 📁 Estructura del proyecto

- `app.py`: Servidor Flask que recibe las notificaciones (webhook).
- `activate_watch.py`: Script para activar el webhook y registrar la URL de escucha.
- `authorize.py`: Script para autorizar la app con OAuth y obtener credenciales.
- `calculoExpiration.py`: Utilidad para manejar expiración del webhook.
- `client_secret_*.json`: Archivo con credenciales OAuth (NO subir a repositorio).
- `token.pickle`: Token de acceso generado tras autorizar la app (NO subir a repositorio).
- `ambiente/`: Entorno virtual Python.
- `requirements.txt`: Dependencias del proyecto.

---

## ⚙️ Configuración

1. Crear un proyecto en Google Cloud Console y habilitar la API de Google Calendar.
2. Descargar las credenciales OAuth (`client_secret_*.json`).
3. Crear un entorno virtual e instalar dependencias:

```bash
python3 -m venv ambiente
source ambiente/bin/activate
pip install -r requirements.txt
```

4. Ejecutar `authorize.py` para obtener el token de acceso:

```bash
python authorize.py
```

5. Ejecutar `activate_watch.py` para activar el webhook y registrar tu endpoint.

6. Levantar el servidor Flask:

```bash
python app.py
```

7. Exponer tu servidor con [ngrok](https://ngrok.com) u otra herramienta para que la URL del webhook sea pública:

```bash
ngrok http 5000
```

---

## 🚀 Uso

- Cada vez que hagas un cambio en Google Calendar, la app recibirá una notificación `POST` en `/webhook-calendar`.
- Puedes extender `app.py` para consultar los eventos modificados y procesarlos según tu lógica.

---

## 🎥 Video Tutorial

Para una guía paso a paso, puedes ver el siguiente video:

[![Video Tutorial](https://img.youtube.com/vi/kVy_RRfCHXQ/0.jpg)](https://youtu.be/kVy_RRfCHXQ)

🔗 [Ver en YouTube](https://youtu.be/kVy_RRfCHXQ)

---

## 🔒 Seguridad

Recuerda **NO subir** al repositorio archivos con credenciales ni tokens sensibles como:

- `client_secret_*.json`
- `token.pickle`

Asegúrate de tener un `.gitignore` configurado correctamente.

---

## 🪪 Licencia

MIT License © 2025

---
