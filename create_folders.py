from educational_institutions import (
    educational_institutions_antioquia,
    educational_institutions_atlantico,
    educational_institutions_bolivar,
    educational_institutions_boyaca,    
    educational_institutions_caldas,
    educational_institutions_choco,
    educational_institutions_cordoba,
    educational_institutions_risaralda,
    educational_institutions_santander,
    educational_institutions_sucre
)

def create_folders(drive_service):

    def find_folder(drive_service, folder_name, parent_id=None):
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        files = results.get('files', [])
        return files[0]['id'] if files else None

    proyecto_folder_id = find_folder(drive_service, "Proyecto Centros de Interés en Historia")
    if not proyecto_folder_id:
        raise Exception("No se encontró la carpeta 'Proyecto Centros de Interés en Historia'.")

    seguimiento_folder_id = find_folder(drive_service, "04_Seguimiento", parent_id=proyecto_folder_id)
    if not seguimiento_folder_id:
        raise Exception("No se encontró la carpeta '04_Seguimiento' dentro de 'Proyecto Centros de Interés en Historia'.")

    centros_folder_id = find_folder(drive_service, "Centros de Interés", parent_id=seguimiento_folder_id)
    if not centros_folder_id:
        raise Exception("No se encontró la carpeta 'Centros de Interés' dentro de '04_Seguimiento'.")

    #Cambiar en los argumentos de la función el nombre de la carpeta del departamento en que desea crear las subcarpetas

    departamento_folder_id = find_folder(drive_service, "Boyacá", parent_id=centros_folder_id)
    if not departamento_folder_id:
        raise Exception("No se encontró la carpeta del departamento dentro de 'Centros de Interés'.")

    # Crear una carpeta por cada establecimiento educativo dentro de la carpeta del departamento

    for educational_institution in educational_institutions_boyaca:
        metadata = {
            'name': educational_institution,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [departamento_folder_id]
        }
        carpeta = drive_service.files().create(body=metadata, fields='id').execute()
        print(f"Carpeta '{educational_institution}' creada con ID: {carpeta.get('id')}")
