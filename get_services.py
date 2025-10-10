from googleapiclient.discovery import build

def get_drive_service(oauth_credentials):

    # Construir el cliente de la API de Google Drive
    drive_service = build('drive', 'v3', credentials=oauth_credentials)

    print("Cliente de Google Drive creado.")
    return drive_service

def get_sheet_service(oauth_credentials):
    
    # Construir el cliente de la API de Google Sheets
    sheet_service = build('sheets', 'v4', credentials=oauth_credentials)

    print("Cliente de Google Sheets creado.")
    return sheet_service