from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # Carga el token guardado si existe
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, solicita autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_722584203991-psbocitc7vdn81btjf8en3ujf6b78gi0.apps.googleusercontent.com.json',
                SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda el token para uso futuro
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    print("✅ Autorización completada y token guardado.")

if __name__ == '__main__':
    main()