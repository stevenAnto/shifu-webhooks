import json
import requests
from datetime import datetime, timedelta, timezone

# Configura tu endpoint de ngrok aquí
NOTIFICATION_URL = "https://988d3a68ef22.ngrok-free.app/webhook-oneDrive"

# Cargar el access_token
try:
    with open("tokens.json") as f:
        tokens = json.load(f)
except FileNotFoundError:
    print("❌ Error: No se encontró el archivo tokens.json")
    exit(1)

access_token = tokens.get("access_token")
if not access_token:
    print("❌ Error: No se encontró access_token en tokens.json")
    exit(1)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Fecha de expiración: máximo 1 hora para OneDrive personal (usando timezone-aware datetime)
expiration = (datetime.now(timezone.utc) + timedelta(minutes=59)).isoformat().replace('+00:00', 'Z')

# Configuración de la suscripción
data = {
    "changeType": "updated",  # También puedes usar "created,updated,deleted"
    "notificationUrl": NOTIFICATION_URL,
    "resource": "me/drive/root",  # Monitorea la raíz del OneDrive
    "expirationDateTime": expiration,
    "clientState": "miEstadoSeguro123"
}

print("🔄 Creando suscripción...")
print(f"📍 URL de notificación: {NOTIFICATION_URL}")
print(f"📅 Expiración: {expiration}")

try:
    response = requests.post(
        "https://graph.microsoft.com/v1.0/subscriptions", 
        headers=headers, 
        json=data,
        timeout=30
    )
    
    print(f"📊 Código de respuesta: {response.status_code}")
    
    if response.status_code == 201:
        subscription = response.json()
        print("✅ ¡Suscripción creada exitosamente!")
        print(f"🆔 ID de suscripción: {subscription.get('id')}")
        
        # Guardar la información de la suscripción
        with open("suscripcion_onedrive.json", "w") as f:
            json.dump(subscription, f, indent=2)
        print("💾 Información de suscripción guardada en 'suscripcion_onedrive.json'")
        
    else:
        print("❌ Error al crear la suscripción:")
        print("📬 Respuesta de la API:")
        try:
            error_info = response.json()
            print(json.dumps(error_info, indent=2))
            
            # Ayuda específica para errores comunes
            if "ValidationError" in str(error_info):
                print("\n💡 Sugerencias para resolver el ValidationError:")
                print("1. Asegúrate de que tu servidor Flask esté ejecutándose")
                print("2. Verifica que ngrok esté funcionando y apuntando al puerto correcto")
                print("3. Confirma que la URL de ngrok sea accesible desde internet")
                print("4. El endpoint debe responder con status 200 y devolver el validationToken")
                
        except json.JSONDecodeError:
            print(response.text)
            
except requests.exceptions.RequestException as e:
    print(f"❌ Error de conexión: {str(e)}")
except Exception as e:
    print(f"❌ Error inesperado: {str(e)}")

print("\n📋 Pasos siguientes:")
print("1. Asegúrate de que tu webhook esté respondiendo correctamente")
print("2. Monitorea los logs para ver las notificaciones entrantes")
print("3. La suscripción expirará en 1 hora, necesitarás renovarla")