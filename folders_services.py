from target_folders_names import target_folders_names_list

# Busca carpetas en Google Drive por nombre exacto y devuelve su ID
def find_folder_by_name(drive_service, folder_name: str, parent_id=None):

    # Query para Drive API (solo busca carpetas)
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    # Ejecutar búsqueda
    results = drive_service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)',
        pageSize=10
    ).execute()

    files = results.get('files', [])

    # Si encuentra la carpeta, devuelve su ID
    if files:
        print(f"Carpeta encontrada: {files[0]['name']} (id={files[0]['id']})")
        return files[0]['id']

    #  Si no se encuentra
    print(f"No se encontró carpeta con el nombre: '{folder_name}'")
    return None

# Crea una carpeta en Google Drive y devuelve su ID
def create_folder(drive_service, folder_name: str, parent_id=None):

    # Metadatos de la carpeta
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    # Crear la carpeta
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    print(f" Carpeta creada: {folder_name} (id={folder.get('id')})")
    return folder.get('id')

# Busca un grupo de carpeta según sus nombres

def get_folders_by_name(drive_service,target_folders_names_list):

    target_folders_list = []

    for target_name in target_folders_names_list:
        folder = drive_service.files().list(
            q=f"name='{target_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name)',
            pageSize=100
        ).execute()

        target_folders_list.extend(folder.get('files', []))

        print(f"Carpetas encontradas hasta ahora: {target_folders_list}")
        
    
    return target_folders_list

# Obtiene la ruta completa de una carpeta dada su ID

def get_folder_path(drive_service, folder_id):
    print(f"Obteniendo la ruta para la carpeta ID: {folder_id}")
    path = []
    current_id = folder_id

    while current_id:
        folder = drive_service.files().get(fileId=current_id, fields='id, name, parents', supportsAllDrives=True).execute()
        path.append(folder['name'])
        parents = folder.get('parents')
        current_id = parents[0] if parents else None

    return '/'.join(reversed(path))

# Obtiene las carpetas objetivo con sus rutas completas

def get_target_folders(drive_service, target_folders_names_list,get_folders_by_name,get_folder_path):

    target_folders = get_folders_by_name(drive_service, target_folders_names_list)

    for folder in target_folders:
        folder['path'] = get_folder_path(drive_service, folder['id'])
        print(f"Carpeta: {folder['name']}, ID: {folder['id']}, Ruta: {folder['path']}")

    return target_folders