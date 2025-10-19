from google_auth_oauthlib.flow import InstalledAppFlow


# Alcances de permisos para la API de Google Drive
OAUTH_SCOPES = ['https://www.googleapis.com/auth/drive', "https://www.googleapis.com/auth/spreadsheets.readonly" ]


def get_oauth_credentials(OAUTH2_CLIENT_PATH):

    # Flujo de autenticación OAuth 2.0
    flow = InstalledAppFlow.from_client_secrets_file(OAUTH2_CLIENT_PATH, OAUTH_SCOPES)
    oauth_credentials = flow.run_local_server(port=0)
    return oauth_credentials

