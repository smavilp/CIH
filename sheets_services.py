
def find_sheet_by_name(drive_service, sheet_name: str):
    print(f"Buscando hoja: {sheet_name}")
    query = (
        f"name='{sheet_name}' "
        "and mimeType = 'application/vnd.google-apps.spreadsheet' "
        "and trashed = false"
    )

    res = drive_service.files().list(
        q=query,
        fields="nextPageToken, files(id, name, parents)",
        spaces="drive",
        pageSize=200,
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        corpora="allDrives",
    ).execute()

    
    files = res.get("files", [])
    if not files:
        raise ValueError(f"No se encontró una Google Sheet llamada '{sheet_name}'")

    sheet_id = files[0]["id"]

    return sheet_id

def copy_sheet(drive_service, template_id: str, new_name: str, parent_folder_id: str):
    print(f"Copiando hoja '{new_name}' en la carpeta ID: {parent_folder_id}")
    copied_file = {
        "name": new_name,
        "parents": [parent_folder_id],
    }
    new_file = drive_service.files().copy(
        fileId=template_id,
        body=copied_file,
        supportsAllDrives=True,
    ).execute()
    return new_file.get("id")

