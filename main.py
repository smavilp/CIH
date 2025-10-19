from auth import get_oauth_credentials
from get_services import get_drive_service, get_sheet_service
from create_folder_architecture import create_folder_architecture
from folders_services import find_folder_by_name, create_folder, get_folders_by_name, get_folder_path, get_target_folders
from target_folders_names import target_folders_names_list
from dotenv import load_dotenv
import os
from utils import parse_path_info
from create_folder_in_EE_folders import create_folder_in_EE_folders
from db_services import add_column_to_db
from db_services import db_connect, insert_folder_in_db, get_folders_by_param, get_folder_ids_by_param, set_folders_assigned
from educational_institutions import assigned_institutions_list

def main():
    print("Iniciando el proceso main")

    load_dotenv()  # Cargar variables de entorno desde el archivo .env

    #OAUTH2_CLIENT_PATH = os.getenv("OAUTH2_CLIENT_PATH")

    # Llamamos a la función para obtener las credenciales OAuth
    #oauth_credentials = get_oauth_credentials(OAUTH2_CLIENT_PATH)


    # Llamamos a la función para obtener el cliente de Google Drive
    #drive_service = get_drive_service(oauth_credentials)

    # Llamamos a la función para obtener el cliente de Google Sheets
    #sheet_service = get_sheet_service(oauth_credentials)

    # Conexión a la base de datos SQLite
    db = db_connect()

    #files = drive_service.files().list(pageSize=1).execute()

    #CI_folder_id= find_folder_by_name(drive_service, "Centros de Interés")

    #files_in_CI_folder = drive_service.files().list(pageSize=1000, q=f"'{CI_folder_id}' in parents and trashed=false").execute()

    #print(f"Archivos en la carpeta 'Centros de Interés': {files_in_CI_folder.get('files', [])}")
    #Aquí puedes llamar a las funciones que necesites para interactuar con Google Drive y Google Sheets (crear arquitectura de carpetar, chequear los archivos subidos, etc.)

    #create_folder_architecture(drive_service, sheet_service)

    #target_folders = get_folders_by_name(drive_service,target_folders_names_list)

    #target_folders = get_target_folders(drive_service, target_folders_names_list, get_folders_by_name, get_folder_path,)

    #insert_folder_in_db(db,target_folders, parse_path_info)

    #create_folder_in_EE_folders(drive_service)

    # add_column_to_db(db, "folders", "assigned", "BOOLEAN", default_value=0)

    for assigned_institution in assigned_institutions_list:
        folder_ids = get_folder_ids_by_param(db, "educational_institution", assigned_institution)
        print(f"IDs de carpetas para la institución '{assigned_institution}': {folder_ids}")

        for folder_id in folder_ids:
            print(f"Procesando la carpeta con ID: {folder_id} para la institución: {assigned_institution}")
            set_folders_assigned(db, "id", folder_id)



    print("Proceso main finalizado")

main()



