from auth import get_oauth_credentials
from get_services import get_drive_service, get_sheet_service
from create_folder_architecture import create_folder_architecture
from folders_services import find_folder_by_name, create_folder, get_folders_by_name, get_folder_path, get_target_folders
from target_folders_names import target_folders_names_list
from dotenv import load_dotenv
import os



def main():
    print("Iniciando el proceso main")

    load_dotenv()  # Cargar variables de entorno desde el archivo .env

    OAUTH2_CLIENT_PATH = os.getenv("OAUTH2_CLIENT_PATH")

    # Llamamos a la función para obtener las credenciales OAuth
    oauth_credentials = get_oauth_credentials(OAUTH2_CLIENT_PATH)

    # Llamamos a la función para obtener el cliente de Google Drive
    drive_service = get_drive_service(oauth_credentials)

    # Llamamos a la función para obtener el cliente de Google Sheets
    sheet_service = get_sheet_service(oauth_credentials)

    #files = drive_service.files().list(pageSize=1).execute()

    #CI_folder_id= find_folder_by_name(drive_service, "Centros de Interés")

    #files_in_CI_folder = drive_service.files().list(pageSize=1000, q=f"'{CI_folder_id}' in parents and trashed=false").execute()

    #print(f"Archivos en la carpeta 'Centros de Interés': {files_in_CI_folder.get('files', [])}")
    #Aquí puedes llamar a las funciones que necesites para interactuar con Google Drive y Google Sheets (crear arquitectura de carpetar, chequear los archivos subidos, etc.)

    # create_folder_architecture(drive_service, sheet_service)

    #target_folders = get_folders_by_name(drive_service,target_folders_names_list)

    #get_target_folders(drive_service, target_folders_names_list, get_folders_by_name, get_folder_path,)



    print("Proceso main finalizado")

main()



