from folders_services import find_folder_by_name, create_folder, get_folders_by_name
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

def create_folder_in_EE_folders(drive_service):

    educational_institutions_list = [
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
    ]

    for educational_institutions in educational_institutions_list:

        for educational_institution in educational_institutions:
            parent_folder_id = find_folder_by_name(drive_service, educational_institution, parent_id=None)

        file_metadata = {
        'name': "Bitácora",
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
        }   

        create_folder(drive_service, "Bitácora", parent_id=parent_folder_id)

        print(f"Carpeta 'Bitácora' creada en: {educational_institution}")
    
    