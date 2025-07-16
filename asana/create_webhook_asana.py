import requests

#reemplazar con sus credenciales respectivas
ASANA_TOKEN = "token"
PROJECT_ID = "id_proyecto"
WEBHOOK_URL = "url publica para escuhcar"  

headers = {
    "Authorization": f"Bearer {ASANA_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "data": {
        "target": WEBHOOK_URL,
        "resource": PROJECT_ID
    }
}

response = requests.post("https://app.asana.com/api/1.0/webhooks", json=data, headers=headers)

print(response.status_code)
print(response.json())
