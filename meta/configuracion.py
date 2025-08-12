import requests
import json
import urllib.parse

# ============ CONFIGURACIÓN ============
#para obtener credenciales de quien vamos a escuhcar ~!!no probado aun
APP_ID = ""
APP_SECRET = ""
USER_ACCESS_TOKEN = ""  # Si ya tienes, ponlo aquí. Sino déjalo vacío y sigue el flujo.

class FacebookWebhookAuth:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def get_app_access_token(self):
        print("🔑 Obteniendo token de aplicación...")
        url = f"{self.base_url}/oauth/access_token"
        params = {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'grant_type': 'client_credentials'
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'access_token' in data:
                print("✅ Token de aplicación obtenido")
                return data['access_token']
            else:
                print(f"❌ Error obteniendo token de app: {data}")
                return None
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
            return None
    
    def get_user_info(self, user_token):
        print("👤 Obteniendo información del usuario...")
        url = f"{self.base_url}/me"
        params = {
            'access_token': user_token,
            'fields': 'id,name,email'
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'id' in data:
                print(f"✅ Usuario encontrado: {data.get('name')} (ID: {data.get('id')})")
                return data
            else:
                print(f"❌ Error obteniendo info de usuario: {data}")
                return None
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
            return None
    
    def check_permissions(self, user_token):
        print("🔍 Verificando permisos del usuario...")
        url = f"{self.base_url}/me/permissions"
        params = {'access_token': user_token}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'data' in data:
                permissions = data['data']
                print("📋 Permisos encontrados:")
                for perm in permissions:
                    status = "✅" if perm['status'] == 'granted' else "❌"
                    print(f"  {status} {perm['permission']}: {perm['status']}")
                # No chequeamos user_likes porque no lo pedimos
                return True
            else:
                print(f"❌ Error verificando permisos: {data}")
                return False
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
            return False
    
    def subscribe_app_to_user(self, user_token, user_id):
        print("🔔 Verificando suscripciones del webhook...")
        app_token = self.get_app_access_token()
        if not app_token:
            return False
        url = f"{self.base_url}/{self.app_id}/subscriptions"
        params = {'access_token': app_token}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'data' in data:
                print("📡 Suscripciones de webhook encontradas:")
                for sub in data['data']:
                    print(f"  • Objeto: {sub.get('object')}")
                    print(f"  • Campos: {sub.get('fields', [])}")
                    print(f"  • URL: {sub.get('callback_url', 'N/A')}")
                    print(f"  • Activa: {sub.get('active', False)}\n")
                # Verificamos que el webhook esté suscrito a "likes"
                for sub in data['data']:
                    if sub.get('object') == 'user' and 'likes' in sub.get('fields', []):
                        print("✅ Suscripción de likes de usuario encontrada y activa")
                        return True
                print("❌ No se encontró suscripción para likes de usuario")
                print("💡 Asegúrate de configurar el webhook en Meta Developers para objeto 'user' con campo 'likes'")
                return False
            else:
                print(f"❌ Error obteniendo suscripciones: {data}")
                return False
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
            return False
    
    def generate_auth_url(self):
        print("🔗 Generando URL de autorización...")
        redirect_uri = "https://a21b739475b6.ngrok-free.app/fb-auth-callback"
        scope = "public_profile,email"  # Aquí solo permisos básicos
        
        auth_url = (
            f"https://www.facebook.com/v18.0/dialog/oauth?"
            f"client_id={self.app_id}&"
            f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
            f"scope={scope}&"
            f"response_type=code"
        )
        print(f"🌐 Ve a esta URL y autoriza la aplicación:")
        print(auth_url)
        print("\n📝 Después de autorizar, Facebook te redirigirá a una página de error.")
        print("🔍 Copia el código de la URL (después de 'code=') y pégalo aquí:")
        return redirect_uri
    
    def exchange_code_for_token(self, code, redirect_uri):
        print("🔄 Intercambiando código por token...")
        url = f"{self.base_url}/oauth/access_token"
        params = {
            'client_id': self.app_id,
            'redirect_uri': redirect_uri,
            'client_secret': self.app_secret,
            'code': code
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'access_token' in data:
                print("✅ Token de usuario obtenido exitosamente")
                print(f"🔑 Token: {data['access_token'][:20]}...")
                return data['access_token']
            else:
                print(f"❌ Error obteniendo token: {data}")
                return None
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
            return None

def main():
    print("=" * 60)
    print("🚀 SCRIPT DE AUTORIZACIÓN FACEBOOK WEBHOOK PARA LIKES (PERMISOS BÁSICOS)")
    print("=" * 60)
    print()
    
    if APP_ID == "TU_APP_ID_AQUI" or APP_SECRET == "TU_APP_SECRET_AQUI":
        print("❌ Por favor, configura APP_ID y APP_SECRET al inicio del script")
        return
    
    auth = FacebookWebhookAuth(APP_ID, APP_SECRET)
    
    app_token = auth.get_app_access_token()
    if not app_token:
        print("❌ No se pudo obtener token de aplicación. Verifica APP_ID y APP_SECRET")
        return
    
    print()
    print("🎯 Ahora necesitamos autorizar un usuario para recibir notificaciones de likes (sin pedir permiso user_likes).")
    print()
    
    if USER_ACCESS_TOKEN:
        print("🔑 Usando token de usuario proporcionado...")
        user_token = USER_ACCESS_TOKEN
    else:
        redirect_uri = auth.generate_auth_url()
        code = input("Pega el código aquí: ").strip()
        if not code:
            print("❌ Código requerido para continuar")
            return
        user_token = auth.exchange_code_for_token(code, redirect_uri)
        if not user_token:
            return
    
    print()
    print("📊 VERIFICANDO CONFIGURACIÓN:")
    print("-" * 40)
    
    user_info = auth.get_user_info(user_token)
    if not user_info:
        return
    
    has_basic_perm = auth.check_permissions(user_token)
    
    is_subscribed = auth.subscribe_app_to_user(user_token, user_info['id'])
    
    print()
    print("📋 RESUMEN:")
    print("-" * 40)
    print(f"✅ Usuario autorizado: {user_info.get('name')}")
    print(f"✅ Permisos básicos concedidos (public_profile, email)")
    print(f"{'✅' if is_subscribed else '❌'} Webhook configurado: {'Sí' if is_subscribed else 'No'}")
    
    if is_subscribed:
        print()
        print("🎉 ¡TODO CONFIGURADO CORRECTAMENTE!")
        print("👍 Ahora puedes dar like a páginas y deberías recibir la notificación en tu webhook.")
        print(f"🔗 URL del webhook: https://a21b739475b6.ngrok-free.app/webhook-meta")
        print()
        print("💡 Para probar:")
        print("1. Da like a alguna página en Facebook.")
        print("2. Revisa los logs de tu aplicación Flask.")
        print("3. Deberías ver la notificación llegar.")
    else:
        print()
        print("⚠️  HAY PROBLEMAS EN LA CONFIGURACIÓN:")
        print("• El webhook debe estar configurado en Meta Developers para objeto 'user' con campo 'likes'")

if __name__ == "__main__":
    main()
