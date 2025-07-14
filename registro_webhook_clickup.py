import requests

# Configuración
API_TOKEN = "tu token aqui"
TEAM_ID = "tu team id"
SPACE_ID = "tu space id"  # ID del espacio ClickUp
PUBLIC_URL = "https://0c2d64601b50.ngrok-free.app/webhook-clickup"  # Reemplaza por tu URL pública real

def registrar_webhook():
    url = f"https://api.clickup.com/api/v2/team/{TEAM_ID}/webhook"
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "endpoint": PUBLIC_URL,
        "events": ["taskCreated", "taskUpdated", "taskDeleted"],
        "space_ids": [SPACE_ID]
    }

    print("Registrando webhook en ClickUp...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Webhook registrado con éxito:")
        print(response.json())
    else:
        print(f"❌ Error al registrar webhook ({response.status_code}):")
        print(response.text)

if __name__ == "__main__":
    registrar_webhook()
